from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from config.settings import elasticsearch_settings as config
from config.logger_config import setup_logger
from typing import List,Optional

class ElasticsearchDB:
    def __init__(self):
        self.logger = setup_logger("logs/database/ES")
        self.url = f"{config.ES_HOST}:{config.ES_PORT}"
        self.user = config.ES_USER
        self.password = config.ES_PASSWORD
        self.index_name = config.ES_INDEX_NAME
        self.connect()

    def connect(self):
        self.client = Elasticsearch(
            hosts=[self.url],
            basic_auth=(self.user, self.password),
            request_timeout=5,
        )
        if not self.client.ping():
            raise ConnectionError(
                f"Failed to connect to Elasticsearch at {self.url}"
            )
    
    def disconnect(self):
        self.client.close()
        self.client = None

    def create_index(self):
        if self.client.indices.exists(self.index_name):
            return
        body = {
            "settings":{
                "number_of_shards": 1,
                "number_of_replicas": 0,
                "analysis":{
                    "analyzer":{
                        "ik_max_word_analyzer":{
                            "type":"custom",
                            "tokenizer":"ik_max_word"
                        },
                        "ik_smart_word_analyzer":{
                            "type":"custom",
                            "tokenizer":"ik_smart"
                        }
                    }
                }
            },
            "mappings":{
                "properties":{
                    "text_id":{"type":"keyword"},
                    "title":{
                        "type": "text",
                        "analyzer": "ik_max_word_analyzer",
                        "search_analyzer": "ik_smart_word_analyzer",
                        "fields": {
                            "keyword": {"type": "keyword"}
                        }
                    },
                    "text":{
                        "type":"text",
                        "analyzer":"ik_max_word_analyzer",
                        "search_analyzer":"ik_smart_word_analyzer"
                    },
                    "source":{"type":"keyword"},
                    "page_num":{"type":"integer"}
                }
            }
        }
        self.client.indices.create(index=self.index_name, body=body)
    
    def insert(self,text_ids,texts,titles,sources,page_nums):
        actions=[]
        for i in range(len(text_ids)):
            actions.append({
                "_index": self.index_name,
                "_id": text_ids[i],
                "_source":{
                    "text_id": text_ids[i],
                    "title": titles[i],
                    "text": texts[i],
                    "source": sources[i],
                    "page_num": page_nums[i]              
                }
            })
        success,_=bulk(self.client, actions)
        return success
    
    def delete_by_source(self,source):
        search_result=self.client.search(
            index=self.index_name,
            body={
                "query":{
                    "term":{
                        "source":source
                    }
                },
                "size":10000,
                "_source":["text_id"]
            }
        )
        deleted_ids = [hit["_source"]["text_id"] for hit in search_result["hits"]["hits"]]
        total_count = search_result["hits"]["total"]["value"]
        if not deleted_ids:
            return{
                "deleted_count":0,
                "deleted_ids":[],
                "total_matched":0
            }
        result = self.client.delete_by_query(
            index=self.index_name,
            body={
                "query":{
                    "term":{
                        "source":source
                    }
                }
            },
            refresh=True
        )
        return{
            "deleted_count":result["deleted"],
            "deleted_ids":deleted_ids[:result["deleted"]],
            "total_matched":total_count
        }
    
    def delete_by_hashsource(self, source_hash: str):
        """根据源文件hash删除ES数据"""
        res = self.client.delete_by_query(
            index=self.index_name,
            body={
                "query": {
                    "prefix": {
                        "text_id": source_hash  # 匹配 "a1b2c3d4_" 开头的所有文档
                    }
                }
            },
            refresh=True
        )
        return res.get("deleted", 0)
    def search(self,queries:List[str],
               top_k:Optional[int]=None,
               source_filter: Optional[List[str]] = None)->List[List[dict]]:
        top_k = top_k or config.TOP_K
        all_results = []
        for query in queries:
            query_body = {
                "query":{
                    "bool":{
                        "must":[
                            {
                                "multi_match":{
                                    "query":query,
                                    "fields":["text","title"],
                                    "type":"best_fields"
                                }
                            }
                        ]
                    }
                },
                "size":top_k,
                "_source":False
            }
            if source_filter:
                query_body["query"]["bool"]["filter"]=[
                    {"terms":{"source":source_filter}}
                ]
            response = self.client.search(
                index=self.index_name,
                body=query_body
            )
            results = []
            for hit in response["hits"]["hits"]:
                results.append({
                    "text_id":hit["_id"],
                    "score":hit["_score"]
                })
            all_results.append(results)
        return all_results
    
    def search_by_ids(self, text_ids: List[str]) -> List[str]:
        """
        根据ID列表从ES中批量检索文档并返回拼接后的字符串列表
        
        Args:
            text_ids (List[str]): 文档ID列表
            
        Returns:
            List[str]: 按输入顺序返回的"title text"格式字符串列表
        """
        if not text_ids:
            return []
        
        try:
            # 构建 mget 请求体
            docs = [{"_index": self.index_name, "_id": tid} for tid in text_ids]
            response = self.client.mget(body={"docs": docs})
            
            # 按顺序处理结果
            results = []
            for doc in response.get("docs", []):
                if doc.get("found"):
                    source = doc["_source"]
                    combined = f"{source.get('title', '')} {source.get('text', '')}".strip()
                    results.append(combined)
                else:
                    results.append("")
                    
            return results
            
        except Exception as e:
            self.logger.error(f"批量检索文档失败: {e}")
            return []    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()