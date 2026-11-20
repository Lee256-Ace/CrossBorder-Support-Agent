from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # MySQL 数据库连接
    # 格式：mysql+aiomysql://用户名:密码@地址:端口/数据库名
    # aiomysql 是异步 MySQL 驱动，让 FastAPI 不必等待数据库响应
    DATABASE_URL: str = "mysql+aiomysql://app:app123@localhost:3306/crossborder"
    
    # Chroma 向量数据库
    CHROMA_HOST: str = "localhost"
    CHROMA_PORT: int = 8001
    
    # 大语言模型接口配置
    # 默认填的是 OpenAI 官方地址，如果你用其他厂商（比如 DeepSeek），改 BASE_URL 即可
    LLM_API_KEY: str = ""
    LLM_BASE_URL: str = "https://api.openai.com/v1"
    LLM_MODEL: str = "gpt-4o-mini"
    
    # 安全密钥
    # 用于给管理员登录 Token 签名，生产环境必须换成随机长字符串
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    
    # 管理员 Token 有效期（分钟）
    # 480 分钟 = 8 小时，管理员登录后 8 小时内不用重新登录
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480
    
    # MVP 初始管理员账号
    # 启动时自动写入数据库，密码会被哈希存储，不是明文
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "admin123"
    
    # 让 Pydantic 自动读取项目根目录的 .env 文件
    # 如果你创建了 .env 文件，里面的值会覆盖上面的默认值
    class Config:
        env_file = ".env"


# 全局单例：项目中任何地方需要配置，就导入这个 settings
settings = Settings()
