import uuid
from typing import List, Optional
from pydantic import BaseModel, Field
from models.llm import get_chat_llm_deepseek, get_chat_llm_local
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from config.logger_config import setup_logger


class RewrittenQueries(BaseModel):
    """改写后的查询列表"""
    queries: List[str] = Field(description="改写后的检索查询列表，每个元素是一个独立的自然语言问题或陈述句")


class QueryRewriterPipeline:
    def __init__(self, use_local_llm: bool = False):
        self.logger = setup_logger("logs/pipeline/QueryRewriterPipeline")
        self.logger.info("QueryRewriterPipeline 开始初始化")

        if use_local_llm:
            self.llm = get_chat_llm_local()
        else:
            self.llm = get_chat_llm_deepseek()

        self.logger.info("LLM 加载完成")

        self._init_chain()
        self.logger.info("QueryRewriterPipeline 初始化完成")

    def _init_chain(self):
        """初始化 Prompt 和 Chain"""
        system_template = """你是一个查询改写专家，服务于 RAG（检索增强生成）系统的检索环节。你的任务是将用户的原始问题改写为多个不同角度的检索查询，以最大化召回相关文档的概率。

## 改写策略
1. **同义词/术语替换**：用同义词、相关术语、中英文对照替换关键词
2. **粒度拆分**：将复杂问题分解为更具体的子问题
3. **限定词增删**：添加或移除时间、范围、场景等限定词
4. **视角转换**：从不同角色或角度提问
5. **显式化隐含信息**：将口语化、省略的表达补全为完整句

## 对话历史利用
如果提供了对话历史：
- 将历史中提到的实体、缩写、指代在改写时显式补全
- 如果当前问题是追问，将依赖的前置信息融入查询
- 不要重复历史中已有明确结论的查询

## 质量约束
- 每个查询必须语义独立，脱离上下文也能被理解
- 查询之间保持足够差异，避免仅差一个词的情况
- 不改写为与原意偏离的方向
- 不生成只有关键词的查询，必须是完整的自然语言问题或陈述句
- 如果原问题本身已经是高质量的检索查询，可保留原问题作为其中一个查询

## 输出格式
请严格输出 JSON 格式，包含一个 "queries" 字段，其值为字符串列表。
示例：
{{
  "queries": ["查询1", "查询2", "查询3"]
}}"""

        user_template = """## 对话历史
{history}

## 用户当前问题
{query}

请生成最多 {max_queries} 个改写查询。注意：如果问题简单，生成2-3个即可；如果复杂，可生成更多，但绝对不超过 {max_queries} 个。"""

        self.rewrite_prompt = ChatPromptTemplate.from_messages([
            ("system", system_template),
            ("human", user_template),
        ])

        parser = JsonOutputParser(pydantic_object=RewrittenQueries)
        self.chain = self.rewrite_prompt | self.llm | parser

    def _format_history(self, history: Optional[List[dict]]) -> str:
        """将消息列表格式化为文本"""
        if not history:
            return "（无）"
        lines = []
        for msg in history:
            role_label = "用户" if msg.get("role") == "user" else "助手"
            lines.append(f"{role_label}：{msg.get('content', '')}")
        return "\n".join(lines)

    def rewrite(
        self,
        query: str,
        steps: list,
        history: Optional[List[dict]] = None,
        max_queries: int = 5,
        trace_id: str = None,
    ) -> List[str]:
        """改写用户查询为多个检索查询

        Args:
            query: 用户原始查询
            steps: 步骤收集列表
            history: 历史消息列表 [{"role":"user","content":"xxx"}, ...]
            max_queries: 最大改写查询数
            trace_id: 追踪ID

        Returns:
            改写后的查询列表
        """
        trace_id = trace_id or str(uuid.uuid4())[:8]
        if not query:
            return []

        history = history or []
        history_str = self._format_history(history[-6:])  # 最多取最近6条

        input_data = {
            "query": query,
            "history": history_str,
            "max_queries": max_queries,
        }

        try:
            self.logger.debug(f"[{trace_id}] 正在改写查询: {query}, 历史: {len(history)} 条")
            result = self.chain.invoke(input_data)

            if isinstance(result, RewrittenQueries):
                queries = result.queries
            elif isinstance(result, dict):
                queries = result.get("queries", [])
            else:
                queries = result

            if not queries:
                self.logger.warning(f"[{trace_id}] 改写结果为空，使用原查询")
                steps.append(f"查询重写结果为空，使用原查询: {query[:50]}...")
                return [query]

            self.logger.info(f"[{trace_id}] 查询改写完成: {len(queries)} 个")
            steps.append(f"查询重写完成，生成 {len(queries)} 个改写查询")
            for i, q in enumerate(queries):
                steps.append(f"查询{i+1}: {q}")
            return queries

        except Exception as e:
            self.logger.error(f"[{trace_id}] 改写查询时出错: {e}")
            steps.append(f"查询重写异常: {e}")
            return [query]
