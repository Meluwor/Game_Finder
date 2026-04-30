import operator
import os
from typing import TypedDict, Sequence, Annotated

from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition

load_dotenv()

OPEN_AI_KEY = os.getenv("OPENAI_GTP_KEY")

"""
Tavily  wäre ein web tool
"""
#Todo Tavily acc wäre super
TAVILY_KEY = os.getenv("TAVILY_KEY")


tavily = TavilySearch(
    max_results=5,
    tavily_api_key=TAVILY_KEY
)

model = ChatOpenAI(
    temperature=0,
    model = "gpt-5-mini",
    api_key=OPEN_AI_KEY
)

#TODO hier sollte die RAWG-API mit rein
tools = [tavily]

model_with_tools = model.bind_tools(tools)



# in this class all needed info will be passed to the next node
class AgentState(TypedDict):
    #Basemessage: System,User,Agent
    messages: Annotated[Sequence[BaseMessage], operator.add]


def call_model(state: AgentState):
    print("Calling Model")
    messages = state["messages"]
    response = model_with_tools.invoke(messages)
    return {"messages" : [response]}

work_flow = StateGraph(AgentState)
tool_node=ToolNode(tools)

work_flow.add_node("web",tool_node)
work_flow.add_node("core",call_model)

work_flow.add_edge("web","core")
work_flow.set_entry_point("core")


work_flow.add_conditional_edges(
    "core",
    tools_condition,
    {
        "tools": "web",
        "__end__": END
    }

)

app = work_flow.compile()


def start():
    while True:
        #TODO mal schaun wofür das noch gut ist
        user_prompt = input("What you searching for: ")
        if user_prompt in "xyz":
            print("Program finished.")
            break
        initial_state={
            "messages": [HumanMessage(content=user_prompt)]

        }
        for output in app.stream(initial_state):
            for key, value in output.items():
                print(f"Output from node: {key}")
                for message in value["messages"]:
                    message.pretty_print()
                print("------")


def main():
    print("start")
    start()

if __name__ =="__main__":
    main()