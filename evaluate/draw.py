import json
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams['font.family'] = 'SimHei'
matplotlib.rcParams['axes.unicode_minus'] = False

with open('evaluate/evaluation_results.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

metrics = ['faithfulness', 'answer_relevancy', 'context_recall', 'context_precision']
labels = ['Faithfulness', 'Answer Relevancy', 'Context Recall', 'Context Precision']

avg = data['average_scores']
averages = [avg[m] for m in metrics]

detailed = data['detailed_scores']
scores_by_metric = {m: [d[m] for d in detailed] for m in metrics}

# ---- Figure 1: Average Scores Bar Chart ----
fig1, ax1 = plt.subplots(figsize=(8, 5))
colors = ['#4C72B0', '#55A868', '#C44E52', '#8172B2']
bars = ax1.bar(labels, averages, color=colors, edgecolor='white', linewidth=0.8)

for bar, val in zip(bars, averages):
    ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
             f'{val:.4f}', ha='center', va='bottom', fontsize=11, fontweight='bold')

ax1.set_ylim(0, 1.15)
ax1.set_ylabel('Score')
ax1.set_title('RAG Evaluation — Average Scores')
ax1.grid(axis='y', alpha=0.3)
fig1.tight_layout()
fig1.savefig('evaluate/avg_scores_bar.png', dpi=150)
plt.close(fig1)

# ---- Figure 2: Detailed Scores Box Plot ----
fig2, ax2 = plt.subplots(figsize=(8, 5))
box_data = [scores_by_metric[m] for m in metrics]
bp = ax2.boxplot(box_data, tick_labels=labels, patch_artist=True,
                 showmeans=True, meanprops=dict(marker='D', markerfacecolor='red', markersize=6))

for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

ax2.set_ylabel('Score')
ax2.set_title('RAG Evaluation — Score Distribution per Metric')
ax2.grid(axis='y', alpha=0.3)
fig2.tight_layout()
fig2.savefig('evaluate/detailed_scores_box.png', dpi=150)
plt.close(fig2)

# ---- Figures 3+: Per-sample Line Charts (9 samples each) ----
chunk_size = 9
total = len(detailed)
colors = ['#4C72B0', '#55A868', '#C44E52', '#8172B2']

for chunk_idx, start in enumerate(range(0, total, chunk_size)):
    end = min(start + chunk_size, total)
    chunk_slice = slice(start, end)
    x = list(range(start + 1, end + 1))

    fig, ax = plt.subplots(figsize=(10, 5))
    for i, m in enumerate(metrics):
        ax.plot(x, scores_by_metric[m][chunk_slice], marker='o', markersize=5,
                color=colors[i], label=labels[i], linewidth=1.3, alpha=0.85)

    ax.axhline(y=0.8, color='gray', linestyle='--', linewidth=0.8, alpha=0.6)
    ax.set_xlabel('Sample Index')
    ax.set_ylabel('Score')
    ax.set_title(f'RAG Evaluation — Per-Sample Scores (Samples {start + 1}–{end})')
    ax.legend(loc='lower left', fontsize=9)
    ax.set_xticks(x)
    ax.grid(axis='y', alpha=0.3)
    fig.tight_layout()
    filename = f'evaluate/per_sample_scores_{start + 1}_{end}.png'
    fig.savefig(filename, dpi=150)
    plt.close(fig)

print('Charts saved to evaluate/ directory:')
print('  avg_scores_bar.png')
print('  detailed_scores_box.png')
for start in range(0, total, chunk_size):
    end = min(start + chunk_size, total)
    print(f'  per_sample_scores_{start + 1}_{end}.png')
