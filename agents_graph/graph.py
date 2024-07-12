import json
from langchain_core.runnables import RunnableLambda
from langgraph.graph import StateGraph, END
from typing import TypedDict
from langchain_core.messages import HumanMessage
from models.openai_models import get_open_ai_json
from langgraph.checkpoint.sqlite import SqliteSaver
from agents.agents import (
    ConsultantAgent,
    ReporterAgent,
    HealthAnalystAgent
)
from prompts.prompts import (
    consultant_prompt,
    reporter_prompt,
    health_analyst_prompt
)

class AgentGraphState(TypedDict):
    user_input: str
    consultant_response: str
    reporter_response: str
    health_analyst_response: str

def get_agent_graph_state(state: AgentGraphState, state_key: str):
    return state.get(state_key, None)

def create_graph(server=None, model=None, stop=None, model_endpoint=None, temperature=0):
    graph = StateGraph(AgentGraphState)

    graph.add_node(
        "consultant",
        lambda state: ConsultantAgent(
            state=state,
            prompt=consultant_prompt,
            model=model,
            server=server,
            stop=stop,
            model_endpoint=model_endpoint,
            temperature=temperature
        ).provide_support(state["user_input"])
    )

    graph.add_node(
        "reporter",
        lambda state: ReporterAgent(
            state=state,
            prompt=reporter_prompt,
            model=model,
            server=server,
            stop=stop,
            model_endpoint=model_endpoint,
            temperature=temperature
        ).document_incident(state["user_input"])
    )

    graph.add_node(
        "health_analyst",
        lambda state: HealthAnalystAgent(
            state=state,
            prompt=health_analyst_prompt,
            model=model,
            server=server,
            stop=stop,
            model_endpoint=model_endpoint,
            temperature=temperature
        ).analyze_health(state["user_input"])
    )

    graph.add_node("end", lambda state: "End of workflow")

    # Define the edges in the agent graph
    graph.set_entry_point("consultant")
    graph.set_finish_point("end")
    graph.add_edge("consultant", "reporter")
    graph.add_edge("reporter", "health_analyst")
    graph.add_edge("health_analyst", "end")

    return graph

def compile_workflow(graph):
    workflow = graph.compile()
    return workflow
