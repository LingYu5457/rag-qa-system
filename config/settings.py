import os
from dotenv import load_dotenv

load_dotenv()

class RAGSettings:
    CHUNK_SIZE=int(os.getenv("CHUNK_SIZE", "500"))
    CHUNK_OVERLAP=int(os.getenv("CHUNK_OVERLAP", "0"))

class ModelSettings:
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
    DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-v4-flash")

    SILICONFLOW_API_KEY=os.getenv("SILICONFLOW_API_KEY")
    SILICONFLOW_EMBEDDING_BASE_URL=os.getenv("SILICONFLOW_EMBEDDING_BASE_URL", "https://api.siliconflow.com/v1/embeddings")
    SILICONFLOW_EMBEDDING_MODEL=os.getenv("SILICONFLOW_EMBEDDING_MODEL", "BAAI/bge-large-zh-v1.5")
    EMBEDDING_DIM=int(os.getenv("EMBEDDING_DIM", "1024"))
    SILICONFLOW_RERANKER_BASE_URL=os.getenv("SILICONFLOW_RERANKER_BASE_URL", "https://api.siliconflow.com/v1/rerank")
    SILICONFLOW_RERANKER_MODEL=os.getenv("SILICONFLOW_RERANKER_MODEL", "siliconflow/siliconflow-reranker-large")

class MilvusSettings:
    MILVUS_HOST=os.getenv("MILVUS_HOST")
    MILVUS_PORT=os.getenv("MILVUS_PORT")

    MILVUS_DB_NAME=os.getenv("MILVUS_DB_NAME")
    MILVUS_COLLECTION_NAME=os.getenv("MILVUS_COLLECTION_NAME")
    
    METRIC_TYPE=os.getenv("METRIC_TYPE", "IP")
    TOP_K=int(os.getenv("TOP_K", "5"))
    EMBEDDING_DIM=int(os.getenv("EMBEDDING_DIM", "1024"))

class ElasticsearchSettings:
    ES_HOST=os.getenv("ES_HOST", "http://127.0.0.1")
    ES_PORT=os.getenv("ES_PORT", "9200")
    ES_USER=os.getenv("ES_USER", "")
    ES_PASSWORD=os.getenv("ES_PASSWORD", "")
    ES_INDEX_NAME=os.getenv("ES_INDEX_NAME", "rag_text")

class MysqlSettings:
    MYSQL_HOST=os.getenv("MYSQL_HOST")
    MYSQL_PORT=os.getenv("MYSQL_PORT")

    MYSQL_USER=os.getenv("MYSQL_USER")
    MYSQL_PASSWORD=os.getenv("MYSQL_PASSWORD")
    MYSQL_DB_NAME=os.getenv("MYSQL_DB_NAME")
    MYSQL_DB_CHARSET=os.getenv("MYSQL_DB_CHARSET", "utf8mb4")

    MYSQL_TABLE_USER=os.getenv("MYSQL_TABLE_USER")
    MYSQL_TABLE_SESSION=os.getenv("MYSQL_TABLE_SESSION")
    MYSQL_TABLE_CHAT=os.getenv("MYSQL_TABLE_CHAT")
    MYSQL_TABLE_FILE=os.getenv("MYSQL_TABLE_FILE")

class TortoisSettiongs:
    TORTOISE_CONFIG = {
        "connections": {
            "default": {
                "engine": "tortoise.backends.mysql",
                "credentials": {
                    "host": os.getenv("MYSQL_HOST"),
                    "port": os.getenv("MYSQL_PORT"),
                    "user": os.getenv("MYSQL_USER"),
                    "password": os.getenv("MYSQL_PASSWORD"),
                    "database": os.getenv("MYSQL_DB_NAME"),
                    "charset": os.getenv("MYSQL_DB_CHARSET", "utf8mb4"),
                }
            }
        },
        "apps": {
            "models": {
                "models": [
                    "database.models",
                    "aerich.models"
                ],
                "default_connection": "default",
            }
        }
    }

rag_settings = RAGSettings()
model_settings = ModelSettings()
milvus_settings = MilvusSettings()
elasticsearch_settings = ElasticsearchSettings()
mysql_settings = MysqlSettings()
tortoise_settings = TortoisSettiongs()