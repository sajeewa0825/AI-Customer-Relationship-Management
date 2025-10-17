# app/services/mcp_client.py
import os
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from app.core.config import Settings
from app.services.embedding.embedding_service import retrieve_company_context
import sys


load_dotenv()


async def run_rag_query(user_prompt: str, history: list, system_prompt: str):
    """
    MCP-enabled version of run_rag_query()
    - Loads company context (RAG)
    - Connects to MCP tools
    - Runs reasoning agent with Groq model
    """

    # 1️⃣ Retrieve company context
    context = retrieve_company_context(user_prompt)

    # 2️⃣ Initialize MCP client (connects to your MCP tools)
    client = MultiServerMCPClient(
        {
            "ownerDetails": {
                "command": sys.executable,
                "args": ["app/services/ai/tools/test_tool.py"],
                "transport": "stdio",
            },
            "productDetails": {
                "command": sys.executable,
                "args": ["app/services/ai/tools/product_tool.py"],
                "transport": "stdio",
            },
        }
    )

    # 3️⃣ Load tools dynamically from MCP servers
    tools = await client.get_tools()

    # 4️⃣ Initialize Groq model
    os.environ["GROQ_API_KEY"] = Settings.GROQ_API_KEY
    model = ChatGroq(
        model=Settings.MODEL_NAME,
        temperature=Settings.TEMPERATURE,
        max_tokens=Settings.MAX_TOKENS,
        api_key=Settings.GROQ_API_KEY,
    )

    # 5️⃣ Create ReAct agent (LangGraph agent)
    agent = create_react_agent(model, tools)

    # 6️⃣ Build system + chat history
    messages = [{"role": "system", "content": f"{system_prompt}\n\nContext:\n{context}"}]
    for msg in history:
        messages.append({"role": "user", "content": msg["user_prompt"]})
        messages.append({"role": "assistant", "content": msg["ai_response"]})
    messages.append({"role": "user", "content": user_prompt})

    # 7️⃣ Run the agent
    response = await agent.ainvoke({"messages": messages})

    # 8️⃣ Extract and return final AI reply
    ai_reply = response["messages"][-1].content
    return ai_reply

