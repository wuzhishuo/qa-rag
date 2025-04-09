import os
from dotenv import load_dotenv

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
env_path = os.path.join(project_root, '.env')
load_dotenv(dotenv_path=env_path)


# 获取环境变量
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
VECTOR_DB_PATH = "vector_db/faiss_index"
EMBEDDING_MODEL = "text-embedding-3-large"
CHUNK_SIZE = 300
CHUNK_OVERLAP = 50