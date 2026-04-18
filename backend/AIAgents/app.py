from fastapi import APIRouter,Request
from pydantic import BaseModel
from .graph import graph
from .models import AutoCodeRequest,APIResponse
app = APIRouter()


@app.post('/autocode_agent')
async def autocode_agent(request: AutoCodeRequest)-> APIResponse:

    user_message = request.user_message


    state = {
        'user_message': user_message
    }

    result_state = await graph.ainvoke(state)
    response= result_state.get('response')

    return APIResponse(response)
