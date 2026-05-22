import json
import matplotlib.pyplot as plt
import numpy as np
from openai import OpenAI
from config.settings import model_settings

client = OpenAI(
    api_key=model_settings.DEEPSEEK_API_KEY,
    base_url=model_settings.DEEPSEEK_BASE_URL
)

# 读取数据
with open('evaluate/ragas_eval_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 评估 prompt
def evaluate_rag(question, answer, context, ground_truth):
    prompt = f"""请评估以下 RAG 系统的回答质量，给出0-1之间的数字分数。

问题：{question}
标准答案：{ground_truth}
检索到的上下文：{context}
生成的答案：{answer}

请按以下格式输出4个分数（只输出数字，用逗号分隔）：
忠实性,答案相关性,上下文召回率,上下文精确率

示例输出：0.85,0.90,0.75,0.80

现在请输出："""

    response = client.chat.completions.create(
        model=model_settings.DEEPSEEK_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    
    result_text = response.choices[0].message.content.strip()
    print(f"返回结果: {result_text}")  # 调试用
    
    # 尝试解析
    try:
        scores = [float(x.strip()) for x in result_text.split(',')]
        if len(scores) != 4:
            raise ValueError(f"返回了{len(scores)}个分数，需要4个")
    except:
        # 如果解析失败，尝试按行解析
        lines = result_text.split('\n')
        scores = []
        for line in lines:
            for part in line.split(','):
                try:
                    scores.append(float(part.strip()))
                except:
                    pass
        if len(scores) != 4:
            print(f"解析失败，使用默认分数")
            scores = [0.5, 0.5, 0.5, 0.5]
    
    return {
        'faithfulness': scores[0],
        'answer_relevancy': scores[1],
        'context_recall': scores[2],
        'context_precision': scores[3]
    }

# 评估所有
results = []
for i, item in enumerate(data):
    print(f"\n评估 {i+1}/{len(data)}")
    try:
        scores = evaluate_rag(
            item['question'],
            item['answer'],
            str(item['contexts']),  # 转成字符串
            item['ground_truth']
        )
        results.append(scores)
        print(f"  忠实性:{scores['faithfulness']:.3f}, 相关性:{scores['answer_relevancy']:.3f}, 召回:{scores['context_recall']:.3f}, 精确:{scores['context_precision']:.3f}")
    except Exception as e:
        print(f"第{i+1}个评估失败: {e}")
        results.append({'faithfulness': 0.5, 'answer_relevancy': 0.5, 'context_recall': 0.5, 'context_precision': 0.5})

# 计算平均
avg = {k: sum(r[k] for r in results)/len(results) for k in results[0]}

# 保存结果到 JSON
with open('evaluate/evaluation_results.json', 'w', encoding='utf-8') as f:
    json.dump({
        'average_scores': avg,
        'detailed_scores': results
    }, f, ensure_ascii=False, indent=2)

# 画图
metrics_cn = ['忠实性', '答案相关性', '上下文召回率', '上下文精确率']
metrics_en = list(avg.keys())
scores = list(avg.values())

plt.figure(figsize=(10, 6))
bars = plt.bar(metrics_cn, scores, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
plt.ylim(0, 1)
plt.ylabel('Score', fontsize=12)
plt.title('RAG System Evaluation Results', fontsize=14)
plt.xticks(rotation=0, fontsize=11)

# 在柱子上显示数值
for bar, score in zip(bars, scores):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, 
             f'{score:.3f}', ha='center', va='bottom', fontsize=11)

plt.tight_layout()
plt.savefig('evaluate/evaluation_chart.png', dpi=300, bbox_inches='tight')
plt.show()

# 打印结果
print("\n" + "="*50)
print("RAG 系统评估结果")
print("="*50)
print(f"忠实性 (Faithfulness): {avg['faithfulness']:.4f}")
print(f"答案相关性 (Answer Relevancy): {avg['answer_relevancy']:.4f}")
print(f"上下文召回率 (Context Recall): {avg['context_recall']:.4f}")
print(f"上下文精确率 (Context Precision): {avg['context_precision']:.4f}")
print("="*50)
print(f"\n结果已保存到:")
print(f"  - evaluate/evaluation_results.json")
print(f"  - evaluate/evaluation_chart.png")