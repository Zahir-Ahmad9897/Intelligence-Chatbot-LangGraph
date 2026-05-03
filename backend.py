import os
import requests
from dotenv import load_dotenv
load_dotenv()
os.environ["LANGCHAIN_PROJECT"] = "Smart Chatbot"

from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_groq import ChatGroq
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

from langgraph.graph import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool

from pydantic import BaseModel, Field
from langchain_core.messages import SystemMessage

# -------------------------
# Define Tools
# -------------------------
@tool
def search(query: str) -> str:
    """
    Search the internet for current events, weather, or general knowledge.
    """
    ddg = DuckDuckGoSearchRun(region="us-en")
    return ddg.run(query)

@tool
def calculator(first_num: float, second_num: float, operation: str) -> dict:
    """
    Execute basic math operations: 'add', 'sub', 'mul', 'div'.
    """
    try:
        if operation == "add": return {"result": first_num + second_num}
        if operation == "sub": return {"result": first_num - second_num}
        if operation == "mul": return {"result": first_num * second_num}
        if operation == "div":
            if second_num != 0: return {"result": first_num / second_num}
            return {"error": "Division by zero"}
        return {"error": "Invalid operation"}
    except Exception as e:
        return {"error": str(e)}

@tool
def get_stock_price(symbol: str) -> dict:
    """
    Get the latest stock price for a ticker symbol (e.g., AAPL).
    """
    API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
    if not API_KEY:
        return {"error": "Alpha Vantage API key not found in environment"}
    
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol.upper()}&apikey={API_KEY}"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        quote = data.get("Global Quote", {})
        if not quote: return {"error": f"No data found for {symbol}"}
        return {
            "symbol": quote.get("01. symbol"),
            "price": quote.get("05. price"),
            "change": quote.get("09. change"),
        }
    except Exception as e:
        return {"error": str(e)}

tools = [get_stock_price, search, calculator]

# -------------------------
# Define State and LLM
# -------------------------
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.1
)
llm_with_tools = llm.bind_tools(tools)

# -------------------------
# Define Nodes
# -------------------------
def Chat_node(state: ChatState):
    messages = state['messages']
    response = llm_with_tools.invoke(messages)
    return {'messages': [response]}

tool_node = ToolNode(tools)

# -------------------------
# Setup Persistence
# -------------------------
connection = sqlite3.connect(r"D:\AgenticAI-LangGraph-projects\Chatbot\database.db", check_same_thread=False)
checkpointer = SqliteSaver(conn=connection)

# -------------------------
# Build Graph
# -------------------------
graph = StateGraph(ChatState)

graph.add_node('Chat_node', Chat_node)
graph.add_node('tools', tool_node)

graph.add_edge(START, 'Chat_node')
graph.add_conditional_edges('Chat_node', tools_condition)
graph.add_edge('tools', 'Chat_node')

chatbot = graph.compile(checkpointer=checkpointer)

if __name__ == "__main__": 
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT DISTINCT thread_id FROM checkpoints")
        all_threads = [row[0] for row in cursor.fetchall()]
    except sqlite3.OperationalError:
        all_threads = []

    print("number of unique threads:", len(all_threads))
    config = {"configurable": {"thread_id": "test-thread-tools"}}
    response = chatbot.invoke({'messages': [HumanMessage(content="What is the stock price of TSLA?")]}, config=config)
    print(response['messages'][-1].content)
