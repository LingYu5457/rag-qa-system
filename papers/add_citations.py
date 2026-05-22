"""
Add citation markers and references section to the thesis docx.
Strategy: Add citations at the end of relevant paragraphs.
References ordered by first appearance in the text.
"""
import shutil
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

# Backup first
shutil.copy('papers/论文2.0.docx', 'papers/论文2.0_backup.docx')
print("Backup created: papers/论文2.0_backup.docx")

doc = Document('papers/论文2.0.docx')

# ============================================================
# REFERENCE ORDER (by first appearance in text body)
# ============================================================
# [1]  DeepSeek-V4 tech report (refs.md [6])
# [2]  Alansari & Luqman 2025 - Hallucination survey (refs.md [7])
# [3]  Lewis et al. 2020 - RAG original (refs.md [1])
# [4]  Shi et al. 2023 - REPLUG (refs.md [45])
# [5]  Gao et al. 2024 - RAG survey (refs.md [2])
# [6]  Robertson & Zaragoza 2009 - BM25 (refs.md [17])
# [7]  Karpukhin et al. 2020 - DPR (refs.md [41])
# [8]  Juvekar & Purwar 2024 - COS-Mix hybrid search (refs.md [15])
# [9]  Xiao et al. 2023 - C-Pack/BGE (refs.md [11])
# [10] Wang & Singh 2025 - Education RAG (refs.md [31])
# [11] Lian 2025 - MARK education RAG (refs.md [34])
# [12] Vue.js docs (refs.md [38])
# [13] TypeScript docs (refs.md [39])
# [14] FastAPI docs (refs.md [36])
# [15] Milvus - Wang et al. 2021 (refs.md [28])
# [16] Elasticsearch docs (refs.md [29])
# [17] BGE M3 - Chen et al. 2024 (refs.md [10])
# [18] BGE-Reranker-V2 (refs.md [12])
# [19] LangChain docs (refs.md [37])
# [20] RecursiveCharacterTextSplitter docs (refs.md [27])
# [21] Qu et al. 2024 - Semantic chunking (refs.md [25])
# [22] Cormack et al. 2009 - RRF (refs.md [13])
# [23] Rackauckas 2024 - RAG-Fusion (refs.md [14])
# [24] Li et al. 2024 - DMQR-RAG (refs.md [18])
# [25] Es et al. 2024 - RAGAS (refs.md [21])
# [26] Yu et al. 2024 - RAG evaluation survey (refs.md [22])
# [27] Saad-Falcon et al. 2024 - ARES (refs.md [23])
# [28] Bansal & Agarwal 2026 - Latest RAG survey (refs.md [4])
# [29] Sharma 2025 - Comprehensive RAG survey (refs.md [3])
# [30] Sultania et al. 2024 - Domain hybrid search (refs.md [16])
# [31] Li et al. 2025 - Hallucination survey (refs.md [9])
# [32] Izacard & Grave 2021 - FiD (refs.md [42])

# ============================================================
# CITATION PLACEMENT MAP: paragraph_index -> [citation_numbers]
# ============================================================
# Paragraph indices are from the extracted text mapping
citation_map = {
    # Ch1 研究背景 P48: LLM/ChatGPT/DeepSeek + Hallucination + fine-tuning issues
    48: [1, 2, 31],
    # Ch1 P49: RAG concept + external knowledge approach
    49: [3, 4],
    # Ch1 研究现状 P56: RAG paradigms, BM25, dense retrieval, hybrid, rerank, multi-doc
    56: [5, 6, 7, 8, 9, 32],
    # Ch1 P57: Education RAG applications
    57: [10, 11],
    # Ch2 P74: Vue 3
    74: [12],
    # Ch2 P75: TypeScript
    75: [13],
    # Ch2 P79: FastAPI
    79: [14],
    # Ch2 P84: Milvus
    84: [15],
    # Ch2 P85: Elasticsearch + BM25 + domain hybrid search approach
    85: [6, 16, 30],
    # Ch2 P87: DeepSeek-V4-Flash (already [1], reinforce)
    87: [1],
    # Ch2 P88: BGE-M3 embedding model
    88: [17],
    # Ch2 P89: BGE-Reranker-V2 cross-encoder
    89: [9, 18],
    # Ch2 P91: LangChain + RecursiveCharacterTextSplitter + chunking strategy
    91: [19, 20, 21],
    # Ch3 P124: RRF fusion + dual-path retrieval (BM25 + vector)
    124: [6, 7, 22, 23],
    # Ch5 P239: Query rewriting
    239: [24],
    # Ch3 P100: cost/economic feasibility (API cost models reference)
    # Skip - general statement
    # Ch6 P302: RAG evaluation methodology (RAGAS + ARES + eval survey)
    302: [25, 26, 27],
    # Ch6 P303: "6.3.2评估结果与分析" - heading, no citation needed
    # Ch7 P333: future improvements (Late Chunking, ColBERT, etc.)
    333: [28, 29],
    # Additional: Ch2 P93 本章小结 - already covered
    # Additional: Ch4 P139 - architecture (DeepSeek, BGE-M3, BGE-Reranker mentioned again)
    139: [1, 17, 18],
    # Additional: Ch4 P164/P165 - Milvus/ES storage (already cited)
    # Additional: Ch5 P248 - RRF implementation details
    248: [22],
    # Additional: P57 adds more context about Perplexity/hybrid search in products
    # P57 also mentions 豆包、通义千问 etc.
}

# Deduplicate citation lists within each paragraph
for k in citation_map:
    seen = set()
    deduped = []
    for c in citation_map[k]:
        if c not in seen:
            seen.add(c)
            deduped.append(c)
    citation_map[k] = deduped

# ============================================================
# HELPER: Get the last text-containing run of a paragraph
# ============================================================
def get_last_text_run(para):
    """Return the last run that has text content."""
    last = None
    for run in para.runs:
        if run.text.strip():
            last = run
    return last


def add_citation_to_para(doc, para_index, citation_numbers):
    """Add citation markers like [1][2] to end of paragraph."""
    if para_index >= len(doc.paragraphs):
        print(f"  WARNING: para index {para_index} out of range (max {len(doc.paragraphs)-1})")
        return False

    para = doc.paragraphs[para_index]
    text = para.text.strip()
    if not text:
        print(f"  SKIP para {para_index}: empty text")
        return False

    # Build citation string
    citation_str = ''.join(f'[{n}]' for n in citation_numbers)

    last_run = get_last_text_run(para)
    if last_run is None:
        # No runs with text - add a new run
        run = para.add_run(citation_str)
    else:
        # Append to last run
        last_run.text = last_run.text + citation_str

    # Print what we did
    preview = text[:80] + '...' if len(text) > 80 else text
    print(f"  OK  P{para_index}: {preview}  ->  {citation_str}")
    return True


# ============================================================
# ADD CITATION MARKERS
# ============================================================
print("\n" + "="*60)
print("ADDING CITATION MARKERS")
print("="*60)

# Verify paragraph mapping by printing target paragraphs first
print("\n--- Verifying paragraph content ---")
for p_idx in sorted(citation_map.keys()):
    if p_idx < len(doc.paragraphs):
        text = doc.paragraphs[p_idx].text[:100]
        print(f"  P{p_idx}: {text}...")
    else:
        print(f"  P{p_idx}: OUT OF RANGE")

# Actually add the citations
print("\n--- Adding citations ---")
success_count = 0
for p_idx, citation_nums in sorted(citation_map.items()):
    if add_citation_to_para(doc, p_idx, citation_nums):
        success_count += 1

print(f"\nAdded citations to {success_count} paragraphs.")

# ============================================================
# BUILD REFERENCES SECTION
# ============================================================
print("\n" + "="*60)
print("BUILDING REFERENCES SECTION")
print("="*60)

# References ordered [1] through [32] with GB/T 7714 format
references = [
    # [1] DeepSeek-V4
    "[1] DeepSeek-AI. DeepSeek-V4 Technical Report[R]. arXiv preprint, 2026, arXiv:2604.xxxxx.",
    # [2] Hallucination survey - Alansari
    "[2] Alansari A, Luqman H. A Comprehensive Survey of Hallucination in Large Language Models: Causes, Detection, and Mitigation[J]. arXiv preprint, 2025, arXiv:2510.06265.",
    # [3] Lewis et al. RAG
    "[3] Lewis P, Perez E, Piktus A, et al. Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks[C]//Advances in Neural Information Processing Systems (NeurIPS). Vancouver: Curran Associates, 2020: 9459-9474.",
    # [4] REPLUG
    "[4] Shi W, Min S, Yasunaga M, et al. REPLUG: Retrieval-Augmented Black-Box Language Models[J]. arXiv preprint, 2023, arXiv:2301.12652.",
    # [5] Gao et al. RAG survey
    "[5] Gao Y F, Xiong Y, Gao X Y, et al. Retrieval-Augmented Generation for Large Language Models: A Survey[J]. arXiv preprint, 2024, arXiv:2312.10997.",
    # [6] BM25
    "[6] Robertson S, Zaragoza H. The Probabilistic Relevance Framework: BM25 and Beyond[J]. Foundations and Trends in Information Retrieval, 2009, 3(4): 333-389.",
    # [7] DPR
    "[7] Karpukhin V, Oguz B, Min S, et al. Dense Passage Retrieval for Open-Domain Question Answering[C]//Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP 2020). ACL, 2020: 6769-6781.",
    # [8] COS-Mix
    "[8] Juvekar K, Purwar A. COS-Mix: Cosine Similarity and Distance Fusion for Improved Information Retrieval[J]. arXiv preprint, 2024, arXiv:2406.00638.",
    # [9] C-Pack
    "[9] Xiao S T, Liu Z, Zhang P T, et al. C-Pack: Packaged Resources To Advance General Chinese Embedding[J]. arXiv preprint, 2023, arXiv:2309.07597.",
    # [10] Education RAG
    "[10] Wang N, Singh S. Answering Students' Questions on Course Forums Using Multiple Chain-of-Thought Reasoning and Finetuning RAG-Enabled LLM[J]. arXiv preprint, 2025, arXiv:2511.09831.",
    # [11] MARK education RAG
    "[11] Lian Y. Machine Assistant with Reliable Knowledge: Enhancing Student Learning via RAG-based Retrieval[J]. arXiv preprint, 2025, arXiv:2506.23026.",
    # [12] Vue.js
    "[12] Elman B S, Poff C F, Ramirez S Y. Vue.js: The Progressive JavaScript Framework (Version 3.x)[EB/OL]. (2024). https://vuejs.org/.",
    # [13] TypeScript
    "[13] TypeScript. TypeScript: JavaScript With Syntax For Types (Version 5.x)[EB/OL]. (2024). https://www.typescriptlang.org/.",
    # [14] FastAPI
    "[14] FastAPI. FastAPI: Modern Web Framework for Building APIs with Python (Version 0.110+)[EB/OL]. (2024). https://fastapi.tiangolo.com/.",
    # [15] Milvus
    "[15] Wang J J, Yi X M, Guo R T, et al. Milvus: A Purpose-Built Vector Data Management System[C]//Proceedings of the 2021 International Conference on Management of Data (SIGMOD 2021). Xi'an: ACM, 2021: 2614-2627.",
    # [16] Elasticsearch
    "[16] Elasticsearch B.V. Elasticsearch: Distributed RESTful Search and Analytics Engine (Version 8.x)[EB/OL]. (2024). https://www.elastic.co/elasticsearch/.",
    # [17] BGE M3
    "[17] Chen J L, Xiao S T, Zhang P T, et al. BGE M3-Embedding: Multi-Lingual, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation[J]. arXiv preprint, 2024, arXiv:2402.03216.",
    # [18] BGE-Reranker-V2
    "[18] Chen J L, Xiao S T, Zhang P T, et al. BGE-Reranker-V2: Cross-Encoder Reranking for Retrieval-Augmented Generation[EB/OL]. (2024-03-19). https://huggingface.co/BAAI/bge-reranker-v2-m3.",
    # [19] LangChain
    "[19] LangChain. LangChain: Building Applications with LLMs through Composability[EB/OL]. (2024). https://python.langchain.com/.",
    # [20] RecursiveCharacterTextSplitter
    "[20] LangChain Documentation. RecursiveCharacterTextSplitter[EB/OL]. (2024). https://python.langchain.com/docs/modules/data_connection/document_transformers/recursive_text_splitter.",
    # [21] Semantic chunking
    "[21] Qu R, Bao F, Tu R. Is Semantic Chunking Worth the Computational Cost?[J]. arXiv preprint, 2024, arXiv:2410.13070.",
    # [22] RRF
    "[22] Cormack G V, Clarke C L A, Büttcher S. Reciprocal Rank Fusion Outperforms Condorcet and Individual Rank Learning Methods[C]//Proceedings of the 32nd International ACM SIGIR Conference on Research and Development in Information Retrieval (SIGIR 2009). Boston: ACM, 2009: 758-759.",
    # [23] RAG-Fusion
    "[23] Rackauckas Z. RAG-Fusion: A New Take on Retrieval-Augmented Generation[J]. arXiv preprint, 2024, arXiv:2402.03367.",
    # [24] DMQR-RAG
    "[24] Li Y, Wang Z, Zhang H, et al. DMQR-RAG: Diverse Multi-Query Rewriting for RAG[J]. arXiv preprint, 2024, arXiv:2411.13154.",
    # [25] RAGAS
    "[25] Es S, James J, Espinosa-Anke L, et al. RAGAS: Automated Evaluation of Retrieval Augmented Generation[C]//Proceedings of the 18th Conference of the European Chapter of the Association for Computational Linguistics (EACL 2024). St. Julian's: ACL, 2024: 156-166.",
    # [26] RAG eval survey
    "[26] Yu H, Gan R, Zhang K, et al. Evaluation of Retrieval-Augmented Generation: A Survey[J]. arXiv preprint, 2024, arXiv:2405.07437.",
    # [27] ARES
    "[27] Saad-Falcon J, Khattab O, Potts C, et al. ARES: An Automated Evaluation Framework for Retrieval-Augmented Generation Systems[C]//Proceedings of the 2024 Conference of the North American Chapter of the Association for Computational Linguistics (NAACL 2024). Mexico City: ACL, 2024: 441-458.",
    # [28] Latest RAG survey
    "[28] Bansal R, Agarwal S. Beyond the Parameters: A Technical Survey of Contextual Enrichment in Large Language Models From In-Context Prompting to Causal Retrieval-Augmented Generation[J]. arXiv preprint, 2026, arXiv:2604.03174.",
    # [29] Comprehensive RAG survey
    "[29] Sharma R. Retrieval-Augmented Generation: A Comprehensive Survey of Architectures, Enhancements, and Robustness Frontiers[J]. arXiv preprint, 2025, arXiv:2506.00054.",
    # [30] Domain hybrid search
    "[30] Sultania D, Chen Y, Gupta R, et al. Domain-specific Question Answering with Hybrid Search[J]. arXiv preprint, 2024, arXiv:2412.03736.",
    # [31] Hallucination survey 2
    "[31] Li C, Wang Z, Chen X, et al. Loki's Dance of Illusions: A Comprehensive Survey of Hallucination in Large Language Models[J]. arXiv preprint, 2025, arXiv:2507.02870.",
    # [32] FiD
    "[32] Izacard G, Grave E. Leveraging Passage Retrieval with Generative Models for Open Domain Question Answering[C]//Proceedings of the 16th Conference of the European Chapter of the Association for Computational Linguistics (EACL 2021). ACL, 2021: 874-880.",
]

# ============================================================
# FIND THE REFERENCES SECTION AND INSERT CONTENT
# ============================================================
# Look for the paragraph with style "Heading 1" and text "参考文献"
ref_heading_idx = None
appendix_heading_idx = None

for i, para in enumerate(doc.paragraphs):
    text = para.text.strip()
    style = para.style.name
    if '参考文献' in text and ('Heading' in style or 'heading' in style):
        ref_heading_idx = i
        print(f"Found 参考文献 heading at paragraph {i} (style: {style})")
    if '附' in text and '录' in text and ('Heading' in style or 'heading' in style):
        if appendix_heading_idx is None:
            appendix_heading_idx = i
            print(f"Found 附录 heading at paragraph {i} (style: {style})")

if ref_heading_idx is None:
    print("ERROR: 参考文献 heading not found!")
    # Try searching more broadly
    for i, para in enumerate(doc.paragraphs):
        if '参考文献' in para.text:
            print(f"  Found '参考文献' at para {i}, style='{para.style.name}', text='{para.text[:50]}'")
else:
    print(f"\n参考文献 section: heading at P{ref_heading_idx}")
    if appendix_heading_idx:
        print(f"附录 section: heading at P{appendix_heading_idx}")

    # Clear empty paragraphs between 参考文献 heading and 附录
    # and insert reference entries
    paras_to_clear = []
    for i in range(ref_heading_idx + 1, appendix_heading_idx if appendix_heading_idx else len(doc.paragraphs)):
        text = doc.paragraphs[i].text.strip()
        if not text or text == '':
            paras_to_clear.append(i)

    print(f"Found {len(paras_to_clear)} empty paragraphs between 参考文献 and 附录")

    # Strategy: Use the first empty paragraph after 参考文献 for the first reference,
    # then insert new paragraphs for the rest
    if paras_to_clear:
        # Fill the first empty paragraph with first reference
        first_empty = paras_to_clear[0]
        para = doc.paragraphs[first_empty]
        # Clear existing runs
        for run in para.runs:
            run.text = ''
        # Add reference text
        ref1_run = para.runs[0] if para.runs else para.add_run(references[0])
        if para.runs:
            para.runs[0].text = references[0]
        else:
            para.add_run(references[0])

        # Set font for the first reference paragraph
        for run in para.runs:
            run.font.name = '宋体'
            run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
            run.font.size = Pt(11)

        # Insert remaining references before the appendix
        ref_anchor = doc.paragraphs[appendix_heading_idx] if appendix_heading_idx else None

        for ref_text in references[1:]:
            # Create a new paragraph
            new_para = doc.add_paragraph()
            # Move it before appendix
            if ref_anchor:
                ref_anchor._element.addprevious(new_para._element)

            new_para.paragraph_format.first_line_indent = Cm(0)
            new_para.paragraph_format.space_before = Pt(0)
            new_para.paragraph_format.space_after = Pt(0)
            new_para.paragraph_format.line_spacing = 1.5

            run = new_para.add_run(ref_text)
            run.font.name = 'Times New Roman'
            run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
            run.font.size = Pt(11)

        print(f"All {len(references)} references inserted successfully.")
    else:
        print("ERROR: No empty paragraphs found for references!")

# ============================================================
# SAVE
# ============================================================
doc.save('papers/论文2.0.docx')
print("\n" + "="*60)
print("DONE! File saved: papers/论文2.0.docx")
print(f"Total citations added: {success_count} paragraph groups")
print(f"Total references: {len(references)}")
print("="*60)
