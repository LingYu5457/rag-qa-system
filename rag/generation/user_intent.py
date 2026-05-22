import uuid
from typing import Optional, List
from pydantic import BaseModel, Field
from typing import Literal
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from models.llm import get_chat_llm_deepseek, get_chat_llm_local
from config.logger_config import setup_logger


class Intent(BaseModel):
    """意图分类"""
    intent: Literal['search_precise', 'search_broad', 'search_deep', 'chat'] = Field(
        description="用户意图类型"
    )
    confidence: float = Field(description="意图分类置信度0-1")


class IntentRouterPipeline:
    def __init__(self, use_local_llm: bool = False):
        self.logger = setup_logger("logs/pipeline/IntentRouterPipeline")
        self.logger.info("IntentRouterPipeline 开始初始化")

        if use_local_llm:
            self.llm = get_chat_llm_local()
        else:
            self.llm = get_chat_llm_deepseek()

        self.logger.info("LLM 加载完成")

        self._init_chain()
        self.logger.info("IntentRouterPipeline 初始化完成")

    def _init_chain(self):
        """初始化 Prompt 和 Chain"""
        system_template = """你是一个意图分类专家，服务于 RAG（检索增强生成）系统的路由环节。你的任务是根据用户输入判断意图类型，以决定检索策略。

## 意图类型定义
- **search_precise**：精确事实查询，答案集中在单一知识点，用少量文档即可回答。包括：
  - 查找具体数值、日期、定义、公式、参数
  - 确认特定事实的是/否类问题（如"XXX是否支持YYY？"）
  - 针对特定术语、API、配置项的精准提问
  - 特点：问题聚焦、答案明确、不需要大量上下文

- **search_broad**：广泛知识查询，答案需要综合多方面信息。包括：
  - "XXX有哪些方法/类型/特点/应用场景"
  - 对比分析类问题（如"XXX和YYY有什么区别"）
  - 需要了解某个主题全貌的概述性问题
  - 特点：需要覆盖多个角度、期望较为全面的回答

- **search_deep**：深度研究查询，需要详尽、全面的背景资料才能回答。包括：
  - 复杂技术原理、系统架构、工作流程说明
  - "详细说明XXX的实现原理/完整流程"
  - 需要深入理解多层嵌套概念的问题
  - 跨文档的综合分析、总结类请求
  - 特点：问题复杂、需要大量上下文、期望深入详尽的回答

- **chat**：普通对话，不需要检索知识库。包括：
  - 问候、寒暄（如"你好"、"早上好"）
  - 闲聊、情感表达（如"今天心情不错"）
  - 对系统本身的询问（如"你能做什么"、"你有什么功能"）
  - 纯主观观点交流、无事实依赖的讨论

## 判断原则
1. 当不确定时，选择 search_broad —— 中等检索量是安全的默认选择
2. 简单的事实确认、定义查询 → search_precise
3. 需要多方面信息的问题 → search_broad
4. 复杂、深入、需要详尽回答的问题 → search_deep
5. 只有明确是闲聊、问候或纯主观表达时才判为 chat
6. 置信度反映判断的确定性：0.9以上 = 非常确定，0.7-0.9 = 比较确定，0.5-0.7 = 不确定

## 输出格式
请严格输出 JSON 格式，包含 "intent" 和 "confidence" 两个字段。
示例：
{{"intent": "search_precise", "confidence": 0.95}}
{{"intent": "search_broad", "confidence": 0.90}}
{{"intent": "search_deep", "confidence": 0.88}}
{{"intent": "chat", "confidence": 0.98}}"""

        user_template = """## 对话历史
{history}

## 用户当前输入
{input}

请判断以上「用户当前输入」的意图类型。"""

        self.intent_prompt = ChatPromptTemplate.from_messages([
            ("system", system_template),
            ("human", user_template),
        ])

        parser = JsonOutputParser(pydantic_object=Intent)
        self.chain = self.intent_prompt | self.llm | parser

    def _format_history(self, history: Optional[List[dict]]) -> str:
        """将消息列表格式化为文本，用于意图分类的上下文"""
        if not history:
            return "（无历史对话）"
        lines = []
        for msg in history:
            role_label = "用户" if msg.get("role") == "user" else "助手"
            lines.append(f"{role_label}：{msg.get('content', '')}")
        return "\n".join(lines)

    def route(
        self,
        user_input: str,
        steps: list,
        history: Optional[List[dict]] = None,
        trace_id: Optional[str] = None,
    ) -> Intent:
        """对用户输入进行意图分类

        Args:
            user_input: 用户输入文本
            steps: 步骤收集列表
            history: 历史消息列表 [{"role":"user","content":"xxx"}, ...]
            trace_id: 追踪ID，不提供则自动生成

        Returns:
            Intent 对象，包含 intent 和 confidence 字段
        """
        trace_id = trace_id or str(uuid.uuid4())[:8]

        if not user_input or not user_input.strip():
            self.logger.warning(f"[{trace_id}] 用户输入为空，默认返回 chat")
            steps.append("意图识别: 输入为空，默认chat")
            return Intent(intent="chat", confidence=1.0)

        history = history or []
        history_str = self._format_history(history[-6:])  # 最多取最近6条

        try:
            self.logger.debug(f"[{trace_id}] 正在进行意图分类: {user_input[:100]}")
            result = self.chain.invoke({
                "input": user_input,
                "history": history_str,
            })

            if isinstance(result, Intent):
                intent_result = result
            elif isinstance(result, dict):
                intent_result = Intent(**result)
            else:
                self.logger.warning(f"[{trace_id}] 未知结果类型: {type(result)}，默认返回 search_broad")
                steps.append("意图识别: 结果类型未知，默认search_broad")
                return Intent(intent="search_broad", confidence=0.5)

            self.logger.info(
                f"[{trace_id}] 意图分类完成: intent={intent_result.intent}, "
                f"confidence={intent_result.confidence:.3f}"
            )
            steps.append(f"意图识别完成: {intent_result.intent} (置信度={intent_result.confidence:.2f})")
            return intent_result

        except Exception as e:
            self.logger.error(f"[{trace_id}] 意图分类出错: {e}，默认返回 search_broad")
            steps.append(f"意图识别异常: {e}，默认search_broad")
            return Intent(intent="search_broad", confidence=0.5)
