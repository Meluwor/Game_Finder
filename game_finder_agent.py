import json
import operator
import os
from typing import TypedDict, Sequence, Annotated, List

from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, AIMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.runnables import RunnableConfig

from Game_Finder import RAWG_API
from Game_Finder.app import data_manager
from Game_Finder.structured_output import ItemList

load_dotenv()

MAX_AGENT_CALLS = 10
OPEN_AI_KEY = os.getenv("OPENAI_GTP_KEY")

model_for_core = ChatOpenAI(
    temperature=0,
    model="gpt-4o-mini",
    api_key=OPEN_AI_KEY
)
model_for_structured_output = ChatOpenAI(
    temperature=0,
    model="gpt-4o-mini",
    api_key=OPEN_AI_KEY
)


@tool
def call_me_allways(config: RunnableConfig):
    """
    This function has all needed knowledge of this user based on database.
    """
    user_id = config["configurable"]["user_id"]
    user_data = data_manager.get_user_data(user_id)
    print(f"<<<<<<<<<i got a call: {user_id}>>>>>>>>>")
    return user_data


@tool
def connect_to_rawg(item_names: List[str],config: RunnableConfig) -> str:
    """
    This function will allow the LLM to get new game data via the RAWG-API. Just items which are not in database will be returned
    """

    if not item_names:
        return "There are no given names to search for!"
    is_available, message = RAWG_API.prepare_and_check_api()
    if not is_available:
        return "Problem with API: " + message
    user_id = config["configurable"]["user_id"]
    cleaned_names = data_manager.prepare_name_list(user_id,item_names)
    if len(cleaned_names)==0:
        return f"No need to search for this! user knows all theese games allready: {item_names}"
    print("<<<<<<<<<RAWG-CALL>>>>>>>>>")
    print("item_names:", cleaned_names)
    game_data = {}
    # an id to fit the shema
    fake_user_id = -1
    for name in cleaned_names:
        print("-----searching game via rawg-----")

        game_data_from_api = RAWG_API.search_game_by_name(name)
        results = game_data_from_api.get("results")
        if results:
            item_data, genre_data = data_manager.prepare_rawg_data(fake_user_id, results)
            game_data[name] = {"item_data":item_data,
                               "genre_data":genre_data}
        else:
            game_data[name] = {
                "status": "not_found",
                "message": f"Nothing was found by given name: '{name}'."
            }
    return json.dumps(game_data, indent=2)


tools = [call_me_allways, connect_to_rawg]

model_with_tools = model_for_core.bind_tools(tools)


# in this class all needed info will be passed to the next node
class AgentState(TypedDict):
    # BaseMessage: System,User,Agent
    messages: Annotated[Sequence[BaseMessage], operator.add]
    final_output: ItemList


def call_model(state: AgentState):
    print("Calling Model")
    messages = state["messages"]
    response = model_with_tools.invoke(messages)
    return {"messages": [response]}


structured_llm = model_for_structured_output.with_structured_output(ItemList)
def format_output(state: AgentState):
    """
    This node will format the given input to a structured one with the help off a LLM.
    """
    print("checking output")

    prompt = SystemMessage(content=(
        "Du bist ein Extraktions-Assistent. Deine einzige Aufgabe ist es, "
        "Informationen aus dem Kontext in das Schema zu übertragen. "
        "Erfinde NIEMALS Daten."
        "Wenn Daten nicht existieren, lasse die Felder leer oder nutze None."
        "Erstelle keine fiktiven Links."
        "Nutze die letzte Antwort des Beraters für das Feld 'answer_to_user'"
    ))
    messages = state["messages"]
    response = structured_llm.invoke([prompt] + messages)
    print("output generated")
    # Todo speichere hier core antwort und formatter antwort
    return {"messages": [AIMessage(content=response.model_dump_json())]}


work_flow = StateGraph(AgentState)
tool_node = ToolNode(tools)

work_flow.add_node("tool", tool_node)
work_flow.add_node("core", call_model)
work_flow.add_node("formatter", format_output)

work_flow.add_edge("tool", "core")
work_flow.set_entry_point("core")

work_flow.add_conditional_edges(
    "core",
    tools_condition,
    {
        "tools": "tool",
        "__end__": "formatter"
    }

)
work_flow.add_edge("formatter", END)

# RAM based memori
memory = MemorySaver()
app = work_flow.compile(checkpointer=memory)


def chat_bot(user_id, user_content):
    config: RunnableConfig = {"configurable": {"thread_id": f"chating_with_user_:{user_id}",
                                               "user_id": user_id
                                               }}

    system_start_content = (f"""Du bist ein Spieleberater für die Game-Finder-App.
                          Halte dich an folgende Regeln:
                          1.Nutze deine Tools für alle Informationen und erfinde niemals Daten (keine Halluzinationen)!
                          2.Besorge dir alle informationen über den User!
                          3.Berate den User ausschließlich zu Videospielen!
                          4.Biete in jeder Antwort eine passende Spieleempfehlung an.
                          5.Bleib auf dem Laufenden und besorge dir immer das Neuste!
                          6.ABSOLUTES VERBOT: Schlage niemals, unter keinen Umständen, ein Spiel vor, das in der Liste 'already_owned_items' auftaucht. Gleiche jeden Vorschlag erst mit dieser Liste ab!“!
                          7.Nutze die RAWG-API um Informationen zu neuen Spielen zu bekommen.
                          8.Bevor du antwortest, schreibe für dich selbst (intern) einen Abgleich: 'Vorschlag: [Spiel] | In Besitz: [Ja/Nein]'.
                            """)

    start_state = app.get_state(config)
    if not start_state.values.get("messages"):
        app.update_state(config, {"messages": [SystemMessage(content=system_start_content)]})

    initial_state = {"messages": [HumanMessage(content=user_content)]}
    answer = ""
    for output in app.stream(initial_state, config=config):
        for key, value in output.items():
            print(f"Output from node: {key}")
            messages = value.get("messages",[])
            if messages:
                for message in value["messages"]:
                    message.pretty_print()
                    print("------")
                answer=messages[-1].content

    return answer


def start_for_testing():
    config: RunnableConfig = {"configurable": {"thread_id": "lokaler_test_thread"}}
    system_start_content = ("Du bist ein Spieleberater der mit Hilfe seiner Tools über die Game-Finder app wacht. "
                            "Deine Hauptaufgabe besteht darin dem user nur! in Bezug auf Spiele zu beraten")

    start_state = app.get_state(config)
    if not start_state.values.get("messages"):
        app.update_state(config, {"messages": [SystemMessage(content=system_start_content)]})

    calls = 0
    while True:
        if calls == MAX_AGENT_CALLS:
            # TODO hier muss man mal schaun zwecks Token Überwachung
            print("end of calls")
            break
            # TODO ne userinfo wäre angebracht
        calls += 1
        user_prompt = input("What you searching for: ").strip()
        if not user_prompt:
            continue
        if user_prompt in ["x", "y", "z"]:
            print("Program finished.")
            break
        initial_state = {"messages": [HumanMessage(content=user_prompt)]}

        for output in app.stream(initial_state, config=config):
            for key, value in output.items():
                print(f"Output from node: {key}")
                for message in value["messages"]:
                    message.pretty_print()
                print("------")


def main():
    print("start")
    start_for_testing()


if __name__ == "__main__":
    main()
