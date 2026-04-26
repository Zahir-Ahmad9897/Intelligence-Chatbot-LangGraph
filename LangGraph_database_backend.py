from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Annotated
from langchain_core.messages import BaseMessage,HumanMessage
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langgraph.checkpoint.sqlite import SqliteSaver
import os
import sqlite3
load_dotenv()

from langgraph.graph import add_messages

class ChatState(TypedDict):
    messages : Annotated[list[BaseMessage],add_messages]


llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.7
)
def Chat_node(state : ChatState):
    messages = state['messages']
    response = llm.invoke(messages)
    return {'messages' : response}


connection = sqlite3.connect(r"D:\AgenticAI-LangGraph-projects\Chatbot\database.db",check_same_thread=False)
checkpointer = SqliteSaver(conn=connection)



graph = StateGraph(ChatState)
# add nodes
graph.add_node('Chat_node' , Chat_node)
# add edges
graph.add_edge(START , 'Chat_node')
graph.add_edge('Chat_node' , END)
chatbot = graph.compile(checkpointer=checkpointer)

if __name__ == "__main__": 
    # calculate number of unique threads
    cursor = connection.cursor()
    # Ensure table exists before querying (though SqliteSaver usually handles this)
    try:
        cursor.execute("SELECT DISTINCT thread_id FROM checkpoints")
        all_threads = [row[0] for row in cursor.fetchall()]
    except sqlite3.OperationalError:
        all_threads = []

    print("number of unique threads:",len(all_threads))
    config = {"configurable": {"thread_id": "thread-1"}}
    response = chatbot.invoke({'messages' : [HumanMessage(content="what is my name")]}, config=config)
    print(response['messages'][-1].content)
