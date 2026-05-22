from langchain_community.document_loaders import (
    PyMuPDFLoader, Docx2txtLoader, TextLoader, UnstructuredHTMLLoader)
import time
import uuid
from config.logger_config import setup_logger

class FileParserPipeline:
    def __init__(self):
        self.logger = setup_logger("logs/pipeline/FileParser")

    def parse_file(self, file_path: str, trace_id: str = None):
        trace_id = trace_id or str(uuid.uuid4())[:8]
        start_time = time.time()

        ext = file_path.split(".")[-1].lower()
        self.logger.info(f"[{trace_id}]开始解析文件,文件类型{ext}")

        res = None
        try:
            if ext == 'pdf':
                res = self.parse_pdf(file_path, trace_id)
            elif ext == 'docx':
                res = self.parse_docx(file_path, trace_id)
            elif ext in ['txt', 'md']:
                res = self.parse_txt(file_path, trace_id)
            elif ext in ['html', 'htm']:
                res = self.parse_html(file_path, trace_id)
            else:
                self.logger.warning(f"[{trace_id}]不支持的文件类型: {ext}")
                return None
        except Exception as e:
            self.logger.error(f"[{trace_id}]解析失败: {e}")
            return None

        elapsed = (time.time() - start_time) * 1000
        page_count = len(res) if isinstance(res, list) else 1
        self.logger.info(f"[{trace_id}] 解析完成，{page_count}页，耗时{elapsed:.2f}ms")
        return res

    def parse_pdf(self, file_path: str, trace_id: str):
        self.logger.debug(f"[{trace_id}]使用 PyMuPDFLoader 解析 PDF")
        loader = PyMuPDFLoader(file_path)
        documents = loader.load()
        self.logger.debug(f"[{trace_id}]PDF 解析到 {len(documents)} 页")
        return documents

    def parse_docx(self, file_path: str, trace_id: str):
        self.logger.debug(f"[{trace_id}]使用 Docx2txtLoader 解析 DOCX")
        loader = Docx2txtLoader(file_path)
        documents = loader.load()
        self.logger.debug(f"[{trace_id}]DOCX 解析完成")
        return documents

    def parse_txt(self, file_path: str, trace_id: str):
        self.logger.debug(f"[{trace_id}]使用 TextLoader 解析文本文件")
        loader = TextLoader(file_path, encoding='utf-8')
        documents = loader.load()
        self.logger.debug(f"[{trace_id}]文本文件解析完成")
        return documents
    
    def parse_html(self, file_path: str, trace_id: str):
        self.logger.debug(f"[{trace_id}]使用 UnstructuredHTMLLoader 解析 HTML")
        loader = UnstructuredHTMLLoader(file_path)
        documents = loader.load()
        self.logger.debug(f"[{trace_id}]HTML 解析完成，提取到 {len(documents)} 块")
        return documents