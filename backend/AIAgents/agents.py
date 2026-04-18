import json
from .models import State
from langchain_groq import ChatGroq
from ..config import CONFIG

api_key = CONFIG.get("GROQ_API_KEY")

planner_llm = ChatGroq(model="openai/gpt-oss-120b",api_key=api_key)
executor_llm = ChatGroq(model="openai/gpt-oss-120b",api_key=api_key)
codereview_llm = ChatGroq(model="openai/gpt-oss-120b",api_key=api_key)
supervisor_llm = ChatGroq(model="openai/gpt-oss-120b",api_key=api_key)
summary_llm = ChatGroq(model="openai/gpt-oss-20b",api_key=api_key)
feedback_llm = ChatGroq(model="openai/gpt-oss-20b",api_key=api_key)
response_llm = ChatGroq(model="llama",api_key=api_key)
async def PlannerAgent(state: State) -> State:
    user_message = state['user_message']
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
    response_content = json.loads(response).content

    return {
        "ExecutorInstructions":response_content["Executor"],
        "CodeReviewerInstructions":response_content["CodeReviewer"],
        "SummaryInstructions": response_content["Summary"],
        "FeedbackInstructions": response_content["Feedback"]

    }

async def ExecutorAgent(state: State) -> State:
    prompt = state["ExecutorInstructions"]
    user_message = state["user_message"]
    codereview_addon_prompt = (
        f"{prompt}\n"
        "Given:\n"
        f"- User Task:\n{user_message}\n"
        "Please provide your answer in the following JSON format: {\"executor_code\": \"\"}\n"
    )
    response = await summary_llm.ainvoke(codereview_addon_prompt)
    response_content = json.loads(response)
    executor_code = response_content.content["executor_code"]
    return {
        "executor_code":executor_code
    }

async def CodeReviewAgent(state: State) -> State:
    prompt = state["CodeReviewerInstructions"]
    user_message = state["user_message"]
    executor_agent_code = state["executor_code"]
    codereview_addon_prompt = (
        f"{prompt}\n"
        "Given:\n"
        f"- User Task:\n{user_message}\n"
        f"- ExecutorAgent code output:\n{executor_agent_code}\n"
        "Please provide your answer in the following JSON format: {\"codereview_response\": \"\"}\n"
    )
    response = await summary_llm.ainvoke(codereview_addon_prompt)
    response_content = json.loads(response)
    codereview_response = response_content.content["codereview_response"]
    return {
        "codereview_suggestions":codereview_response
    }

async def SupervisorAgent(state: State) -> State:
    user_message = state["user_message"]
    executor_agent_code = state["executor_code"]
    codereviewagent_analysis = state["codereview_suggestions"]
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
    5. Return your decision as a JSON object, e.g. {"supervisor_succeed": true} or {"supervisor_succeed": false}.

    Respond ONLY with the JSON object.
"""
    response = await supervisor_llm.ainvoke(prompt)
    response_content = json.loads(response).content
    supervisor_succeed = response_content["supervisor_succeed"]
    return {
        "supervisor_succeed":supervisor_succeed
    }

async def SummaryAgent(state: State) -> State:
    prompt = state["SummaryInstructions"]
    user_message = state["user_message"]
    executor_agent_code = state["executor_code"]
    summary_addon_prompt = (
        f"{prompt}\n"
        "Given:\n"
        f"- User Task:\n{user_message}\n"
        f"- ExecutorAgent code output:\n{executor_agent_code}\n"
        "Please provide your answer in the following JSON format: {\"summary_response\": \"\"}\n"
    )
    response = await summary_llm.ainvoke(summary_addon_prompt)
    response_content = json.loads(response)
    summary_response = response_content.content["summary_response"]
    return {
        "summary_response":summary_response
    }

async def FeedbackAgent(state: State) -> State:
    prompt = state["SummaryInstructions"]
    user_message = state["user_message"]
    feedback_addon_prompt = (
        f"{prompt}\n"
        "Given:\n"
        f"- User Task:\n{user_message}\n"
        "Please provide your answer in the following JSON format: {\"feedback_response\": \"\"}\n"
    )
    response = await feedback_llm.ainvoke(feedback_addon_prompt)
    response_content = json.loads(response)
    feedback_response = response_content.content["feedback_response"]
    return {
        "feedback_response":feedback_response
    }

async def ResponseAgent(state:State)-> State:
    user_message = state["user_message"]
    executor_agent_code = state["executor_code"]
    summary_response = state["summary_response"]
    feedback_response = state["feedback_response"]
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

    response = await response_llm.ainovke(prompt)
    response_content = json.load(response).content["response"]
    return {
        "response":response_content
    }