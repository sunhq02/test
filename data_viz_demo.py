"""
基础数据可视化示例 - 柱状图
演示如何使用 matplotlib 绘制简单的柱状图
"""

import numpy as np
import matplotlib.pyplot as plt

# 设置中文字体支持（防止中文乱码）
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 生成随机数据
np.random.seed(42)  # 固定随机种子，保证结果可复现

# 类别标签
categories = ['产品 A', '产品 B', '产品 C', '产品 D', '产品 E']

# 生成随机销售额数据（单位：万元）
sales = np.random.randint(50, 200, size=5)

# 生成对应的颜色，使每个柱子有不同颜色
colors = ['#8877cc', '#6699cc', '#55aacc', '#44bbdd', '#33ccee']

# 创建柱状图
fig, ax = plt.subplots(figsize=(10, 6))

bars = ax.bar(categories, sales, color=colors, edgecolor='black', linewidth=1.2)

# 添加标题和标签
ax.set_title('各产品销售业绩对比', fontsize=16, fontweight='bold')
ax.set_xlabel('产品', fontsize=12)
ax.set_ylabel('销售额 (万元)', fontsize=12)

# 在柱子上方添加数值标签
for bar, value in zip(bars, sales):
    ax.text(bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 5,
            f'{value:.1f}',
            ha='center', va='bottom', fontsize=11)

# 优化布局并显示网格（仅 Y 轴）
ax.grid(axis='y', alpha=0.3, linestyle='--')
ax.set_axisbelow(True)

# 调整 y 轴范围，给顶部留点空间
ax.set_ylim(0, max(sales) * 1.3)

plt.tight_layout()
plt.show()

print("=== 数据可视化演示完成 ===")
print(f"生成的数据:")
for cat, sale in zip(categories, sales):
    print(f"  {cat}: {sale} 万元")
