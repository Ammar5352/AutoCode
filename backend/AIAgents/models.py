from typing import Any, List, TypedDict

from pydantic import BaseModel

class State(TypedDict):
    user_message: str
    response: str
    ExecutorInstructions: str
    CodeReviewerInstructions:str
    SummaryInstructions:str
    FeedbackInstructions:str
    executor_code:str
    codereview_suggestions:str
    supervisor_succeed: bool
    summary_response:str
    feedback_response:str
    previous_executed_code: str
    logs: List[dict[str, Any]]
class AutoCodeRequest(BaseModel):
    user_message:str
class APIResponse(BaseModel):
    response:str
    task_code:str
    summary:str
    feedback:str