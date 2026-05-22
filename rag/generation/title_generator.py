from langchain_core.messages import SystemMessage, HumanMessage
from models.llm import get_chat_llm_deepseek
from config.logger_config import setup_logger


class TitleGenerator:
    def __init__(self):
        self.logger = setup_logger("logs/pipeline/TitleGenerator")
        self.llm = get_chat_llm_deepseek()

    def generate(self, query: str) -> str:
        messages = [
            SystemMessage(
                content="你是一个标题生成助手。根据用户的提问生成一个简短的会话标题。"
                "要求：1. 精炼概括问题主题 2. 不超过15个汉字（或30个英文字符）"
                "3. 只输出纯标题文本，不加引号、标点、换行或其他修饰"
            ),
            HumanMessage(content=f"用户提问：{query}\n\n请生成标题："),
        ]
        try:
            response = self.llm.invoke(messages)
            title = response.content.strip()
            if len(title) > 15:
                title = title[:15]
            return title or query[:15]
        except Exception as e:
            self.logger.error(f"标题生成失败: {e}")
            return query[:15]
