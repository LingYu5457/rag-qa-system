from langchain_text_splitters import RecursiveCharacterTextSplitter
from models.embedding import SiliconFlowEmbeddingClient
from typing import List
import numpy as np
from models.llm import DeepSeekClient

#切割文档
with open("data/tests/sample.txt", "r",encoding="utf-8") as f:
    text = f.read()
splitter = RecursiveCharacterTextSplitter(
    chunk_size=100, 
    chunk_overlap=20,
     separators=["\n\n", "\n", "。", " ", ""]
)
chunks = splitter.split_text(text)
for i,chunk in enumerate(chunks):
    print(f"Chunk {i}: {chunk}")

#向量嵌入
embedder = SiliconFlowEmbeddingClient()
chunk_embeddings = embedder.embed_batch(chunks)
for i, embedding in enumerate(chunk_embeddings):
    print(f"Chunk {i}: {embedding}")

#检索
def retrieve(query:str,top_k:int=3) -> List[dict]:
    query_embedding = embedder.embed(query)
    scores = np.dot(chunk_embeddings, query_embedding)
    top_indices = np.argsort(scores)[::-1][:top_k]
    results = []
    for i in top_indices:
        results.append({
            "text": chunks[i],
            "score": float(scores[i]),
            "index": int(i)
        })
    return results
query = "RAG如何减少幻觉"
retrieved=retrieve(query)
context = "\n\n".join([
    f"[来源{i+1}] {r['text']}" for i, r in enumerate(retrieved)
])

#生成回答
llm = DeepSeekClient()

prompt=f"""你是一个知识库助手。请严格根据以下参考文档回答问题。
如果文档中没有答案，请明确说"未找到相关信息"。
## 参考文档
{context}
##用户问题
{query}
## 回答（请标注来源编号）:"""

print("\n"+"="*50)
print("检索到的文档：")
for r in retrieved:
    print(f"[来源{r['index']}](score={r['score']:.3f}) {r['text']}")
print("\n"+"="*50)
print("LLM生成的答案：")
answer = llm.chat(prompt)
print(answer)