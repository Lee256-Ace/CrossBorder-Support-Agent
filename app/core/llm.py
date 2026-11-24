from langchain_openai import ChatOpenAI
from app.core.config import settings

# 初始化大模型
llm = ChatOpenAI(
    api_key=settings.LLM_API_KEY,
    base_url=settings.LLM_BASE_URL,
    model=settings.LLM_MODEL,
    temperature=0  # 温度设为0，让模型输出最稳定、客观，不乱发散
)