import time
import uuid
import os
import hashlib
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List
from config.logger_config import setup_logger
from config.settings import RAGSettings as config
from rag.document_processing.parse import FileParserPipeline
from models.embedding import SiliconFlowEmbedding
from database.vector_db import MilvusVectorDB
from database.text_db import ElasticsearchDB

class DocumentStorePipeline:
    def __init__(self):
        self.logger = setup_logger("logs/pipeline/DocumentStore")
        self.logger.info("初始化文档存储")

        self.file_parser = FileParserPipeline()
        self.logger.info("文件解析初始化成功")

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = config.CHUNK_SIZE,
            chunk_overlap = config.CHUNK_OVERLAP,
            separators=["\n\n", "\n", "。", "！", "？", "；", "，", " ", ""]
        )
        self.logger.info("文本切分初始化成功")

        self.embedding = SiliconFlowEmbedding()
        self.logger.info("embedding初始化成功")

        self.vector_db = MilvusVectorDB()
        self.logger.info("向量数据库初始化成功")

        self.text_db = ElasticsearchDB()
        self.logger.info("ES数据库初始化成功")


        self.logger.info("初始化完成")

    def store(self, path: str, trace_id: str = None) -> List[int]:
        trace_id = trace_id or str(uuid.uuid4())[:8]
        start_time = time.time()

        self.logger.info(f"[{trace_id}]开始存入程序")


        if not os.path.isfile(path):
            self.logger.error(f"[{trace_id}]文件不存在")
            return None

        try:
            filepath = os.path.abspath(path)
            documents = self.file_parser.parse_file(filepath)
            chunks = self.text_splitter.split_documents(documents)
            self.logger.info(f"[{trace_id}]文档分块完成，共{len(chunks)}个块")

            embeddings = self.embedding.embed_batch(
                [chunk.page_content for chunk in chunks]
            )
            self.logger.info(f"[{trace_id}]嵌入完成,共{len(embeddings)}个嵌入向量")

            source_hash = hashlib.md5(filepath.encode()).hexdigest()[:8]
            text_ids = [f"{source_hash}_{i}" for i in range(len(chunks))]

            # 过滤掉嵌入失败的块
            valid_pairs = [
                (tid, emb) for tid, emb in zip(text_ids, embeddings) if emb is not None
            ]
            if not valid_pairs:
                raise RuntimeError("所有文本块嵌入失败，无法存入向量数据库")
            valid_ids, valid_embeddings = zip(*valid_pairs)
            total_vector = self.vector_db.insert(list(valid_ids), list(valid_embeddings))
            
            # 提取信息，没有 page 就用 chunk 序号
            contents = [chunk.page_content for chunk in chunks]
            sources = [chunk.metadata.get("source", "") for chunk in chunks]
            page_nums = [
                chunk.metadata.get("page", i)   # 有页码用页码，没有用 chunk 序号
                for i, chunk in enumerate(chunks)
            ]
            titles = [chunk.metadata.get("title", "") for chunk in chunks]
            
            total_text=self.text_db.insert(text_ids, contents, titles, sources, page_nums)

            elapsed = (time.time() - start_time) * 1000
            self.logger.info(f"[{trace_id}] 存入完成 | 向量:{total_vector} | 文本:{total_text} | 耗时:{elapsed:.2f}ms")

            return [total_vector, total_text]
            
        except Exception as e:
            self.logger.error(f"[{trace_id}] 文档存入失败: {str(e)}", exc_info=True)
            raise e

    def delete_by_file(self, path: str, trace_id: str = None) -> List[int]:
        trace_id = trace_id or str(uuid.uuid4())[:8]
        start_time = time.time()

        self.logger.info(f"[{trace_id}]开始删除")

        if not os.path.isfile(path):
            self.logger.error(f"[{trace_id}]文件不存在")
            return None
        try:
            filepath = os.path.abspath(path)
            source_hash = hashlib.md5(filepath.encode()).hexdigest()[:8]
            res_vector = self.vector_db.delete_by_hashsource(source_hash)
            res_text = self.text_db.delete_by_hashsource(source_hash)

            elapsed = (time.time() - start_time) * 1000
            self.logger.info(f"[{trace_id}] 删除完成 | 向量:{res_vector} | 文本:{res_text} | 耗时:{elapsed:.2f}ms")
            return [res_vector,res_text]
        
        except Exception as e:
            self.logger.error(f"[{trace_id}] 删除数据失败: {str(e)}", exc_info=True)
            raise e

    def close(self):
        """清理资源"""
        try:
            if hasattr(self, 'vector_db') and hasattr(self.vector_db, 'close'):
                self.vector_db.close()
            if hasattr(self, 'text_db') and hasattr(self.text_db, 'close'):
                self.text_db.close()
            self.logger.info("资源清理完成")
        except Exception as e:
            self.logger.error(f"资源清理失败: {e}")

    def __del__(self):
        """析构函数，确保资源释放"""
        self.close()