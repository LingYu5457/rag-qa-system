import uuid
from typing import List, Generator, Dict
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

from config.logger_config import setup_logger
from models.llm import get_chat_llm_deepseek, get_chat_llm_local
from rag.generation.user_intent import IntentRouterPipeline
from rag.generation.query_process import QueryRewriterPipeline
from rag.retrieval.rerank import RerankPipeline

INTENT_CONFIG: Dict[str, dict] = {
    'search_precise': {'top_k': 3, 'max_rewrite_queries': 3},
    'search_broad':  {'top_k': 8, 'max_rewrite_queries': 5},
    'search_deep':   {'top_k': 12, 'max_rewrite_queries': 7},
    'chat':          {'top_k': 0, 'max_rewrite_queries': 0},
}


class ChatPipeline:
    def __init__(self, use_local_llm: bool = False):
        self.logger = setup_logger("logs/pipeline/ChatPipeline")
        self.logger.info("ChatPipeline 开始初始化")

        if use_local_llm:
            self.llm = get_chat_llm_local()
        else:
            self.llm = get_chat_llm_deepseek()
        self.logger.info("生成 LLM 加载完成")

        self.intent_router = IntentRouterPipeline(use_local_llm=use_local_llm)
        self.logger.info("意图路由 加载完成")

        self.query_rewriter = QueryRewriterPipeline(use_local_llm=use_local_llm)
        self.logger.info("查询重写 加载完成")

        self.rerank_pipeline = RerankPipeline()
        self.logger.info("检索Rerank 加载完成")

        self.logger.info("ChatPipeline 初始化完成")

    # ── 消息构建 ──────────────────────────────────────────────

    def _build_messages_for_chat(
        self, user_query: str, history: List[dict]
    ) -> list:
        """构建普通多轮对话的消息列表"""
        system = SystemMessage(content="""你是一个友好、博学的智能助手，可以和用户进行日常对话、解答各类问题。

## 对话要求
1. 根据对话上下文自然地回复用户，保持对话连贯性
2. 如果用户打招呼，热情回应并主动询问是否需要帮助
3. 如果用户询问你的能力，简要介绍你可以帮助检索知识库、解答问题、进行日常对话等
4. 回答时保持友好、自然、有帮助的语气""")

        messages = [system]
        for msg in history:
            if msg["role"] == "user" or msg["role"] == "fileupload":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                messages.append(AIMessage(content=msg["content"]))
        messages.append(HumanMessage(content=user_query))
        return messages

    def _build_messages_for_search(
        self, user_query: str, history: List[dict], context: str
    ) -> list:
        """构建带参考资料的知识问答消息列表"""
        system = SystemMessage(content=f"""你是一个专业的智能问答助手，请根据提供的参考资料回答用户的问题。

## 回答规则
1. 优先使用参考资料中的信息作答，引用时注明编号，如"根据【参考资料1】..."
2. 如果参考资料不足以完全回答问题，你可以结合自身知识进行补充，但必须明确区分：
   - 来自参考资料的信息标注来源编号
   - 来自你自身知识补充的内容，需加上"补充说明："前缀
3. 对于你确定、有把握的常识性知识，即使参考资料中没有，也可以参与回答，但不要编造不确定的信息
4. 回答应清晰、准确、有条理
5. 如果用户问题与参考资料完全无关，按常规对话方式回应

## Markdown 格式要求（重要）
- 数学公式必须用 LaTeX 语法包裹：行内公式用 `$...$`，独占一行的公式用 `$$...$$`
- 代码必须用三个反引号代码块包裹，并标注语言类型（如 ```python、```java、```sql 等）
- 即使参考资料中的公式或代码是纯文本格式，你也必须将其转换为上述 Markdown 格式后输出
- 表格、列表等内容也要使用对应的 Markdown 语法

## 参考资料
{context}""")

        messages = [system]
        for msg in history:
            if msg["role"] == "user" or msg["role"] == "fileupload":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                messages.append(AIMessage(content=msg["content"]))
        messages.append(HumanMessage(content=user_query))
        return messages

    # ── 检索分支 ──────────────────────────────────────────────

    def _retrieve(
        self,
        user_query: str,
        steps: list,
        history: List[dict],
        top_k: int,
        max_rewrite_queries: int,
        trace_id: str,
    ) -> tuple[list, bool]:
        """检索分支：查询重写 → 检索 → 返回 (messages, has_results)"""

        rewritten_queries = self.query_rewriter.rewrite(
            query=user_query,
            steps=steps,
            history=history,
            max_queries=max_rewrite_queries,
            trace_id=trace_id,
        )
        self.logger.info(
            f"[{trace_id}] 查询重写完成: {len(rewritten_queries)} 个, "
            f"top_k={top_k}, max_rewrite={max_rewrite_queries}"
        )

        retrieved_docs = self.rerank_pipeline.search_rerank(
            query=user_query,
            queries=rewritten_queries,
            steps=steps,
            top_k=top_k,
            trace_id=trace_id,
        )
        self.logger.info(f"[{trace_id}] 检索结果: {len(retrieved_docs)} 条")

        if not retrieved_docs:
            self.logger.info(f"[{trace_id}] 检索无结果，回退为多轮对话")
            steps.append("检索无结果，回退为普通多轮对话")
            return self._build_messages_for_chat(user_query, history), False

        context = self._build_context(retrieved_docs)
        self.logger.debug(f"[{trace_id}] 上下文长度: {len(context)} 字符")
        steps.append(f"上下文构建完成: {len(context)} 字符")
        return self._build_messages_for_search(user_query, history, context), True

    def _build_context(self, documents: List[str], max_docs: int = 5) -> str:
        """将检索文档拼接为上下文字符串"""
        if not documents:
            return ""
        parts = []
        for i, doc in enumerate(documents[:max_docs], 1):
            parts.append(f"【参考资料{i}】\n{doc}")
        return "\n\n".join(parts)

    # ── 主入口 ────────────────────────────────────────────────

    def chat(
        self,
        user_query: str,
        steps: list,
        history: List[dict] = None,
    ) -> Generator[str, None, None]:
        """主对话流程 —— 返回流式输出生成器

        Args:
            user_query: 用户输入
            steps: 步骤收集列表
            history: 历史消息列表 [{"role":"user","content":"xxx"},
                     {"role":"assistant","content":"xxx"}, ...]

        Yields:
            str: 流式输出的文本片段
        """
        trace_id = str(uuid.uuid4())[:8]
        self.logger.info(f"[{trace_id}] 收到对话: query={user_query[:80]}...")

        steps.append(f"收到查询: {user_query[:80]}...")

        if not user_query or not user_query.strip():
            self.logger.warning(f"[{trace_id}] 输入为空")
            steps.append("输入为空，返回提示")
            yield "请输入您的问题。"
            return

        if history is None:
            history = []
        self.logger.debug(f"[{trace_id}] 历史消息: {len(history)} 条")

        # 1. 意图识别（传入 user_query + 最近6条历史）
        intent_result = self.intent_router.route(
            user_input=user_query,
            steps=steps,
            history=history,
            trace_id=trace_id,
        )
        intent = intent_result.intent
        config = INTENT_CONFIG.get(intent, {'top_k': 8, 'max_rewrite_queries': 5})
        self.logger.info(
            f"[{trace_id}] 意图: {intent} "
            f"(置信度={intent_result.confidence:.3f}, "
            f"top_k={config['top_k']}, max_rewrite={config['max_rewrite_queries']})"
        )

        # 2. 根据意图分支
        if config['top_k'] == 0:
            messages = self._build_messages_for_chat(user_query, history)
            self.logger.debug(f"[{trace_id}] chat 分支")
            steps.append("普通多轮对话模式")
            steps.append(f"构建对话消息: {len(messages)} 条")
        else:
            messages, has_results = self._retrieve(
                user_query=user_query,
                steps=steps,
                history=history,
                top_k=config['top_k'],
                max_rewrite_queries=config['max_rewrite_queries'],
                trace_id=trace_id,
            )
            if not has_results:
                self.logger.info(f"[{trace_id}] 检索无结果，已使用多轮对话模式")

        # 3. 流式生成
        try:
            self.logger.info(f"[{trace_id}] 开始流式生成")
            steps.append("开始流式生成回复")
            for chunk in self.llm.stream(messages):
                if chunk.content is not None:
                    yield chunk.content
            steps.append("流式生成完成")
        except Exception as e:
            self.logger.error(f"[{trace_id}] 流式生成失败: {e}")
            steps.append(f"生成异常: {e}")
            yield f"\n\n[生成出错，请重试]"
