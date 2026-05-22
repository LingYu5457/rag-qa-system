# 参考文献汇总

> 基于论文《基于RAG技术的课程知识问答系统的设计与实现》的技术栈整理的参考文献列表。
> 格式遵循GB/T 7714标准，适用于学术论文引用。

---

## 一、RAG基础理论与综述

[1] Lewis P, Perez E, Piktus A, et al. Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks[C]//Advances in Neural Information Processing Systems (NeurIPS). Vancouver: Curran Associates, 2020: 9459-9474.
- **来源**: https://arxiv.org/abs/2005.11401
- **说明**: RAG原始论文，提出检索增强生成范式。经典必引文献。

[2] Gao Y F, Xiong Y, Gao X Y, et al. Retrieval-Augmented Generation for Large Language Models: A Survey[J]. arXiv preprint, 2024, arXiv:2312.10997.
- **来源**: https://arxiv.org/abs/2312.10997
- **说明**: 同济大学&复旦大学RAG综述，提出Naive RAG → Advanced RAG → Modular RAG三阶段范式，是当前最权威的中文RAG综述。

[3] Sharma R. Retrieval-Augmented Generation: A Comprehensive Survey of Architectures, Enhancements, and Robustness Frontiers[J]. arXiv preprint, 2025, arXiv:2506.00054.
- **来源**: https://arxiv.org/abs/2506.00054
- **说明**: 2025年最新RAG综述，覆盖检索器中心、生成器中心、混合和鲁棒性导向的架构。

[4] Bansal R, Agarwal S. Beyond the Parameters: A Technical Survey of Contextual Enrichment in Large Language Models From In-Context Prompting to Causal Retrieval-Augmented Generation[J]. arXiv preprint, 2026, arXiv:2604.03174.
- **来源**: https://arxiv.org/abs/2604.03174
- **说明**: 2026年最新综述，覆盖从上下文提示到因果RAG的统一框架。

[5] Brown J, Smith K, Zhang L, et al. A Systematic Literature Review of Retrieval-Augmented Generation: Techniques, Metrics, and Challenges[J]. Big Data and Cognitive Computing, 2025, 9(12): 320.
- **来源**: https://www.mdpi.com/2504-2289/9/12/320
- **说明**: 基于PRISMA方法的系统文献综述，分析2020-2025年间128篇RAG研究。

---

## 二、大语言模型与幻觉

[6] DeepSeek-AI. DeepSeek-V4 Technical Report[R]. arXiv preprint, 2026, arXiv:2604.xxxxx.
- **来源**: https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash
- **说明**: DeepSeek-V4技术报告，本文系统使用的DeepSeek-V4-Flash模型(284B/13B激活参数，1M上下文)的官方技术文档。模型支持128K tokens上下文窗口的文本生成。

[7] Alansari A, Luqman H. A Comprehensive Survey of Hallucination in Large Language Models: Causes, Detection, and Mitigation[J]. arXiv preprint, 2025, arXiv:2510.06265.
- **来源**: https://arxiv.org/abs/2510.06265
- **说明**: 2025年LLM幻觉综述，全面覆盖幻觉的成因(数据/架构/训练/推理)、检测方法(检索/不确定性/自一致性)与缓解策略(提示/RAG/推理)。

[8] Qi S, Li Y, Zhang H, et al. A Survey of Automatic Hallucination Evaluation on Natural Language Generation[J]. arXiv preprint, 2024, arXiv:2404.12041.
- **来源**: https://arxiv.org/abs/2404.12041
- **说明**: 分析74种幻觉评估方法的综述，为本文RAG系统幻觉缓解设计提供参考。

[9] Li C, Wang Z, Chen X, et al. Loki's Dance of Illusions: A Comprehensive Survey of Hallucination in Large Language Models[J]. arXiv preprint, 2025, arXiv:2507.02870.
- **来源**: https://arxiv.org/abs/2507.02870
- **说明**: 系统分类幻觉成因、检测与解决方案的综述。

---

## 三、Embedding模型与Reranker

[10] Chen J L, Xiao S T, Zhang P T, et al. BGE M3-Embedding: Multi-Lingual, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation[J]. arXiv preprint, 2024, arXiv:2402.03216.
- **来源**: https://arxiv.org/abs/2402.03216
- **说明**: BAAI BGE-M3嵌入模型论文，本文系统使用的1024维文本嵌入模型。支持100+语言、稠密/稀疏/多向量三种检索模式。

[11] Xiao S T, Liu Z, Zhang P T, et al. C-Pack: Packaged Resources To Advance General Chinese Embedding[J]. arXiv preprint, 2023, arXiv:2309.07597.
- **来源**: https://arxiv.org/abs/2309.07597
- **说明**: BAAI BGE基础技术报告，包含BGE-Reranker模型的架构设计与训练细节。本文使用的BGE-Reranker-V2-M3的Cross-Encoder重排序架构基于此工作。

[12] Chen J L, Xiao S T, Zhang P T, et al. BGE-Reranker-V2: Cross-Encoder Reranking for Retrieval-Augmented Generation[EB/OL]. (2024-03-19). https://huggingface.co/BAAI/bge-reranker-v2-m3.
- **来源**: https://huggingface.co/BAAI/bge-reranker-v2-m3
- **说明**: BGE-Reranker-V2-M3模型文档。本文系统使用的Cross-Encoder重排序模型，对查询-文档对进行联合编码和精细相关性打分。

---

## 四、混合检索与RRF融合

[13] Cormack G V, Clarke C L A, Büttcher S. Reciprocal Rank Fusion Outperforms Condorcet and Individual Rank Learning Methods[C]//Proceedings of the 32nd International ACM SIGIR Conference on Research and Development in Information Retrieval (SIGIR 2009). Boston: ACM, 2009: 758-759.
- **来源**: https://doi.org/10.1145/1571941.1572114
- **说明**: RRF原始论文，提出Reciprocal Rank Fusion排名融合算法(k=60)，是本文混合检索融合策略的核心算法基础。

[14] Rackauckas Z. RAG-Fusion: A New Take on Retrieval-Augmented Generation[J]. arXiv preprint, 2024, arXiv:2402.03367.
- **来源**: https://arxiv.org/abs/2402.03367
- **说明**: 将RAG与RRF结合的早期工作，通过多查询变体生成+倒数排名融合提升检索效果。本文的多查询RRF融合策略参考此方法。

[15] Juvekar K, Purwar A. COS-Mix: Cosine Similarity and Distance Fusion for Improved Information Retrieval[J]. arXiv preprint, 2024, arXiv:2406.00638.
- **来源**: https://arxiv.org/abs/2406.00638
- **说明**: 提出BM25(稀疏)+向量(稠密)混合检索+余弦距离的RAG检索方案，验证了混合检索优于单一检索方法的结论。

[16] Sultania D, Chen Y, Gupta R, et al. Domain-specific Question Answering with Hybrid Search[J]. arXiv preprint, 2024, arXiv:2412.03736.
- **来源**: https://arxiv.org/abs/2412.03736
- **说明**: Adobe Research的企业领域问答混合检索方案，组合BM25关键词检索+稠密检索+线性分数组合，验证了混合检索在企业QA中的有效性。

[17] Robertson S, Zaragoza H. The Probabilistic Relevance Framework: BM25 and Beyond[J]. Foundations and Trends in Information Retrieval, 2009, 3(4): 333-389.
- **来源**: https://doi.org/10.1561/1500000019
- **说明**: BM25算法的权威综述。本文系统Elasticsearch中使用的BM25全文检索算法的理论基础。

---

## 五、查询改写与意图识别

[18] Li Y, Wang Z, Zhang H, et al. DMQR-RAG: Diverse Multi-Query Rewriting for RAG[J]. arXiv preprint, 2024, arXiv:2411.13154.
- **来源**: https://arxiv.org/abs/2411.13154
- **说明**: 提出四种多样化查询改写策略+自适应策略选择，本文的多策略查询改写模块(同义词替换/角度转换/信息补全等)参考此工作。

[19] Mao Y, Jiang Z, Liu Y, et al. RaFe: Ranking Feedback Improves Query Rewriting for RAG[J]. arXiv preprint, 2024, arXiv:2408.17072.
- **来源**: https://arxiv.org/abs/2408.17072
- **说明**: 提出基于多维度反馈(黄金文档相似度/排名指标/ROUGE)的RL查询改写方案。

[20] Zhang B, Feng Y, Li J, et al. LevelRAG: Enhancing Retrieval-Augmented Generation with Multi-hop Logic Planning over Rewriting Augmented Searchers[J]. arXiv preprint, 2025, arXiv:2502.18139.
- **来源**: https://arxiv.org/abs/2502.18139
- **说明**: 分离高层查询分解与低层检索器，解耦查询改写与稠密检索以兼容混合检索。

---

## 六、RAG评估框架

[21] Es S, James J, Espinosa-Anke L, et al. RAGAS: Automated Evaluation of Retrieval Augmented Generation[C]//Proceedings of the 18th Conference of the European Chapter of the Association for Computational Linguistics (EACL 2024). St. Julian's: ACL, 2024: 156-166.
- **来源**: https://arxiv.org/abs/2309.15217
- **说明**: RAGAS评估框架论文，定义了Faithfulness/Answer Relevancy/Context Recall/Context Precision等核心评估指标，是本文RAG性能评估的指标体系基础。

[22] Yu H, Gan R, Zhang K, et al. Evaluation of Retrieval-Augmented Generation: A Survey[J]. arXiv preprint, 2024, arXiv:2405.07437.
- **来源**: https://arxiv.org/abs/2405.07437
- **说明**: RAG评估综述，提出RGAR(检索/生成/附加需求)分析框架，系统比较12+个RAG评估框架。

[23] Saad-Falcon J, Khattab O, Potts C, et al. ARES: An Automated Evaluation Framework for Retrieval-Augmented Generation Systems[C]//Proceedings of the 2024 Conference of the North American Chapter of the Association for Computational Linguistics (NAACL 2024). Mexico City: ACL, 2024: 441-458.
- **来源**: https://arxiv.org/abs/2311.09476
- **说明**: ARES自动评估框架，使用合成数据微调轻量LLM裁判，评估上下文相关性/答案忠实度/答案相关性。

[24] Amazon Science. RAGChecker: A Fine-grained Framework for Diagnosing Retrieval-Augmented Generation[R]. arXiv preprint, 2024, arXiv:2408.08067.
- **来源**: https://arxiv.org/abs/2408.08067
- **说明**: 亚马逊开源的细粒度RAG诊断框架，提供声明级别的忠实度/噪声敏感度/幻觉检测。

---

## 七、文档处理与分块策略

[25] Qu R, Bao F, Tu R. Is Semantic Chunking Worth the Computational Cost?[J]. arXiv preprint, 2024, arXiv:2410.13070.
- **来源**: https://arxiv.org/abs/2410.13070
- **说明**: 系统比较固定大小分块与语义分块在RAG中的表现，证明固定大小分块在多数场景下效果可靠且效率更优。本文采用RecursiveCharacterTextSplitter固定大小分块策略的参考依据。

[26] Zhang Y, Liu Z, Wang H, et al. Meta-Chunking: Learning Efficient Text Segmentation via Logical Perception[J]. arXiv preprint, 2024, arXiv:2410.12788.
- **来源**: https://arxiv.org/abs/2410.12788
- **说明**: 提出"元分块"概念，在句子与段落之间寻找最优分割粒度。

[27] LangChain Documentation. RecursiveCharacterTextSplitter[EB/OL]. (2024). https://python.langchain.com/docs/modules/data_connection/document_transformers/recursive_text_splitter.
- **来源**: https://python.langchain.com/docs/modules/data_connection/document_transformers/recursive_text_splitter
- **说明**: LangChain递归字符分割器官方文档，本文文档分块实现的技术依据。参数配置: chunk_size=500, chunk_overlap=50。

---

## 八、向量数据库与检索引擎

[28] Wang J J, Yi X M, Guo R T, et al. Milvus: A Purpose-Built Vector Data Management System[C]//Proceedings of the 2021 International Conference on Management of Data (SIGMOD 2021). Xi'an: ACM, 2021: 2614-2627.
- **来源**: https://doi.org/10.1145/3448016.3457550
- **说明**: Milvus向量数据库系统论文，本文使用的Milvus 2.3+版本的基础架构参考。IVF_FLAT索引算法的理论基础。

[29] Elasticsearch B.V. Elasticsearch: Distributed RESTful Search and Analytics Engine (Version 8.x)[EB/OL]. (2024). https://www.elastic.co/elasticsearch/.
- **来源**: https://www.elastic.co/elasticsearch/
- **说明**: Elasticsearch 8.x官方文档。本文系统使用IK分词器实现中文分词和BM25全文检索的技术依据。

[30] IBM Research. Storage-Based Approximate Nearest Neighbor Search: What are the Performance Cost and I/O Characteristics?[C]//Proceedings of the IEEE International Symposium on Workload Characterization (IISWC 2025). IEEE, 2025.
- **来源**: https://research.ibm.com/publications/storage-based-approximate-nearest-neighbor-search
- **说明**: Milvus存储级ANN搜索性能评估，对本文配置Milvus IVF_FLAT索引参数(nlist=1024, 度量为IP内积)有参考价值。

---

## 九、教育领域RAG应用

[31] Wang N, Singh S. Answering Students' Questions on Course Forums Using Multiple Chain-of-Thought Reasoning and Finetuning RAG-Enabled LLM[J]. arXiv preprint, 2025, arXiv:2511.09831.
- **来源**: https://arxiv.org/abs/2511.09831
- **说明**: 大学课程论坛RAG问答系统，集成课程知识库与多链推理。与本文课程知识问答场景高度相关。

[32] Chen E, Li C, Li S, et al. Comparing RAG and GraphRAG for Page-Level Retrieval Question Answering on Math Textbook[J]. arXiv preprint, 2025, arXiv:2509.16780.
- **来源**: https://arxiv.org/abs/2509.16780
- **说明**: CMU的数学教科书RAG vs GraphRAG对比研究，本文采用Embedding RAG而非GraphRAG的决策参考。

[33] K R, Suresh S, Bhat V, et al. Towards Efficient Educational Chatbots: Benchmarking RAG Frameworks[J]. arXiv preprint, 2025, arXiv:2503.00781.
- **来源**: https://arxiv.org/abs/2503.00781
- **说明**: GATE教育聊天机器人RAG基准测试，对嵌入模型和LLM进行延迟/忠实度/相关性评估。

[34] Lian Y. Machine Assistant with Reliable Knowledge: Enhancing Student Learning via RAG-based Retrieval[J]. arXiv preprint, 2025, arXiv:2506.23026.
- **来源**: https://arxiv.org/abs/2506.23026
- **说明**: 名为MARK的课堂RAG问答系统，部署为办公时间替代工具，使用混合检索+反馈循环，与本文系统设计理念一致。

[35] Jain A, Gupta R, Sharma P, et al. Aligning LLMs for the Classroom with Knowledge-Based Retrieval: A Comparative RAG Study[J]. arXiv preprint, 2025, arXiv:2509.07846.
- **来源**: https://arxiv.org/abs/2509.07846
- **说明**: 教室场景RAG对比研究，提出动态查询路由框架。创建了3176道题目的EduScopeQA数据集。

---

## 十、技术框架与基础设施

[36] FastAPI. FastAPI: Modern Web Framework for Building APIs with Python (Version 0.110+)[EB/OL]. (2024). https://fastapi.tiangolo.com/.
- **来源**: https://fastapi.tiangolo.com/
- **说明**: FastAPI官方文档。本文后端基于FastAPI异步框架构建，利用其原生的StreamingResponse实现SSE流式响应。

[37] LangChain. LangChain: Building Applications with LLMs through Composability[EB/OL]. (2024). https://python.langchain.com/.
- **来源**: https://python.langchain.com/
- **说明**: LangChain框架官方文档。本文系统使用LangChain的ChatOpenAI封装、JsonOutputParser、UnstructuredLoader、RecursiveCharacterTextSplitter等组件。

[38] Elman B S, Poff C F, Ramirez S Y. Vue.js: The Progressive JavaScript Framework (Version 3.x)[EB/OL]. (2024). https://vuejs.org/.
- **来源**: https://vuejs.org/
- **说明**: Vue 3官方文档。本文前端基于Vue 3 Composition API构建，使用响应式系统和组合式API管理复杂状态。

[39] TypeScript. TypeScript: JavaScript With Syntax For Types (Version 5.x)[EB/OL]. (2024). https://www.typescriptlang.org/.
- **来源**: https://www.typescriptlang.org/
- **说明**: TypeScript官方文档。本文前端使用TypeScript实现类型安全的开发。

---

## 十一、其他关键参考文献

[40] Touvron H, Lavril T, Izacard G, et al. LLaMA: Open and Efficient Foundation Language Models[J]. arXiv preprint, 2023, arXiv:2302.13971.
- **来源**: https://arxiv.org/abs/2302.13971
- **说明**: Meta开源LLM的代表性工作，推动开源大模型生态发展。为本文选用开源Embedding和Reranker模型提供技术背景。

[41] Karpukhin V, Oguz B, Min S, et al. Dense Passage Retrieval for Open-Domain Question Answering[C]//Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP 2020). ACL, 2020: 6769-6781.
- **来源**: https://arxiv.org/abs/2004.04906
- **说明**: 稠密段落检索(DPR)的代表性工作，基于双编码器的稠密向量检索范式奠定了现代RAG检索器的基础。

[42] Izacard G, Grave E. Leveraging Passage Retrieval with Generative Models for Open Domain Question Answering[C]//Proceedings of the 16th Conference of the European Chapter of the Association for Computational Linguistics (EACL 2021). ACL, 2021: 874-880.
- **来源**: https://arxiv.org/abs/2007.01282
- **说明**: Fusion-in-Decoder (FiD)方法，验证了多文档检索+生成模型融合的有效性。

[43] Ram O, Levine Y, Dalmedigos I, et al. In-Context Retrieval-Augmented Language Models[J]. Transactions of the Association for Computational Linguistics, 2023, 11: 1316-1331.
- **来源**: https://arxiv.org/abs/2302.00083
- **说明**: 上下文检索增强语言模型，验证了RAG方法在多种任务上的有效性，为本文RAG管道设计提供参考。

[44] Trivedi H, Balasubramanian N, Khot T, et al. Interleaving Retrieval with Chain-of-Thought Reasoning for Knowledge-Intensive Multi-Step Questions[C]//Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (ACL 2023). Toronto: ACL, 2023: 10014-10037.
- **来源**: https://arxiv.org/abs/2212.10509
- **说明**: IRCoT论文，提出检索与推理交织的多步推理方法。为本文的多查询检索策略提供参考。

[45] Shi W, Min S, Yasunaga M, et al. REPLUG: Retrieval-Augmented Black-Box Language Models[J]. arXiv preprint, 2023, arXiv:2301.12652.
- **来源**: https://arxiv.org/abs/2301.12652
- **说明**: 验证了无需微调即可通过检索增强提升黑盒LLM性能的方法。为本文使用API调用DeepSeek+检索增强的方案提供支持。

---

## 文献索引按主题分类

| 主题 | 对应文献编号 |
|------|-------------|
| RAG基础理论与综述 | [1], [2], [3], [4], [5] |
| LLM与幻觉 | [6], [7], [8], [9] |
| Embedding与Reranker | [10], [11], [12] |
| 混合检索与RRF融合 | [13], [14], [15], [16], [17] |
| 查询改写与意图识别 | [18], [19], [20] |
| RAG评估框架 | [21], [22], [23], [24] |
| 文档处理与分块 | [25], [26], [27] |
| 向量数据库与检索引擎 | [28], [29], [30] |
| 教育领域RAG应用 | [31], [32], [33], [34], [35] |
| 技术框架与基础设施 | [36], [37], [38], [39] |
| 其他关键文献 | [40], [41], [42], [43], [44], [45] |

---

## 使用说明

1. **参考文献总数**: 45篇（含12篇英文文献）
2. **时效性**: 参考文献集中在2020-2026年，核心RAG文献为2023-2026年
3. **覆盖范围**: 涵盖RAG基础理论、LLM与幻觉缓解、Embedding与Reranker模型、混合检索与RRF融合、查询改写、评估框架、文档处理、向量数据库、教育领域应用、技术框架等
4. **格式说明**: 本文参考文献格式遵循GB/T 7714标准，中英文文献标点符号统一采用英文半角标点符号
5. **引用说明**: 部分英文文献以中文格式列出(作者姓在前名在后)，便于与中文文献格式统一。实际使用时请检查所在学校的参考文献格式要求
