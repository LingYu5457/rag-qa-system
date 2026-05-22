import json
import os
import time
from rag.generation.chat import ChatPipeline
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def load_qa_pairs(file_path: str) -> list:
    """
    读取 qa_pairs.json，将嵌套结构展开为扁平列表。
    每个元素包含: id, source, difficulty, direction, question, ground_truth
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    qa_pairs = data.get("qa_pairs", {})
    flat_list = []
    for source_name, source_data in qa_pairs.items():
        for q in source_data.get("questions", []):
            flat_list.append({
                "id": q["id"],
                "source": source_name,
                "source_desc": source_data.get("source", ""),
                "difficulty": q["difficulty"],
                "direction": q["direction"],
                "question": q["question"],
                "ground_truth": q["answer"],
            })
    return flat_list


def extract_contexts_from_steps(steps: list) -> list:
    """从steps中提取rerank结果的文档文本作为contexts"""
    contexts = []
    for step in steps:
        if step.startswith("rerank结果"):
            colon_idx = step.find(": ")
            if colon_idx != -1:
                doc_text = step[colon_idx + 2:]
                if doc_text.endswith("..."):
                    doc_text = doc_text[:-3]
                contexts.append(doc_text)
    return contexts


def plot_timing(iteration_times: list, total_time: float, output_dir: str):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    iterations = range(1, len(iteration_times) + 1)
    bars = ax1.bar(iterations, iteration_times, color='steelblue', edgecolor='white')
    ax1.set_xlabel('Iteration')
    ax1.set_ylabel('Time (seconds)')
    ax1.set_title('Time per Iteration')
    ax1.set_xticks(iterations)

    for bar, t in zip(bars, iteration_times):
        ax1.text(bar.get_x() + bar.get_width() / 2., bar.get_height() + 0.1,
                 f'{t:.1f}s', ha='center', va='bottom', fontsize=9)

    avg_time = sum(iteration_times) / len(iteration_times) if iteration_times else 0
    stats = ['Min', 'Max', 'Avg', 'Total']
    values = [min(iteration_times), max(iteration_times), avg_time, total_time]
    colors = ['#5cb85c', '#d9534f', '#f0ad4e', '#337ab7']
    bars2 = ax2.bar(stats, values, color=colors, edgecolor='white')
    ax2.set_ylabel('Time (seconds)')
    ax2.set_title('Summary Statistics')

    for bar, v in zip(bars2, values):
        ax2.text(bar.get_x() + bar.get_width() / 2., bar.get_height() + 0.1,
                 f'{v:.1f}s', ha='center', va='bottom', fontsize=10)

    plt.tight_layout()
    output_path = os.path.join(output_dir, "timing_evaluation.png")
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"用时评估图已保存至: {output_path}")


def run_evaluation(qa_pairs_path: str = "evaluate/qa_pairs.json",
                   output_dir: str = "evaluate"):
    qa_pairs = load_qa_pairs(qa_pairs_path)
    print(f"已加载 {len(qa_pairs)} 条QA数据\n")

    pipeline = ChatPipeline(use_local_llm=False)

    results = []
    iteration_times = []
    total_start = time.time()

    for i, qa in enumerate(qa_pairs):
        question = qa["question"]
        ground_truth = qa["ground_truth"]

        steps = []
        iter_start = time.time()

        answer_chunks = []
        for chunk in pipeline.chat(user_query=question, steps=steps, history=[]):
            answer_chunks.append(chunk)
        answer = "".join(answer_chunks)

        iter_time = time.time() - iter_start
        iteration_times.append(iter_time)

        contexts = extract_contexts_from_steps(steps)

        eval_dict = {
            "id": qa["id"],
            "source": qa["source"],
            "difficulty": qa["difficulty"],
            "direction": qa["direction"],
            "question": question,
            "answer": answer,
            "contexts": contexts,
            "ground_truth": ground_truth,
        }
        results.append(eval_dict)

        print(
            f"[{i+1}/{len(qa_pairs)}] {qa['id']} "
            f"| 难度:{qa['difficulty']} | 方向:{qa['direction']} "
            f"| 耗时:{iter_time:.2f}s | context:{len(contexts)}条"
        )

    total_time = time.time() - total_start

    # 保存RAGAS评估数据
    output_path = os.path.join(output_dir, "ragas_eval_data.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n评估数据已保存至: {output_path}")

    # 绘制用时评估图
    plot_timing(iteration_times, total_time, output_dir)

    print(f"\n总迭代次数: {len(qa_pairs)}")
    print(f"总用时: {total_time:.2f}s")
    print(f"平均每次用时: {sum(iteration_times)/len(iteration_times):.2f}s")

    return results


if __name__ == "__main__":
    run_evaluation()
