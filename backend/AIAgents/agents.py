import json
import re
import os
from .models import State
from .logger import logger
from langchain_groq import ChatGroq
from ..config import CONFIG
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

planner_llm = ChatGroq(model="openai/gpt-oss-120b",api_key=api_key)
executor_llm = ChatGroq(model="llama-3.1-8b-instant",api_key=api_key)
codereview_llm = ChatGroq(model="openai/gpt-oss-20b",api_key=api_key)
supervisor_llm = ChatGroq(model="qwen/qwen3-32b",api_key=api_key)
summary_llm = ChatGroq(model="openai/gpt-oss-20b",api_key=api_key)
feedback_llm = ChatGroq(model="openai/gpt-oss-20b",api_key=api_key)
response_llm = ChatGroq(model="llama-3.3-70b-versatile",api_key=api_key)

JSON_FENCE_RE = re.compile(r"```(?:json)?\s*([\s\S]*?)\s*```", re.IGNORECASE)
ANY_FENCE_RE = re.compile(r"```(?:[a-zA-Z0-9_+-]+)?\s*([\s\S]*?)\s*```")

def _preview_text(text: str, limit: int = 1000) -> str:
    if text is None:
        return ""
    s = str(text)
    s = s.replace("\r\n", "\n").replace("\r", "\n")
    if len(s) <= limit:
        return s
    return s[:limit] + f"\n...[truncated {len(s) - limit} chars]"

def _log_agent_llm_response(*, agent: str, response_text: str, state: State, extra: dict | None = None) -> None:
    payload = {
        "event": "llm_response",
        "chars": len(response_text or ""),
        "preview": _preview_text(response_text or ""),
    }
    if extra:
        payload.update(extra)
    logger.logit("INFO", agent, payload, state)

def _extract_code_text(raw: str) -> str:
    """
    Best-effort extraction of code when the model includes reasoning/prose.
    Prefers fenced code blocks; otherwise takes the first plausible Python code line onward.
    """
    if raw is None:
        return ""
    text = raw.strip()
    if not text:
        return ""
    m = ANY_FENCE_RE.search(text)
    if m:
        return m.group(1).strip()
    if "<think>" in text and "</think>" in text:
        after = text.split("</think>", 1)[1].strip()
        if after:
            text = after
    starters = ("from ", "import ", "def ", "class ", "@", "if __name__")
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.lstrip().startswith(starters):
            return "\n".join(lines[i:]).strip()

    return text

def _extract_json_text(raw: str) -> str:
    """Extract a JSON object/array string from a model response."""
    if raw is None:
        return ""
    text = raw.strip()
    if not text:
        return ""

    m = JSON_FENCE_RE.search(text)
    if m:
        text = m.group(1).strip()
    obj_start = text.find("{")
    if obj_start != -1:
        return text[obj_start:].strip()
    return text

def _safe_json_loads(raw: str, *, context: str, state: State) -> dict:
    extracted = _extract_json_text(raw)
    decoder = json.JSONDecoder()
    try:
        parsed, _ = decoder.raw_decode(extracted)
        if not isinstance(parsed, dict):
            raise ValueError(f"Expected JSON object, got {type(parsed).__name__}")
        return parsed
    except Exception as e:
        if raw:
            for i, ch in enumerate(raw):
                if ch != "{":
                    continue
                try:
                    candidate, _ = decoder.raw_decode(raw[i:])
                    if isinstance(candidate, dict):
                        return candidate
                except Exception:
                    continue
        logger.logit(
            "ERROR",
            context,
            {
                "event": "json_parse_failed",
                "error": str(e),
                "raw_preview": (raw or "")[:500],
                "extracted_preview": (extracted or "")[:500],
            },
            state,
        )
        return {}
async def PlannerAgent(state: State) -> State:
    user_message = state['user_message']
    logger.logit("INFO", "Planner Agent", "Starting Planner Agent", state)
    prompt = f"""
    You are an exceptional Senior Software Engineer. Your primary task is to carefully plan the approach for the following user request and provide structured, detailed instructions for each specialized agent in the workflow. The goal is to ensure clear delegation, a logical flow, and a high-quality result for the user's objective.

    For the following user request, break down the task into actionable steps. Assign responsibilities to each agent described below, ensuring each receives clear, detailed, and relevant prompts:

    Agent 1: Executor Agent
    - Responsible for generating complete, correct, and efficient code that addresses the user's request.
    - Provide precise coding requirements, contain the overall implementation strategy, and clarify any assumptions.

    Agent 2: Code Review Agent
    - Responsible for thoroughly reviewing the code produced by the Executor Agent.
    - Instruct on code quality, adherence to best practices, logic correctness, potential optimizations, and error checking.
    - Request constructive, actionable feedback and suggest improvements if necessary.

    Agent 3: Summary Agent
    - Responsible for summarizing the resulting codebase and its structure after implementation.
    - Clarify what was achieved, key functionalities, architectural choices, and how the parts fit together.
    - Make the summary understandable for both technical and non-technical stakeholders.

    Agent 4: Feedback Agent
    - Responsible for providing suggestions for further improvements, new features, optimizations, or alternative solutions.
    - Encourage creative thinking and identify areas where the user can take their project to the next level.

    Provide detailed and actionable instructions for each agent in the workflow to effectively address the user's request. Your response must be a JSON object, where each key corresponds to an agent and the value is a specific, clear instruction tailored for that agent to perform their role.

    # Task: {user_message}
    # Return your answer strictly in the following JSON format, filling in each value with precise, agent-specific instructions for this task:
    Example:
    {{
        "Executor": "Write exact step-by-step coding instructions and requirements for the Executor Agent to implement the user's request.",
        "CodeReviewer": "Clearly outline the review criteria, checks to perform, and feedback expectations for the Code Review Agent.",
        "Summary": "Give explicit summary points the Summary Agent should cover when describing the completed solution.",
        "Feedback": "List concrete suggestions or improvements the Feedback Agent should consider based on the implementation."
    }}

    Replace the values in quotes above with specific instructions derived from the user's task.
    """

    response = await planner_llm.ainvoke(prompt)
    _log_agent_llm_response(agent="Planner Agent", response_text=response.content, state=state)
    response_content = _safe_json_loads(response.content, context="Planner Agent", state=state)
    logger.logit(
        "INFO",
        "Planner Agent",
        {"event": "planner_instructions_ready", "keys": list(response_content.keys())},
        state,
    )
    if not response_content:

        response_content = {
            "Executor": "Implement the user request end-to-end with production-quality code. Make reasonable assumptions and keep the solution minimal and correct.",
            "CodeReviewer": "Review the implementation for correctness, edge cases, security, and maintainability. Provide actionable fixes.",
            "Summary": "Summarize what was built, key files/modules, and how to run or use it.",
            "Feedback": "Suggest concrete next improvements, optional enhancements, and potential risks.",
        }
    return {
        "ExecutorInstructions":response_content["Executor"],
        "CodeReviewerInstructions":response_content["CodeReviewer"],
        "SummaryInstructions": response_content["Summary"],
        "FeedbackInstructions": response_content["Feedback"]

    }

async def ExecutorAgent(state: State) -> State:
    prompt = state["ExecutorInstructions"]
    logger.logit("INFO", "Executor Agent", "Starting Executor Agent", state)
    previous_executed_code = state.get("previous_executed_code", "")
    user_message = state["user_message"]
    codereview_addon_prompt = f"""{prompt}

User Task:
{user_message}
""" + (
    f"\nPrevious Code Before Code Review Changes:\n{previous_executed_code}\n" if previous_executed_code else ""
) + (
    f"\nCode Review Suggestions on Implementation:\n{state['codereview_suggestions']}\n" if state.get("codereview_suggestions") else ""
) + """
Write only the complete, production-quality code to fulfill the user's request.
Do NOT include explanations, markdown, or any additional text. Return ONLY the code as plain text.
"""
    response = await executor_llm.ainvoke(codereview_addon_prompt)
    _log_agent_llm_response(agent="Executor Agent", response_text=response.content, state=state)
    executor_code = _extract_code_text(response.content)
    if executor_code != (response.content or "").strip():
        logger.logit(
            "INFO",
            "Executor Agent",
            {
                "event": "executor_code_extracted",
                "raw_chars": len((response.content or "").strip()),
                "code_chars": len(executor_code),
            },
            state,
        )
    logger.logit(
        "INFO",
        "Executor Agent",
        {"event": "Executor Agent produced code", "code_chars": len(executor_code)},
        state,
    )
    return {
        "executor_code": executor_code
    }

async def CodeReviewAgent(state: State) -> State:
    prompt = state["CodeReviewerInstructions"]
    user_message = state["user_message"]
    executor_agent_code = state["executor_code"]
    logger.logit("INFO", "Code Review Agent", "Starting Code Review Agent", state)
    codereview_addon_prompt = (
        f"{prompt}\n"
        "Given:\n"
        f"- User Task:\n{user_message}\n"
        f"- ExecutorAgent code output:\n{executor_agent_code}\n"
        "Please provide your code review as a plain string. Do not return JSON, markdown, or any additional formatting. Just return the review text only."
    )
    response = await codereview_llm.ainvoke(codereview_addon_prompt)
    _log_agent_llm_response(agent="Code Review Agent", response_text=response.content, state=state)
    codereview_response = response.content.strip()
    logger.logit(
        "INFO",
        "Code Review Agent",
        {"event": "Code review completed", "review_chars": len(codereview_response)},
        state,
    )
    return {
        "codereview_suggestions": codereview_response
    }

async def SupervisorAgent(state: State) -> State:
    user_message = state["user_message"]
    executor_agent_code = state["executor_code"]
    codereviewagent_analysis = state["codereview_suggestions"]
    logger.logit("INFO", "Supervisor Agent", "Starting Supervisor Agent", state)
    prompt =f"""
    You are the Supervisor Agent.

    Given:
    - User Task
    {user_message}
    - ExecutorAgent code output:
    {executor_agent_code}
    - CodeReviewAgent analysis:
    {codereviewagent_analysis}

    Instructions:
    1. Carefully review the above code output and code review analysis.
    2. Decide if the ExecutorAgent's code fully meets the user's requirements and the feedback from the CodeReviewAgent has been satisfied.
    3. If the code is production-ready and no further changes are required, set "supervisor_succeed": true.
    4. If further work or corrections are needed, set "supervisor_succeed": false.
    5. Return your decision as a JSON object, e.g. {{"supervisor_succeed": true}} or {{"supervisor_succeed": false}}.

    Respond ONLY with the JSON object.
"""
    response = await supervisor_llm.ainvoke(prompt)
    _log_agent_llm_response(agent="Supervisor Agent", response_text=response.content, state=state)
    response_content = _safe_json_loads(response.content, context="Supervisor Agent", state=state)
    supervisor_succeed = bool(response_content.get("supervisor_succeed"))
    logger.logit(
        "INFO",
        "Supervisor Agent",
        {"event": "Supervisor decision", "supervisor_succeed": supervisor_succeed},
        state,
    )
    return {
        "supervisor_succeed":supervisor_succeed
    }

async def SummaryAgent(state: State) -> State:
    prompt = state["SummaryInstructions"]
    user_message = state["user_message"]
    executor_agent_code = state["executor_code"]
    logger.logit("INFO", "Summary Agent", "Starting Summary Agent", state)
    summary_addon_prompt = (
        f"{prompt}\n"
        "Given:\n"
        f"- User Task:\n{user_message}\n"
        f"- ExecutorAgent code output:\n{executor_agent_code}\n"
        "Please provide your answer in the following JSON format: {\"summary_response\": \"\"}\n"
    )
    response = await summary_llm.ainvoke(summary_addon_prompt)
    _log_agent_llm_response(agent="Summary Agent", response_text=response.content, state=state)
    response_content = _safe_json_loads(response.content, context="Summary Agent", state=state)
    summary_response = response_content.get("summary_response", "").strip()
    logger.logit(
        "INFO",
        "Summary Agent",
        {"event": "Summary completed", "summary_chars": len(summary_response)},
        state,
    )
    return {
        "summary_response":summary_response
    }

async def FeedbackAgent(state: State) -> State:
    prompt = state["FeedbackInstructions"]
    user_message = state["user_message"]
    logger.logit("INFO", "Feedback Agent", "Starting Feedback Agent", state)
    feedback_addon_prompt = (
        f"{prompt}\n"
        "Given:\n"
        f"- User Task:\n{user_message}\n"
        "Please provide your answer in the following JSON format: {\"feedback_response\": \"\"}\n"
    )
    response = await feedback_llm.ainvoke(feedback_addon_prompt)
    _log_agent_llm_response(agent="Feedback Agent", response_text=response.content, state=state)
    response_content = _safe_json_loads(response.content, context="Feedback Agent", state=state)
    feedback_response = response_content.get("feedback_response", "").strip()
    logger.logit(
        "INFO",
        "Feedback Agent",
        {"event": "Feedback completed", "feedback_chars": len(feedback_response)},
        state,
    )

    return {
        "feedback_response":feedback_response
    }

async def ResponseAgent(state:State)-> State:
    user_message = state["user_message"]
    executor_agent_code = state["executor_code"]
    summary_response = state["summary_response"]
    feedback_response = state["feedback_response"]
    logger.logit("INFO", "Response Agent", "Starting Response Agent", state)
    prompt =f"""
    You are Response Generator Agent Based on WHole execution of task
    You will have code, You will have summary and feed back so you have to generate proper response while giving whole code perfeclty
    syntax wise as recieved and afte rthat summary and feedback which u will recieved
    # User Task
    {user_message}
    #Code
    {executor_agent_code}
    #Summary of working code
    {summary_response}
    #Feedback of working code
    {feedback_response}
    Return JSON response in format {{"response":""}}
    """

    response = await response_llm.ainvoke(prompt)
    _log_agent_llm_response(agent="Response Agent", response_text=response.content, state=state)
    response_content = _safe_json_loads(response.content, context="Response Agent", state=state).get("response", "").strip()
    logger.logit(
        "INFO",
        "Response Agent",
        {"event": "Final response produced", "response_chars": len(response_content)},
        state,
    )
    return {
        "response":response_content
    }