from langchain_core.messages import SystemMessage, HumanMessage
from models.llm import get_chat_llm_deepseek
from config.logger_config import setup_logger

MAX_CONTENT_CHARS = 4000


class DocumentSummarizer:
    def __init__(self):
        self.logger = setup_logger("logs/pipeline/DocumentSummarizer")
        self.llm = get_chat_llm_deepseek()

    def summarize(self, content: str, file_name: str) -> str:
        if len(content) > MAX_CONTENT_CHARS:
            content = content[:MAX_CONTENT_CHARS]

        messages = [
            SystemMessage(
                content="你是一个文档摘要助手。根据提供的文档内容生成简洁摘要。"
                "要求：1. 摘要控制在500字以内 2. 提取文档核心主题、关键信息和结论"
                "3. 使用客观中立的语气 4. 只输出摘要正文，不加任何前缀标签"
            ),
            HumanMessage(content=f"文件名：{file_name}\n\n文档内容：\n{content}\n\n请生成摘要："),
        ]
        try:
            response = self.llm.invoke(messages)
            summary = response.content.strip()
            return summary
        except Exception as e:
            self.logger.error(f"摘要生成失败: {e}")
            return f"[文件上传] {file_name}"
