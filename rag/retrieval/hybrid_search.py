from typing import List, Dict, Any, Optional
import time
from uuid import uuid4
from config.logger_config import setup_logger
from database.text_db import ElasticsearchDB
from database.vector_db import MilvusVectorDB
from models.embedding import SiliconFlowEmbedding

class HybridSearchPipeline:
    def __init__(self):
        self.logger = setup_logger("logs/pipeline/HybridSearch")
        self.logger.info("开始初始化 hybrid_search pipeline")

        self.embedding = SiliconFlowEmbedding()
        self.logger.info("Embedding模型 加载完成")

        try:
            self.sparse_retriever: Optional[ElasticsearchDB] = ElasticsearchDB()
            self.logger.info("ES数据库 加载完成")
        except Exception as e:
            self.logger.warning(f"ES 初始化失败（检索将跳过BM25）: {e}")
            self.sparse_retriever = None

        try:
            self.vector_retriever: Optional[MilvusVectorDB] = MilvusVectorDB()
            self.logger.info("Milvus数据库 加载完成")
        except Exception as e:
            self.logger.warning(f"Milvus 初始化失败（检索将跳过向量检索）: {e}")
            self.vector_retriever = None

        if self.sparse_retriever is None and self.vector_retriever is None:
            self.logger.warning("ES 和 Milvus 均不可用，检索功能不可用")

        self.logger.info("hybrid_search pipeline 初始化完成")

    def retrieve(self, querys: List[str], steps: list, top_k: int = 5, trace_id: str = None) -> List[str]:
        """
        混合查询

        Args:
            querys (List[str]): 查询列表
            steps (list): 步骤收集列表
            top_k (int, optional): 检索数量. Defaults to 5.

        Returns:
            List[str]: 最终文档列表
        """
        trace_id = trace_id or str(uuid4())[:8]
        start_time = time.time()

        self.logger.info(f"[{trace_id}]开始检索：{len(querys)}个查询，top_k={top_k}")
        if not querys:
            self.logger.warning(f"[{trace_id}] 接收到空查询")
            steps.append("混合检索: 空查询，跳过")
            return []

        try:
            # 获取查询向量
            query_embeddings = self.embedding.embed_batch(querys)
            query_embeddings = [e for e in query_embeddings if e is not None]
            self.logger.debug(f"[{trace_id}] 生成{len(query_embeddings)}个向量")
            steps.append(f"查询向量生成: {len(query_embeddings)}个")

            # 并行检索（只调用可用的检索器）
            bm25_results = self.sparse_retriever.search(querys, top_k=top_k) if self.sparse_retriever else []
            vector_results = self.vector_retriever.search(query_embeddings, top_k=top_k) if self.vector_retriever else []
            bm25_count = sum(len(r) for r in bm25_results) if bm25_results else 0
            vector_count = sum(len(r) for r in vector_results) if vector_results else 0
            self.logger.info(f"[{trace_id}] 检索完成，BM25:{bm25_count}，向量:{vector_count}")
            steps.append(f"BM25检索: {bm25_count}条，向量检索: {vector_count}条")

            # 如果只有一个检索器可用，直接使用其结果
            if not self.sparse_retriever and self.vector_retriever:
                # 只返回向量检索结果
                ids_list = [[x["text_id"] for x in vr] for vr in vector_results]
                final_ids = self.rrf_merge(ids_list)
            elif self.sparse_retriever and not self.vector_retriever:
                # 只返回 BM25 结果
                ids_list = [[x["text_id"] for x in br] for br in bm25_results]
                final_ids = self.rrf_merge(ids_list)
            elif not self.sparse_retriever and not self.vector_retriever:
                self.logger.warning(f"[{trace_id}] 无可用检索器")
                steps.append("无可用检索器")
                return []
            else:
                # 每个查询内部RRF融合
                self.logger.debug(f"[{trace_id}] 开始RRF融合，共{len(querys)}个查询")
                ids_list = []
                for i in range(len(querys)):
                    bm25_ids = [x["text_id"] for x in bm25_results[i]]
                    vector_ids = [x["text_id"] for x in vector_results[i]]
                    ids = self.rrf_merge([bm25_ids, vector_ids])
                    ids_list.append(ids[:min(len(ids), (top_k + 2))])
                    if (i + 1) % 10 == 0:
                        self.logger.info(f"[{trace_id}] RRF融合进度: {i + 1}/{len(querys)}")
                self.logger.info(f"所有query融合完成，共{len(ids_list)}个结果")

                # 跨查询RRF融合
                final_ids = self.rrf_merge(ids_list)
                self.logger.info(f"跨query融合完成，共{len(final_ids)}个结果")

            # 多取一些
            final_count = min(
                len(final_ids),
                (top_k + len(querys) * 2)
            )

            # 用text_db根据ID获取内容
            if self.sparse_retriever:
                result = self.sparse_retriever.search_by_ids(final_ids[:final_count])
            else:
                # 如果ES不可用，只能返回ID列表（实际不应该到这里）
                self.logger.warning(f"[{trace_id}] ES不可用，无法根据ID获取文本")
                result = []

            elapsed = (time.time() - start_time) * 1000
            self.logger.info(f"[{trace_id}] 检索完成，返回{len(result)}条，耗时{elapsed:.2f}ms")
            steps.append(f"RRF融合完成，最终返回{len(result)}条，耗时{elapsed:.0f}ms")
            return result
        except Exception as e:
            self.logger.error(f"[{trace_id}] 检索失败：{e}")
            steps.append(f"检索异常: {e}")
            return []


    def rrf_merge(self, mergelist: List[List[Any]], k: int = 60) -> List[Any]:
        """
        RRF融合

        Args:
            mergelist (List[List[Any]]): 待融合列表
            k (int, optional): RRF参数，控制排名的影响程度. Defaults to 60.

        Returns:
            List[Any]: 融合后的排序列表
        """
        if not mergelist:
            return []
        scores: Dict[Any, float] = {}
        # 计算RRF分数
        for rank_list in mergelist:
            for rank, item in enumerate(rank_list, start=1):
                score = 1.0 / (k + rank)
                scores[item] = scores.get(item, 0) + score
        # 排序并返回
        sorted_items = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [item for item, score in sorted_items]
