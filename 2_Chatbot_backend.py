from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Annotated
from langchain_core.messages import BaseMessage,HumanMessage
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

# new import for memory feature
from langgraph.checkpoint.memory import InMemorySaver
load_dotenv()

from langgraph.graph import add_messages
from typing import TypedDict,Annotated
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


checkpointer = InMemorySaver()
graph = StateGraph(ChatState)
# add nodes
graph.add_node('Chat_node' , Chat_node)
# add edges
graph.add_edge(START , 'Chat_node')
graph.add_edge('Chat_node' , END)
chatbot = graph.compile(checkpointer=checkpointer)

if __name__ == "__main__":
    config = {"configurable": {"thread_id": "test_thread"}}
    response = chatbot.invoke({'messages' : [HumanMessage(content="Hello")]}, config=config)
    print(response)
