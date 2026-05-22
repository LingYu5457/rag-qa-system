"""
为论文添加参考文献引用标记和参考文献列表。
两步走：先用占位符插入引用，再按首次出现顺序重新编号。
"""
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
import re

# ============================================================
# 参考文献数据（按引用ID索引，排序由程序自动确定）
# ============================================================
ref_data = {
    'REF_HALLUCINATION': (
        'Alansari A, Luqman H. A Comprehensive Survey of Hallucination in Large Language Models: '
        'Causes, Detection, and Mitigation[EB/OL]. 2025-10-13[2026-05-19]. '
        'https://arxiv.org/abs/2510.06265.'
    ),
    'REF_RAG_LEWIS': (
        'Lewis P, Perez E, Piktus A, et al. Retrieval-Augmented Generation for Knowledge-Intensive '
        'NLP Tasks[C]//Advances in Neural Information Processing Systems (NeurIPS 2020). '
        'Vancouver: Curran Associates, 2020: 9459-9474.'
    ),
    'REF_RAG_SURVEY_GAO': (
        'Gao Y F, Xiong Y, Gao X Y, et al. Retrieval-Augmented Generation for Large Language '
        'Models: A Survey[EB/OL]. 2024-03-05[2026-05-19]. '
        'https://arxiv.org/abs/2312.10997.'
    ),
    'REF_BM25': (
        'Robertson S, Zaragoza H. The Probabilistic Relevance Framework: BM25 and Beyond[J]. '
        'Foundations and Trends in Information Retrieval, 2009, 3(4): 333-389.'
    ),
    'REF_DPR': (
        'Karpukhin V, Oguz B, Min S, et al. Dense Passage Retrieval for Open-Domain Question '
        'Answering[C]//Proceedings of the 2020 Conference on Empirical Methods in Natural Language '
        'Processing (EMNLP 2020). Online: ACL, 2020: 6769-6781.'
    ),
    'REF_COSMIX': (
        'Juvekar K, Purwar A. COS-Mix: Cosine Similarity and Distance Fusion for Improved '
        'Information Retrieval[EB/OL]. 2024-06-03[2026-05-19]. '
        'https://arxiv.org/abs/2406.00638.'
    ),
    'REF_BGE_RERANKER': (
        'Chen J L, Xiao S T, Zhang P T, et al. BGE-Reranker-V2: Cross-Encoder Reranking for '
        'Retrieval-Augmented Generation[EB/OL]. 2024-03-19[2026-05-19]. '
        'https://huggingface.co/BAAI/bge-reranker-v2-m3.'
    ),
    'REF_REPLUG': (
        'Shi W, Min S, Yasunaga M, et al. REPLUG: Retrieval-Augmented Black-Box Language '
        'Models[EB/OL]. 2023-01-25[2026-05-19]. '
        'https://arxiv.org/abs/2301.12652.'
    ),
    'REF_EDU_WANG': (
        'Wang N, Singh S. Answering Students\' Questions on Course Forums Using Multiple '
        'Chain-of-Thought Reasoning and Finetuning RAG-Enabled LLM[EB/OL]. 2025-11-20[2026-05-19]. '
        'https://arxiv.org/abs/2511.09831.'
    ),
    'REF_VUE': (
        'Elman B S, Poff C F, Ramirez S Y. Vue.js: The Progressive JavaScript Framework '
        '(Version 3.x)[EB/OL]. 2024[2026-05-19]. '
        'https://vuejs.org/.'
    ),
    'REF_TYPESCRIPT': (
        'Microsoft. TypeScript: JavaScript With Syntax For Types (Version 5.x)[EB/OL]. '
        '2024[2026-05-19]. '
        'https://www.typescriptlang.org/.'
    ),
    'REF_FASTAPI': (
        'FastAPI. FastAPI: Modern Web Framework for Building APIs with Python '
        '(Version 0.110+)[EB/OL]. 2024[2026-05-19]. '
        'https://fastapi.tiangolo.com/.'
    ),
    'REF_MILVUS': (
        'Wang J J, Yi X M, Guo R T, et al. Milvus: A Purpose-Built Vector Data Management '
        'System[C]//Proceedings of the 2021 International Conference on Management of Data '
        '(SIGMOD 2021). Xi\'an: ACM, 2021: 2614-2627.'
    ),
    'REF_ES': (
        'Elasticsearch B V. Elasticsearch: Distributed RESTful Search and Analytics Engine '
        '(Version 8.x)[EB/OL]. 2024[2026-05-19]. '
        'https://www.elastic.co/elasticsearch/.'
    ),
    'REF_DEEPSEEK': (
        'DeepSeek-AI. DeepSeek-V4 Technical Report[EB/OL]. 2026[2026-05-19]. '
        'https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash.'
    ),
    'REF_BGE_M3': (
        'Chen J L, Xiao S T, Zhang P T, et al. BGE M3-Embedding: Multi-Lingual, Multi-Functionality, '
        'Multi-Granularity Text Embeddings Through Self-Knowledge Distillation[EB/OL]. '
        '2024-02-05[2026-05-19]. '
        'https://arxiv.org/abs/2402.03216.'
    ),
    'REF_CPACK': (
        'Xiao S T, Liu Z, Zhang P T, et al. C-Pack: Packaged Resources To Advance General '
        'Chinese Embedding[EB/OL]. 2023-09-14[2026-05-19]. '
        'https://arxiv.org/abs/2309.07597.'
    ),
    'REF_LANGCHAIN': (
        'LangChain. LangChain: Building Applications with LLMs through Composability[EB/OL]. '
        '2024[2026-05-19]. '
        'https://python.langchain.com/.'
    ),
    'REF_CHUNKING': (
        'Qu R, Bao F, Tu R. Is Semantic Chunking Worth the Computational Cost?[EB/OL]. '
        '2024-10-16[2026-05-19]. '
        'https://arxiv.org/abs/2410.13070.'
    ),
    'REF_RRF': (
        'Cormack G V, Clarke C L A, Büttcher S. Reciprocal Rank Fusion Outperforms Condorcet '
        'and Individual Rank Learning Methods[C]//Proceedings of the 32nd International ACM SIGIR '
        'Conference on Research and Development in Information Retrieval (SIGIR 2009). '
        'Boston: ACM, 2009: 758-759.'
    ),
    'REF_DMQR': (
        'Li Y, Wang Z, Zhang H, et al. DMQR-RAG: Diverse Multi-Query Rewriting for RAG[EB/OL]. '
        '2024-11-19[2026-05-19]. '
        'https://arxiv.org/abs/2411.13154.'
    ),
    'REF_RAGAS': (
        'Es S, James J, Espinosa-Anke L, et al. RAGAS: Automated Evaluation of Retrieval '
        'Augmented Generation[C]//Proceedings of the 18th Conference of the European Chapter '
        'of the Association for Computational Linguistics (EACL 2024). '
        'St. Julian\'s: ACL, 2024: 150-158.'
    ),
    'REF_EVAL_SURVEY': (
        'Yu H, Gan R, Zhang K, et al. Evaluation of Retrieval-Augmented Generation: '
        'A Survey[EB/OL]. 2024-05-13[2026-05-19]. '
        'https://arxiv.org/abs/2405.07437.'
    ),
    'REF_LLAMA': (
        'Touvron H, Lavril T, Izacard G, et al. LLaMA: Open and Efficient Foundation Language '
        'Models[EB/OL]. 2023-02-27[2026-05-19]. '
        'https://arxiv.org/abs/2302.13971.'
    ),
    'REF_FID': (
        'Izacard G, Grave E. Leveraging Passage Retrieval with Generative Models for Open Domain '
        'Question Answering[C]//Proceedings of the 16th Conference of the European Chapter of '
        'the Association for Computational Linguistics (EACL 2021). '
        'Online: ACL, 2021: 874-880.'
    ),
    'REF_RALM': (
        'Ram O, Levine Y, Dalmedigos I, et al. In-Context Retrieval-Augmented Language Models[J]. '
        'Transactions of the Association for Computational Linguistics, 2023, 11: 1316-1331.'
    ),
    'REF_IRCOT': (
        'Trivedi H, Balasubramanian N, Khot T, et al. Interleaving Retrieval with Chain-of-Thought '
        'Reasoning for Knowledge-Intensive Multi-Step Questions[C]//Proceedings of the 61st Annual '
        'Meeting of the Association for Computational Linguistics (ACL 2023). '
        'Toronto: ACL, 2023: 10014-10037.'
    ),
    'REF_EDU_BENCHMARK': (
        'K R, Suresh S, Bhat V, et al. Towards Efficient Educational Chatbots: Benchmarking '
        'RAG Frameworks[EB/OL]. 2025-03-02[2026-05-19]. '
        'https://arxiv.org/abs/2503.00781.'
    ),
    'REF_MARK': (
        'Lian Y. Machine Assistant with Reliable Knowledge: Enhancing Student Learning via '
        'RAG-based Retrieval[EB/OL]. 2025-06-30[2026-05-19]. '
        'https://arxiv.org/abs/2506.23026.'
    ),
    'REF_RAG_FUSION': (
        'Rackauckas Z. RAG-Fusion: A New Take on Retrieval-Augmented Generation[EB/OL]. '
        '2024-02-06[2026-05-19]. '
        'https://arxiv.org/abs/2402.03367.'
    ),
    'REF_RAG_SURVEY_SHARMA': (
        'Sharma R. Retrieval-Augmented Generation: A Comprehensive Survey of Architectures, '
        'Enhancements, and Robustness Frontiers[EB/OL]. 2025-06-02[2026-05-19]. '
        'https://arxiv.org/abs/2506.00054.'
    ),
    'REF_HYBRID_DOMAIN': (
        'Sultania D, Chen Y, Gupta R, et al. Domain-specific Question Answering with Hybrid '
        'Search[EB/OL]. 2024-12-05[2026-05-19]. '
        'https://arxiv.org/abs/2412.03736.'
    ),
}

# ============================================================
# 引用插入列表：(搜索文本, 替换文本含占位符{REF_XXX})
# ============================================================
citations = [
    # ---- 第一章 绪论 ----
    # P48: LLM发展背景
    (
        "大语言模型（Large Language Model，LLM）在自然语言处理领域取得了突破性的进展",
        "大语言模型（Large Language Model，LLM）在自然语言处理领域取得了突破性的进展{REF_LLAMA}"
    ),
    # P48: 幻觉问题
    (
        "即大模型的幻觉（Hallucination）问题。",
        "即大模型的幻觉（Hallucination）问题{REF_HALLUCINATION}。"
    ),
    # P49: RAG技术出现
    (
        "检索增强生成（Retrieval-Augmented Generation，RAG）技术的出现提供了有效的解决方案",
        "检索增强生成（Retrieval-Augmented Generation，RAG）技术的出现提供了有效的解决方案{REF_RAG_LEWIS}"
    ),
    # P49: 非参数化知识作为上下文
    (
        "将非参数化的知识作为上下文提供给大语言模型，使其回答有据可循",
        "将非参数化的知识作为上下文提供给大语言模型，使其回答有据可循{REF_RALM}"
    ),
    # P49: RAG核心 - 知识作为外部输入(再次提及RAG)
    (
        "只需要将知识作为外部输入，大语言模型就能理解并生成可靠的回答。",
        "只需要将知识作为外部输入，大语言模型就能理解并生成可靠的回答{REF_RAG_LEWIS}。"
    ),
    # P56: Lewis RAG论文明确提及处
    (
        "RAG的概念最早由Lewis等人于2020年在论文《Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks》中提出",
        "RAG的概念最早由Lewis等人于2020年在论文《Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks》中提出{REF_RAG_LEWIS}"
    ),
    # P56: RAG范式分类 + 2025综述
    (
        "比如原始的RAG、引入了查询重写和重排序等模块高级RAG、具有可插拔的管道式设计的模块化RAG等等方式。",
        "比如原始的RAG、引入了查询重写和重排序等模块高级RAG、具有可插拔的管道式设计的模块化RAG等等方式{REF_RAG_SURVEY_GAO}{REF_RAG_SURVEY_SHARMA}。"
    ),
    # P56: BM25稀疏检索
    (
        "早期系统依赖基于关键词比如BM25的稀疏检索",
        "早期系统依赖基于关键词比如BM25的稀疏检索{REF_BM25}"
    ),
    # P56: FiD多文档检索
    (
        "但该方法无法捕获查询与文档之间的语义关联。之后随着Embedding模型的发展，",
        "但该方法无法捕获查询与文档之间的语义关联{REF_FID}。之后随着Embedding模型的发展，"
    ),
    # P56: DPR稠密向量检索
    (
        "稠密向量检索逐渐成为主流，通过将查询和文档映射到同一向量空间进行相似度计算，能够实现语义层面的匹配。",
        "稠密向量检索逐渐成为主流，通过将查询和文档映射到同一向量空间进行相似度计算，能够实现语义层面的匹配{REF_DPR}。"
    ),
    # P56: 混合检索 + Domain QA
    (
        "混合检索（Hybrid Search）结合稀疏和稠密检索的优势，成为RAG系统提升召回效果的重要手段。",
        "混合检索（Hybrid Search）结合稀疏和稠密检索的优势，成为RAG系统提升召回效果的重要手段{REF_COSMIX}{REF_HYBRID_DOMAIN}。"
    ),
    # P56: Cross-encoder重排序
    (
        "交叉编码（Cross-encoder）结构的重排序模型对查询和文档进行联合编码，能够更加精细地评估相关性，通常作为检索后处理的精排环节。",
        "交叉编码（Cross-encoder）结构的重排序模型对查询和文档进行联合编码，能够更加精细地评估相关性，通常作为检索后处理的精排环节{REF_BGE_RERANKER}。"
    ),
    # P57: Perplexity AI + REPLUG
    (
        "Perplexity AI将检索过程与生成过程深度整合，在回答中标注信息来源，为用户提供了可验证的问答体验。",
        "Perplexity AI将检索过程与生成过程深度整合，在回答中标注信息来源，为用户提供了可验证的问答体验{REF_REPLUG}。"
    ),
    # P57: Khanmigo + 教育RAG基准
    (
        "Khan Academy与GPT-4合作推出的Khanmigo能够为学生提供个性化的学习辅导，包括课程问答、代码调试、写作辅助等功能。",
        "Khan Academy与GPT-4合作推出的Khanmigo能够为学生提供个性化的学习辅导，包括课程问答、代码调试、写作辅助等功能{REF_EDU_WANG}{REF_EDU_BENCHMARK}。"
    ),
    # P57: 高校RAG
    (
        "高校里，部分研究团队开始探索将RAG技术应用于课程教学，如构建课程知识库、开发智能编程助手等。",
        "高校里，部分研究团队开始探索将RAG技术应用于课程教学，如构建课程知识库、开发智能编程助手等{REF_MARK}。"
    ),
    # ---- 第二章 相关技术分析 ----
    # P74: Vue 3
    (
        "Vue 3是一套用于构建用户界面的渐进式JavaScript框架。",
        "Vue 3是一套用于构建用户界面的渐进式JavaScript框架{REF_VUE}。"
    ),
    # P75: TypeScript
    (
        "TypeScript是微软开发的开源编程语言，是JavaScript的超集",
        "TypeScript是微软开发的开源编程语言，是JavaScript的超集{REF_TYPESCRIPT}"
    ),
    # P79: FastAPI
    (
        "FastAPI是一个基于Python的现代Web框架，专为构建API而设计。",
        "FastAPI是一个基于Python的现代Web框架，专为构建API而设计{REF_FASTAPI}。"
    ),
    # P84: Milvus
    (
        "Milvus是一款开源的向量数据库，专为大规模向量数据的存储、索引和检索而设计。",
        "Milvus是一款开源的向量数据库，专为大规模向量数据的存储、索引和检索而设计{REF_MILVUS}。"
    ),
    # P85: Elasticsearch
    (
        "Elasticsearch是基于Apache Lucene构建的分布式全文检索引擎，提供准实时的搜索能力。",
        "Elasticsearch是基于Apache Lucene构建的分布式全文检索引擎，提供准实时的搜索能力{REF_ES}。"
    ),
    # P85: BM25 in ES context
    (
        "其核心检索算法为BM25，是对传统TF-IDF算法的改进，引入了文档长度归一化因子",
        "其核心检索算法为BM25，是对传统TF-IDF算法的改进，引入了文档长度归一化因子{REF_BM25}"
    ),
    # P87: DeepSeek
    (
        "DeepSeek是由深度求索公司研发的大语言模型。",
        "DeepSeek是由深度求索公司研发的大语言模型{REF_DEEPSEEK}。"
    ),
    # P88: BGE-M3
    (
        "bge-m3是由北京智源人工智能研究院（BAAI）开源的Embedding模型",
        "bge-m3是由北京智源人工智能研究院（BAAI）开源的Embedding模型{REF_BGE_M3}"
    ),
    # P88: C-Pack BGE基础
    (
        "模型支持多语言（中英文混合）和稠密检索与稀疏检索的双重输出。",
        "模型支持多语言（中英文混合）和稠密检索与稀疏检索的双重输出{REF_CPACK}。"
    ),
    # P89: BGE-Reranker (复用 REF_BGE_RERANKER)
    (
        "bge-reranker-v2-m3是BAAI开源的交叉编码器（Cross-encoder）重排序模型。",
        "bge-reranker-v2-m3是BAAI开源的交叉编码器（Cross-encoder）重排序模型{REF_BGE_RERANKER}。"
    ),
    # P91: LangChain
    (
        "LangChain是一个用于构建LLM应用的开源框架，提供了丰富的文档加载器和文本分割器。",
        "LangChain是一个用于构建LLM应用的开源框架，提供了丰富的文档加载器和文本分割器{REF_LANGCHAIN}。"
    ),
    # P91: RecursiveCharacterTextSplitter / chunking
    (
        "分割策略采用chunk_size=500字符、chunk_overlap=50字符的参数设置，在保证语义完整性的同时控制文本块大小在模型上下文窗口内。",
        "分割策略采用chunk_size=500字符、chunk_overlap=50字符的参数设置，在保证语义完整性的同时控制文本块大小在模型上下文窗口内{REF_CHUNKING}。"
    ),
    # ---- 第三章 系统分析 ----
    # P124: 意图路由 IRCoT
    (
        "系统将根据不同的结果进入不同的分支之中。",
        "系统将根据不同的结果进入不同的分支之中{REF_IRCOT}。"
    ),
    # P124: 查询改写 DMQR
    (
        "用户问题重写完成之后将传递给混合检索模块",
        "用户问题重写完成之后将传递给混合检索模块{REF_DMQR}"
    ),
    # P124: RRF融合 + RAG-Fusion
    (
        "两路返回结果后会经行RRF融合，只保留部分。",
        "两路返回结果后会经行RRF融合，只保留部分{REF_RRF}{REF_RAG_FUSION}。"
    ),
    # ---- 第五章 系统实现 ----
    # RRF算法(再次引用)
    # P248: RRF算法描述 - 标记在代码注释中(代码在附录中,不需要引用于正文列表)
    # 代码注释中的"RRF融合算法"不做正文引用
    # ---- 第六章 系统测试 ----
    # P302: RAGAS + 评估综述
    (
        "RAG质量评估通过独立评估模块evaluate实现。",
        "RAG质量评估通过独立评估模块evaluate实现{REF_EVAL_SURVEY}。"
    ),
    # P302: RAGAS四个维度
    (
        "忠实性（Faithfulness）评估可从上下文推断的陈述比例、答案相关性（Answer Relevancy）评估回答与问题的相关程度、上下文召回率（Context Recall）评估标准答案信息被上下文覆盖的比例、上下文精确率（Context Precision）评估检索上下文中有用信息的比例。",
        "忠实性（Faithfulness）评估可从上下文推断的陈述比例、答案相关性（Answer Relevancy）评估回答与问题的相关程度、上下文召回率（Context Recall）评估标准答案信息被上下文覆盖的比例、上下文精确率（Context Precision）评估检索上下文中有用信息的比例{REF_RAGAS}。"
    ),
]


def replace_text_in_paragraph(para, old_text, new_text):
    """在段落中查找并替换文本，正确处理跨越多个runs的情况"""
    full_text = para.text
    if old_text not in full_text:
        return False

    runs = para.runs
    if not runs:
        return False

    # 构建 run 到文本位置的映射
    positions = []
    current_pos = 0
    for run in runs:
        run_len = len(run.text) if run.text else 0
        positions.append((run, current_pos, current_pos + run_len))
        current_pos += run_len

    match_start = full_text.find(old_text)
    match_end = match_start + len(old_text)

    # 确定哪些 runs 包含匹配文本
    affected_runs = []
    for run, run_start, run_end in positions:
        if run_end > match_start and run_start < match_end:
            affected_runs.append((run, run_start, run_end))

    if not affected_runs:
        return False

    # 单个run的情况
    if len(affected_runs) == 1:
        run, run_start, run_end = affected_runs[0]
        local_start = match_start - run_start
        local_end = match_end - run_start
        run.text = run.text[:local_start] + new_text + run.text[local_end:]
        return True

    # 多个run的情况：在第一个run中替换匹配开始到run结束的部分
    first_run, first_start, first_end = affected_runs[0]
    local_start = match_start - first_start
    first_run.text = first_run.text[:local_start] + new_text

    # 清空中间和最后一个run中属于匹配的部分
    for run, rs, re in affected_runs[1:]:
        local_s = max(0, match_start - rs)
        local_e = min(len(run.text), match_end - rs)
        if local_e >= len(run.text):
            run.text = ''
        else:
            run.text = run.text[local_e:]

    return True


def apply_citations(doc):
    """第一阶段：用占位符替换引用标记"""
    modified = 0
    unmatched = []

    for search, replace in citations:
        found = False
        for para in doc.paragraphs:
            if search in para.text:
                replace_text_in_paragraph(para, search, replace)
                modified += 1
                found = True
                break
        if not found:
            unmatched.append(search[:80])

    print(f"第一阶段：成功插入 {modified}/{len(citations)} 处引用占位符")
    if unmatched:
        print(f"未匹配 {len(unmatched)} 处:")
        for u in unmatched:
            print(f"  - {u}")
    return modified


def collect_appearance_order(doc, ref_heading_idx):
    """扫描正文，按首次出现顺序收集引用ID"""
    appearance_order = []
    seen = set()

    placeholder_pattern = re.compile(r'\{REF_(\w+)\}')

    for i in range(ref_heading_idx):
        text = doc.paragraphs[i].text
        for match in placeholder_pattern.finditer(text):
            ref_id = f'REF_{match.group(1)}'
            if ref_id not in seen:
                seen.add(ref_id)
                appearance_order.append(ref_id)

    print(f"第二阶段：发现 {len(appearance_order)} 个唯一引用ID")
    return appearance_order, seen


def renumber_citations(doc, ref_heading_idx, appearance_order):
    """将占位符替换为最终编号[1], [2], ..."""
    id_to_num = {ref_id: i+1 for i, ref_id in enumerate(appearance_order)}

    for i in range(ref_heading_idx):
        para = doc.paragraphs[i]
        text = para.text
        new_text = re.sub(r'\{REF_(\w+)\}', lambda m: f'[{id_to_num.get(f"REF_{m.group(1)}", "?")}]', text)
        if new_text != text:
            # Replace all runs
            runs = para.runs
            if runs:
                for run in runs:
                    run.text = ''
                runs[0].text = new_text

    print(f"第三阶段：占位符已替换为连续编号 [1]~[{len(appearance_order)}]")
    return id_to_num


def clear_and_write_references(doc, appearance_order, id_to_num):
    """清空参考文献部分并写入排序后的列表"""
    ref_heading_idx = None
    for i, para in enumerate(doc.paragraphs):
        if para.text.strip() == '参考文献':
            ref_heading_idx = i
            break

    if ref_heading_idx is None:
        print("未找到'参考文献'标题！")
        return

    # 找到附录位置
    appendix_idx = None
    for i in range(ref_heading_idx + 1, len(doc.paragraphs)):
        if '附  录' in doc.paragraphs[i].text:
            appendix_idx = i
            break
    if appendix_idx is None:
        appendix_idx = len(doc.paragraphs)

    # 删除参考文献标题和附录之间的现有段落
    body = doc.element.body
    paras_to_remove = []
    for i, para in enumerate(doc.paragraphs):
        if ref_heading_idx < i < appendix_idx:
            paras_to_remove.append(para._element)
    for elem in paras_to_remove:
        body.remove(elem)

    # 在参考文献标题后插入参考文献条目
    ref_element = doc.paragraphs[ref_heading_idx]._element
    insert_after = ref_element

    for ref_id in appearance_order:
        ref_text = ref_data.get(ref_id)
        if ref_text is None:
            continue

        num = id_to_num[ref_id]
        # 创建新段落
        p = ref_element.makeelement(ref_element.tag, {})

        # 设置段落属性 (左对齐，无缩进，顶格)
        pPr = p.makeelement(qn('w:pPr'), {})
        p.append(pPr)
        jc = pPr.makeelement(qn('w:jc'), {qn('w:val'): 'left'})
        pPr.append(jc)
        # 取消首行缩进
        ind = pPr.makeelement(qn('w:ind'), {qn('w:firstLine'): '0', qn('w:left'): '0'})
        pPr.append(ind)

        # 添加 run
        r = p.makeelement(qn('w:r'), {})
        p.append(r)

        # 设置 run 属性（字体）
        rPr = r.makeelement(qn('w:rPr'), {})
        r.append(rPr)
        rFonts = rPr.makeelement(qn('w:rFonts'), {
            qn('w:ascii'): 'Times New Roman',
            qn('w:hAnsi'): 'Times New Roman',
            qn('w:eastAsia'): '宋体',
        })
        rPr.append(rFonts)
        sz = rPr.makeelement(qn('w:sz'), {qn('w:val'): '24'})  # 12pt
        rPr.append(sz)

        # 添加文本
        t = r.makeelement(qn('w:t'), {})
        t.text = f'[{num}] {ref_text}'
        t.set(qn('xml:space'), 'preserve')
        r.append(t)

        insert_after.addnext(p)
        insert_after = p

    print(f"已写入 {len(appearance_order)} 条参考文献")


def main():
    input_path = '论文2.0.docx'
    output_path = '论文2.0_含参考文献.docx'

    print(f"读取文档: {input_path}")
    doc = Document(input_path)

    # 找到参考文献标题位置
    ref_heading_idx = None
    for i, para in enumerate(doc.paragraphs):
        if para.text.strip() == '参考文献':
            ref_heading_idx = i
            break

    if ref_heading_idx is None:
        print("错误：未找到'参考文献'标题！")
        return

    # 第一阶段：插入占位符
    apply_citations(doc)

    # 第二阶段：扫描首次出现顺序
    appearance_order, seen_ids = collect_appearance_order(doc, ref_heading_idx)

    # 检查是否有引用占位符未出现在正文中
    for ref_id in ref_data:
        if ref_id not in seen_ids:
            print(f"警告：{ref_id} 未在正文中引用")

    # 第三阶段：替换占位符为连续编号
    id_to_num = renumber_citations(doc, ref_heading_idx, appearance_order)

    # 第四阶段：写入参考文献列表
    clear_and_write_references(doc, appearance_order, id_to_num)

    print(f"保存副本: {output_path}")
    doc.save(output_path)
    print("完成！")


if __name__ == '__main__':
    main()
