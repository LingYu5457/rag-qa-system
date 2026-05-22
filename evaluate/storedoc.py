from rag.document_processing.store import DocumentStorePipeline
import glob
import os

pipeline = DocumentStorePipeline()
pdf_files = glob.glob(os.path.join("data/eval", "**/*.pdf"), recursive=True)
for pdf_path in pdf_files:
    pipeline.store(pdf_path)