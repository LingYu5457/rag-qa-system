# RAG-QA-System

基于 **RAG（检索增强生成）** 架构的智能知识问答系统。支持用户上传文档（PDF/DOCX/TXT/HTML/Markdown），通过混合检索（BM25 + 向量检索）与重排序召回相关内容，结合 LLM 流式生成高质量回答。

## 技术架构

```
frontend (Vue 3 + TypeScript + Vite)
    ↕ SSE 流式响应
backend (FastAPI + Tortoise ORM)
    ↕
┌─────────────────────────────────┐
│  RAG Pipeline                   │
│  ┌─────────────┐ ┌────────────┐ │
│  │ 意图路由      │ │ 查询重写    │ │
│  │ (4类意图)   │ │ (多角度)     │ │
│  └──────┬──────┘ └─────┬──────┘ │
│         ↓               ↓       │
│  ┌──────────────────────────┐   │
│  │ 混合检索 (Hybrid Search) │    │
│  │  BM25(ES) + 向量(Milvus)│     │
│  └──────────┬───────────────┘   │
│             ↓                   │
│  ┌──────────────────┐            │
│  │ Reranker 精排    │            │
│  └────────┬─────────┘            │
│           ↓                      │
│  ┌──────────────────┐            │
│  │ LLM 流式生成     │            │
│  │ DeepSeek API     │            │
│  └──────────────────┘            │
└─────────────────────────────────┘
    ↕
┌─────────────────────────────────┐
│  数据层                          │
│  MySQL  |  Milvus  |  ES        │
│  (业务) | (向量)   | (全文)     │
└─────────────────────────────────┘
```

## 核心功能

- **文档管理**：上传/删除文档，自动解析、分块、向量化并存入 Milvus 和 ES
- **智能检索**：意图分类（精确搜索/广泛搜索/深度搜索/闲聊）→ 查询多角度重写 → BM25 + 向量混合检索 → RRF 融合 → Reranker 精排
- **流式对话**：基于 SSE 的流式生成，支持多轮对话历史上下文
- **多用户支持**：用户注册/登录，会话管理，对话历史查询

## 项目结构

```
├── backend/            # FastAPI 后端
│   ├── main.py         # 应用入口
│   └── app/
│       ├── user/       # 用户注册/登录
│       ├── session/    # 会话 CRUD + 标题生成
│       ├── chat/       # 对话接口 (SSE 流式)
│       └── file/       # 文件上传/删除
├── rag/                # RAG 核心管道
│   ├── document_processing/
│   │   ├── parse.py    # 多格式文件解析
│   │   └── store.py    # 文档分块→向量化→入库
│   ├── retrieval/
│   │   ├── hybrid_search.py  # BM25+向量混合检索+RRF融合
│   │   └── rerank.py         # Reranker 精排管道
│   └── generation/
│       ├── user_intent.py    # LLM 意图分类
│       ├── query_process.py  # LLM 查询重写
│       ├── chat.py           # 主对话管道
│       ├── title_generator.py
│       └── summarizer.py
├── models/             # AI 模型客户端
│   ├── llm.py          # DeepSeek (OpenAI 兼容)
│   ├── embedding.py    # SiliconFlow Embedding (BGE-M3)
│   └── reranker.py     # SiliconFlow Reranker (BGE-Reranker-V2)
├── database/
│   ├── models.py       # Tortoise ORM 数据模型
│   ├── mysql.py        # MySQL 连接
│   ├── vector_db.py    # Milvus 向量库操作
│   └── text_db.py      # ES 全文索引操作
├── config/
│   ├── settings.py     # 全局配置 (从 .env 加载)
│   └── logger_config.py
├── frontend/           # Vue 3 + TypeScript + Vite
├── migrations/         # Aerich 数据库迁移
└── data/               # 模型文件 / 测试数据
```

## 快速开始

### 环境要求

- Python 3.10+
- Node.js 20+
- MySQL 8.0+
- Elasticsearch 8.x（需安装 IK 分词器）
- Milvus 2.x

### 1. 安装后端依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 填入各服务的连接信息与 API Key
```

主要配置项：

| 配置 | 说明 |
|------|------|
| `DEEPSEEK_API_KEY` | DeepSeek API 密钥（LLM 生成） |
| `DEEPSEEK_MODEL` | 模型名称，默认 `deepseek-v4-flash` |
| `SILICONFLOW_API_KEY` | SiliconFlow API 密钥（Embedding + Reranker） |
| `SILICONFLOW_EMBEDDING_MODEL` | 嵌入模型，默认 `Pro/BAAI/bge-m3` |
| `MILVUS_HOST` / `MILVUS_PORT` | Milvus 连接信息 |
| `ES_HOST` / `ES_PORT` | Elasticsearch 连接信息 |
| `MYSQL_HOST` / `MYSQL_PORT` | MySQL 连接信息 |

### 3. 启动 MySQL / ES / Milvus

确保三个数据服务已运行。

### 4. 数据库迁移

```bash
aerich upgrade
```

### 5. 启动后端

```bash
python backend/main.py
# 默认 http://127.0.0.1:8000
# Swagger 文档: http://127.0.0.1:8000/docs
```

### 6. 启动前端

```bash
cd frontend
npm install
npm run dev
```

## API 概览

| 模块 | 端点 | 说明 |
|------|------|------|
| 用户 | `POST /user/register` | 用户注册 |
| 用户 | `POST /user/login` | 用户登录 |
| 会话 | `POST /session/create` | 创建会话（含 LLM 生成标题） |
| 会话 | `GET /session/history/{user_id}` | 用户会话列表 |
| 会话 | `GET /session/{session_id}` | 会话消息详情 |
| 会话 | `DELETE /session/{session_id}` | 删除会话（联动清理 ES/Milvus） |
| 对话 | `POST /chat/query` | SSE 流式问答 |
| 对话 | `GET /chat/step/{session_id}` | 获取管道执行步骤（调试用） |
| 文件 | `POST /file/upload` | 上传文件到会话 |
| 文件 | `POST /file/upload_rag` | 上传文件并入库 RAG |
| 文件 | `DELETE /file/{file_id}` | 删除文件 |
| 文件 | `GET /file/history/{user_id}` | 用户文件列表 |

## RAG 管道流程

1. **意图路由** — LLM 将用户输入分为四类：精确搜索 / 广泛搜索 / 深度搜索 / 闲聊，动态决定检索深度
2. **查询重写** — LLM 将原始问题改写为多个不同角度的检索查询，提升召回率
3. **混合检索** — 并行执行 BM25 全文检索（ES + IK 分词）和向量语义检索（Milvus），通过 RRF 算法融合排序
4. **重排序** — BGE-Reranker-V2 对候选文档精排，取 Top-K 最相关文档
5. **LLM 生成** — DeepSeek 基于检索上下文流式生成回答

## 关键技术

- **混合检索 + RRF 融合**：BM25（精确关键词匹配）与向量检索（语义相似度）互补，RRF 无需调参即可融合
- **多查询重写**：针对不同检索深度的意图自适应调整查写数量（3-7个）
- **中文分词**：ES 使用 IK 分词器（`ik_max_word` 索引 / `ik_smart` 搜索）
- **流式 SSE**：FastAPI StreamingResponse + 线程池，非阻塞推送生成结果
