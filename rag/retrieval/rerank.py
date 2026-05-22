import uuid
from typing import List
from config.logger_config import setup_logger 
from rag.retrieval.hybrid_search import HybridSearchPipeline
from models.reranker import SiliconFlowReranker
class RerankPipeline:
    def __init__(self):
        self.logger = setup_logger("logs/pipeline/RerankPipeline")
        self.logger.info("开始初始化rerank pipeline")
        self.hybrid_search = HybridSearchPipeline()
        self.logger.info("hybrid_search 加载完成")
        self.reranker = SiliconFlowReranker()
        self.logger.info("rerank 模型加载完成")
        self.logger.info("rerank pipeline 初始化完成")

    def search_rerank(self, query: str, queries: List[str], steps: list, top_k: int = 5, trace_id: str = None) -> List[str]:
        trace_id = trace_id or str(uuid.uuid4())[:8]
        self.logger.info(f"[{trace_id}]开始rerank，原始查询:{query[:30]}...")

        hybrid_results = self.hybrid_search.retrieve(queries, steps, top_k, trace_id)

        if not hybrid_results:
            self.logger.warning(f"[{trace_id}]搜索无结果，提前结束")
            return []
        self.logger.info(f"[{trace_id}]查询完毕,共:{len(hybrid_results)}条")

        reranked_results = self.reranker.rerank(query, hybrid_results, trace_id)
        if reranked_results:
            self.logger.info(f"[{trace_id}]rerank完毕,最高：{reranked_results[0]['relevance_score']:.2f}|最低{reranked_results[-1]['relevance_score']:.2f}")
            steps.append(f"重排序完成，最高相关性: {reranked_results[0]['relevance_score']:.2f}，最低: {reranked_results[-1]['relevance_score']:.2f}")
            for i, result in enumerate(reranked_results):
                steps.append(f"rerank结果{i+1}: {hybrid_results[result["index"]]}...")
            return [hybrid_results[result["index"]] for result in reranked_results]
        self.logger.warning(f"[{trace_id}]rerank完毕但结果为空")
        steps.append("重排序结果为空，使用原始检索结果")
        return hybrid_results