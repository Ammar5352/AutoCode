from typing import TypedDict

from pydantic import BaseModel

class State(TypedDict):
    user_message: str
    response: str
    ExecuterInstructions:str
    CodeReviewerInstructions:str
    SummaryInstructions:str
    FeedbackInstructions:str
    executor_code:str
    codereview_suggestions:str
    supervisor_succeed:str
    summary_response:str
    feedback_response:str
class AutoCodeRequest(BaseModel):
    user_message:str
class APIResponse(BaseModel):
    response:str