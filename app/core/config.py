from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    # 1. 数据库连接：已替换为 PostgreSQL (asyncpg 驱动)
    DATABASE_URL: str = "postgresql+asyncpg://app:app123@localhost:5432/crossborder"
    
    # 2. Chroma 向量数据库
    CHROMA_HOST: str = "localhost"
    CHROMA_PORT: int = 8001
    
    # 3. 大语言模型接口配置
    LLM_API_KEY: str = ""
    LLM_BASE_URL: str = "https://api.openai.com/v1"
    LLM_MODEL: str = "gpt-4o-mini"
    
    # 4. 安全密钥 (用于管理员登录)
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480
    
    # 5. MVP 初始管理员账号
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "admin123"
    
    # 使用 Pydantic v2 推荐的写法读取 .env 文件
    model_config = ConfigDict(env_file=".env")

# 全局单例
settings = Settings()