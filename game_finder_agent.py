import operator
import os
from typing import TypedDict, Sequence, Annotated

from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
#from langchain_tavily import TavilySearch
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver


load_dotenv()

MAX_AGENT_CALLS = 10
OPEN_AI_KEY = os.getenv("OPENAI_GTP_KEY")

"""
Tavily  wäre ein web tool
"""
"""
#Todo Tavily acc wäre super
TAVILY_KEY = os.getenv("TAVILY_KEY")


tavily = TavilySearch(
    max_results=5,
    tavily_api_key=TAVILY_KEY
)
"""
model = ChatOpenAI(
    temperature=0,
    model="gpt-4o-mini",
    api_key=OPEN_AI_KEY
)




@tool
def call_me_allways():
    """
    This function has all needed knowledge of the database.
    """
    # TODO llm greift darauf zu mal schaun wie weit
    print("<<<<<<<<<i got a call>>>>>>>>>")
    return "never call me again"


@tool
def connect_to_rawg():
    """
    This function will allow the LLM to get specific game data via the RAWG-API
    """
    # TODO hier sollte die RAWG-API mit rein
    print("<<<<<<<<<RAWG-CALL>>>>>>>>>")
    return "calling API"


tools = [call_me_allways, connect_to_rawg]

model_with_tools = model.bind_tools(tools)


# in this class all needed info will be passed to the next node
class AgentState(TypedDict):
    # Basemessage: System,User,Agent
    messages: Annotated[Sequence[BaseMessage], operator.add]


def call_model(state: AgentState):
    print("Calling Model")
    messages = state["messages"]
    response = model_with_tools.invoke(messages)
    return {"messages": [response]}


work_flow = StateGraph(AgentState)
tool_node = ToolNode(tools)

work_flow.add_node("tool", tool_node)
work_flow.add_node("core", call_model)

work_flow.add_edge("tool", "core")
work_flow.set_entry_point("core")

work_flow.add_conditional_edges(
    "core",
    tools_condition,
    {
        "tools": "tool",
        "__end__": END
    }

)
#RAM based memori
memory = MemorySaver()
app = work_flow.compile(checkpointer=memory)


def start():
    #TODO die id sollte angepasst werden
    config = {"configurable": {"thread_id": "lokaler_test_thread"}}
    system_start_content = ("Du bist ein Spieleberater der mit Hilfe seiner Tools über die Game-Finder app wacht. "
                            "Deine Hauptaufgabe besteht darin dem user nur! in Bezug auf Spiele zu beraten")
    calls = 0
    while True:
        if calls == MAX_AGENT_CALLS:
            print("end of calls")
            break
            #TODO ne userinfo wäre angebracht
        calls += 1
        # TODO mal schaun wofür das noch gut ist
        user_prompt = input("What you searching for: ").strip()
        if not user_prompt:
            continue
        if user_prompt in ["x", "y", "z"]:
            print("Program finished.")
            break
        initial_state = {
            "messages": [SystemMessage(content=system_start_content),
                         HumanMessage(content=user_prompt)
                         ]
        }
        for output in app.stream(initial_state, config=config):
            for key, value in output.items():
                print(f"Output from node: {key}")
                for message in value["messages"]:
                    message.pretty_print()
                print("------")


def main():
    print("start")
    start()


if __name__ == "__main__":
    main()
