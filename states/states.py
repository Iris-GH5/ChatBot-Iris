from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages


class AgentGraphState(TypedDict):
    user_input: str
    consultant_response: Annotated[list, add_messages]
    reporter_response: Annotated[list, add_messages]
    health_analyst_response: Annotated[list, add_messages]
    end_chain: Annotated[list, add_messages]


def get_agent_graph_state(state: AgentGraphState, state_key: str):
    if state_key == "consultant_all":
        return state["consultant_response"]
    elif state_key == "consultant_latest":
        if state["consultant_response"]:
            return state["consultant_response"][-1]
        else:
            return state["consultant_response"]

    elif state_key == "reporter_all":
        return state["reporter_response"]
    elif state_key == "reporter_latest":
        if state["reporter_response"]:
            return state["reporter_response"][-1]
        else:
            return state["reporter_response"]

    elif state_key == "health_analyst_all":
        return state["health_analyst_response"]
    elif state_key == "health_analyst_latest":
        if state["health_analyst_response"]:
            return state["health_analyst_response"][-1]
        else:
            return state["health_analyst_response"]

    else:
        return None

state = {
    "user_input": "",
    "consultant_response": [],
    "reporter_response": [],
    "health_analyst_response": [],
    "end_chain": []
}
