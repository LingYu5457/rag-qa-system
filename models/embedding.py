import requests
import uuid
from typing import List
from config.settings import model_settings as config
from config.logger_config import setup_logger

class SiliconFlowEmbedding:
    def __init__(self):
        self.logger = setup_logger("logs/models/SiliconFlowEmbedding")
        self.logger.info("开始初始化embedding模型")
        self.url = config.SILICONFLOW_EMBEDDING_BASE_URL
        self.headers = {
            "Authorization": f"Bearer {config.SILICONFLOW_API_KEY}",
            "Content-Type": "application/json"
        }
        self.model = config.SILICONFLOW_EMBEDDING_MODEL
        self.timeout = 30
        self.logger.info("embedding模型 初始化完成")

    def embed(self, text: str, trace_id: str = None) -> List[float]:
        trace_id = trace_id or str(uuid.uuid4())[:8]
        self.logger.info(f"[{trace_id}] 开始embed | text长度={len(text)}")
        
        if not text:
            self.logger.warning(f"[{trace_id}] text为空，跳过embed")
            return []
        
        payload = {
            "model": self.model,
            "input": text
        }
        try:
            response = requests.post(
                self.url,
                json=payload,
                headers=self.headers,
                timeout=self.timeout
            )
            
            if response.status_code != 200:
                self.logger.error(
                    f"[{trace_id}] API错误 | 状态码={response.status_code} | "
                    f"text={text[:50]}... | 响应={response.text[:200]}"
                )
                return []
            
            result = response.json()
            embedding = result['data'][0]['embedding']
            self.logger.info(f"[{trace_id}] Embed成功 | 向量维度={len(embedding)}")
            return embedding
            
        except requests.exceptions.Timeout:
            self.logger.error(f"[{trace_id}] Embed超时 | timeout={self.timeout}s | text={text[:50]}...")
            return []
        except (KeyError, IndexError, ValueError) as e:
            self.logger.error(f"[{trace_id}] Embed响应解析失败 | 错误={e} | 响应={response.text[:300]}")
            return []
        except requests.exceptions.RequestException as e:
            self.logger.error(f"[{trace_id}] Embed请求异常 | 错误={e} | text={text[:50]}...")
            return []


    BATCH_SIZE = 64

    def _embed_chunk(self, texts: List[str], trace_id: str) -> List[List[float]]:
        payload = {
            "model": self.model,
            "input": texts
        }
        response = requests.post(
            self.url,
            json=payload,
            headers=self.headers,
            timeout=60
        )

        if response.status_code != 200:
            self.logger.error(
                f"[{trace_id}] Batch API错误 | 状态码={response.status_code} | "
                f"文本数={len(texts)} | 响应={response.text[:200]}"
            )
            return [None] * len(texts)

        result = response.json()
        return [item['embedding'] for item in result['data']]

    def embed_batch(self, texts: List[str], trace_id: str = None) -> List[List[float]]:
        trace_id = trace_id or str(uuid.uuid4())[:8]
        self.logger.info(f"[{trace_id}] 开始batch embed | 文本数={len(texts)}")

        if not texts:
            self.logger.warning(f"[{trace_id}] texts为空，跳过batch embed")
            return []

        all_embeddings: List[List[float]] = []
        for i in range(0, len(texts), self.BATCH_SIZE):
            chunk = texts[i:i + self.BATCH_SIZE]
            try:
                chunk_result = self._embed_chunk(chunk, trace_id)
                all_embeddings.extend(chunk_result)
            except requests.exceptions.Timeout:
                self.logger.error(f"[{trace_id}] Batch embed超时 | 分片{i // self.BATCH_SIZE}")
                all_embeddings.extend([None] * len(chunk))
            except (KeyError, IndexError, ValueError) as e:
                self.logger.error(f"[{trace_id}] Batch embed解析失败 | 分片{i // self.BATCH_SIZE} | 错误={e}")
                all_embeddings.extend([None] * len(chunk))
            except requests.exceptions.RequestException as e:
                self.logger.error(f"[{trace_id}] Batch embed请求异常 | 分片{i // self.BATCH_SIZE} | 错误={e}")
                all_embeddings.extend([None] * len(chunk))

        self.logger.info(
            f"[{trace_id}] Batch embed完成 | 结果数={len(all_embeddings)} | "
            f"有效={sum(1 for e in all_embeddings if e is not None)}"
        )
        return all_embeddings