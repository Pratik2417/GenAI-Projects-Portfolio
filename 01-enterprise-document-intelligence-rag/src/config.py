from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str = ''
    embedding_model: str = 'text-embedding-3-small'
    llm_model: str = 'gpt-4o-mini'
    faiss_index_path: str = './data/faiss_index'
    chunk_size: int = 1000
    chunk_overlap: int = 150
    top_k: int = 4
    similarity_threshold: float = 0.72
    class Config:
        env_file = '.env'

settings = Settings()
