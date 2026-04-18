from langgraph.graph import StateGraph, START, END
from .models import State
from .agents import PlannerAgent,ExecutorAgent,CodeReviewAgent,SummaryAgent,FeedbackAgent,SupervisorAgent,ResponseAgent
graph_builder = StateGraph(State)

async def should_continue(state:State):
    if state.get("supervisor_succeed"):
        return "SummaryAgent"
    else:
        return "ExecutorAgent"

graph_builder.add_edge(START, "PlannerAgent")
graph_builder.add_node("PlannerAgent", PlannerAgent)
graph_builder.add_node("ExecutorAgent", ExecutorAgent)
graph_builder.add_node("CodeReviewAgent", CodeReviewAgent)
graph_builder.add_node("SupervisorAgent",SupervisorAgent)
graph_builder.add_node("SummaryAgent", SummaryAgent)
graph_builder.add_node("FeedbackAgent", FeedbackAgent)
graph_builder.add_node("ResponseAgent",ResponseAgent)

graph_builder.add_edge("PlannerAgent","ExecutorAgent")
graph_builder.add_edge("ExecutorAgent","CodeReviewAgent")
graph_builder.add_edge("CodeReviewAgent","SupervisorAgent")


graph_builder.add_conditional_edges(
    "SupervisorAgent",
    should_continue,
    {"ExecutorAgent":"ExecutorAgent", "SummaryAgent":"SummaryAgent"}
)
graph_builder.add_edge("SummaryAgent","FeedbackAgent")
graph_builder.add_edge("FeedbackAgent","ResponseAgent")
graph_builder.add_edge("ResponseAgent",END)


graph = graph_builder.compile()