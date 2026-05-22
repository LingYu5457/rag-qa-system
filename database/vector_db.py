from pymilvus import (
    MilvusClient,utility,DataType
)
from typing import (List,Optional)
from config.settings import milvus_settings as config

class MilvusVectorDB:
    def __init__(self):
        self.url = f"{config.MILVUS_HOST}:{config.MILVUS_PORT}"
        self.db_name=config.MILVUS_DB_NAME
        self.collection_name=config.MILVUS_COLLECTION_NAME
        self.dim = config.EMBEDDING_DIM
        self.metric_type = config.METRIC_TYPE
        self.connect()
        self.create_collection()
    def connect(self):
        """建立数据库连接"""
        self.client = MilvusClient(uri=self.url, timeout=5)
        database = self.client.list_databases()
        if self.db_name not in database:
            self.client.create_database(self.db_name)
        self.client.use_database(self.db_name)
    
    def disconnect(self):
        """断开数据库连接"""
        self.client.close()

    def create_collection(self):
        """创建或加载集合"""
        if self.client.has_collection(self.collection_name):
            self.client.load_collection(self.collection_name)
            return 
        schema = MilvusClient.create_schema()
        schema.add_field(
            field_name="text_id",
            datatype=DataType.VARCHAR,
            max_length=20,
            is_primary=True,
            auto_id=False
        )
        schema.add_field(
            field_name="embedding",
            datatype=DataType.FLOAT_VECTOR,
            dim=self.dim
        )
        index_params = MilvusClient.prepare_index_params()
        index_params.add_index(
            field_name="embedding",
            index_type="IVF_FLAT",
            metric_type=self.metric_type,
            params={
                "nlist": 1024,
            }
        )
        self.client.create_collection(
            collection_name=self.collection_name,
            schema=schema,
            index_params=index_params
        )
    
    def insert(self,text_ids,embeddings,partition_name=None):
        """插入向量数据"""
        data = [
            {"text_id":text_id,"embedding":embedding} 
            for text_id,embedding in zip(text_ids,embeddings)
        ]
        res = self.client.insert(
            collection_name=self.collection_name,
            data=data,
            partition_name=partition_name
        )
        return res.get('insert_count')
    
    def delete_by_id(self,text_ids:List[int]):
        """根据ID删除数据"""
        res=self.client.delete(
            collection_name=self.collection_name,
            ids=text_ids
        )
        return res is not None and res.get('delete_count')==len(text_ids)
    
    def delete_by_hashsource(self, source_hash: str):
        """根据源文件hash删除Milvus数据"""
        res = self.client.delete(
            collection_name=self.collection_name,
            filter=f'text_id like "{source_hash}%"' 
        )
        return res.get('delete_count', 0)

    
    def search(self, query_embeddings: List[List[float]], 
            top_k: Optional[int] = None, 
            partition_names: Optional[List[str]] = None):
        """向量搜索"""
        return self.client.search(
            collection_name=self.collection_name,
            partition_names=partition_names,
            anns_field="embedding",
            data=query_embeddings,
            limit=top_k or config.TOP_K,
            search_params={"metric_type": self.metric_type}
        )

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()