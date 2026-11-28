from functools import lru_cache

from langchain_openai import ChatOpenAI

from app.core.config import settings


@lru_cache(maxsize=1)
def get_llm() -> ChatOpenAI:
    """惰性创建并缓存 LLM 客户端。

    注意：这里故意不在模块导入时实例化 ChatOpenAI。
    底层 openai 客户端在构造时会校验 api_key，若 LLM_API_KEY 未配置，
    模块级实例化会导致 ``import app.core.llm`` 直接抛错，进而让整个
    FastAPI 服务无法启动——即便本次请求根本不需要调用 LLM。

    改为懒加载后：
      - 服务在无 Key 环境下也能正常启动（健康检查、订单查询等非 LLM 路由可用）；
      - 只有真正调用 LLM 时才会创建客户端；
      - lru_cache 保证同一进程内只创建一次，避免重复构造开销。

    用法：
        from app.core.llm import get_llm
        llm = get_llm()
        await llm.ainvoke(...)
    """
    if not settings.LLM_API_KEY:
        raise RuntimeError(
            "LLM_API_KEY 未配置。请在项目根目录创建 .env（可参考 .env.example），"
            "或设置环境变量 LLM_API_KEY 后再调用 LLM 功能。"
        )
    return ChatOpenAI(
        api_key=settings.LLM_API_KEY,
        base_url=settings.LLM_BASE_URL,
        model=settings.LLM_MODEL,
        temperature=0,  # 温度设为0，让模型输出最稳定、客观，不乱发散
    )