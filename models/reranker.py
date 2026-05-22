import requests
import uuid
from typing import List
from config.settings import model_settings as config
from config.logger_config import setup_logger

class SiliconFlowReranker:
    def __init__(self):
        self.logger = setup_logger("logs/models/SiliconFlowReranker")
        self.logger.info("开始初始化 rerank模型")
        self.url = config.SILICONFLOW_RERANKER_BASE_URL
        self.headers = {
            "Authorization": f"Bearer {config.SILICONFLOW_API_KEY}",
            "Content-Type": "application/json"
        }
        self.model = config.SILICONFLOW_RERANKER_MODEL
        self.timeout = 30
        self.logger.info("rerank模型 初始化完成")

    def rerank(self,query:str,documents:List[str],trace_id:str = None) -> List[dict]:
        trace_id = trace_id or str(uuid.uuid4())[:8]
        self.logger.info(f"[{trace_id}]开始rerank | query={query[:50]}... | docs数量={len(documents)}")
        if not query or not documents:
            self.logger.warning("query 或 documents 为空")
            return []
        
        payload = {
            "model": self.model,
            "query": query,
            "documents": documents
        }
        try:
            response = requests.post(
                self.url, 
                json=payload, 
                headers=self.headers, 
                timeout=self.timeout
            )

            if response.status_code != 200:
                self.logger.error(f"[{trace_id}]API 错误状态码 {response.status_code}: {response.text}")
                return []
            
            result = response.json()
            results = result.get("results", [])
            if results:
                top_scores = [f"{r.get('index')}:{r.get('relevance_score'):.4f}" for r in results[:3]]
                self.logger.info(f"[{trace_id}] Rerank成功 | 结果数={len(results)} | top分数=[{', '.join(top_scores)}]")
            else:
                self.logger.warning(f"[{trace_id}] Rerank成功但无结果")
            return results
        
        except requests.exceptions.Timeout:
            self.logger.error(f"[{trace_id}]Rerank 请求超时 | timeout={self.timeout}s | query={query[:50]}...")
            return []
        except (KeyError, IndexError, ValueError) as e:
            self.logger.error(f"[{trace_id}]Rerank 响应解析失败 | 错误={e} | 原始响应={response.text[:300]}")
            return []
        except requests.exceptions.RequestException as e:
            self.logger.error(f"[{trace_id}]Rerank 请求异常 | 错误={e} | query={query[:50]}...")
            return []