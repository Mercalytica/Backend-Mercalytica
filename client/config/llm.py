from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from config.env import EnvConfig
from api.client import client

env = EnvConfig()
gemini_api_key = env.get("GEMINI_API_KEY")

async def getModel():
    geminiModel = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
        api_key=gemini_api_key  
    )
    
    tools = await client.get_tools()
    geminiAgent = create_agent(geminiModel, tools)
    
    return geminiAgent  