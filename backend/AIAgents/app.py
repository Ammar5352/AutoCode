from fastapi import APIRouter,Request
from .graph import graph
from .models import AutoCodeRequest,APIResponse
from .logger import logger
app = APIRouter()


@app.post('/autocode_agent')
async def autocode_agent(request: AutoCodeRequest)-> APIResponse:

    user_message = request.user_message

    logger.logit("INFO", "API", {"event": "request_received", "user_message_chars": len(user_message)})

    state = {
        "user_message": user_message,
        "previous_executed_code": "",
        "codereview_suggestions": "",
        "executor_code": "",
        "summary_response": "",
        "feedback_response": "",
        "logs": [],
    }

    result_state = await graph.ainvoke(state)
    response= result_state.get('response')
    task_code = result_state.get('executor_code')
    summary = result_state.get('summary_response') or ""
    feedback= result_state.get('feedback_response') or ""
    logger.logit("INFO", "API", {"event": "final_response_ready", "response_chars": len(response or "")}, result_state)

    return APIResponse(
        response=response or "",
        task_code=task_code or "",
        summary=summary,
        feedback=feedback,
    )
