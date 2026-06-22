import matplotlib.pyplot as plt
import numpy as np
import math
import os
import json

RESULTS_FOLDER = "results_folder"

def main():
 
    # =========================================================================
    # ОКРЕМА ВІЗУАЛІЗАЦІЯ ГРАФІКІВ (ЗБЕРЕЖЕННЯ В РІЗНІ ФАЙЛИ)
    # =========================================================================
    dump_path = os.path.join(RESULTS_FOLDER, "analysis_dump.json")
    with open(dump_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Розпаковуємо змінні назад у код
    ranked_core = data["ranked_core"]
    cutoff_index = data["cutoff_index"]
    p1_x, p1_y = data["p1_x"], data["p1_y"]
    p2_x, p2_y = data["p2_x"], data["p2_y"]

    # 1. Готуємо загальні дані
    x_vals = np.arange(len(ranked_core))
    y_vals = np.array([point['pr'] for point in ranked_core])

    knee_x = cutoff_index
    knee_y = ranked_core[cutoff_index]['pr']
    knee_word = ranked_core[cutoff_index]['word']

    # Обчислюємо масив значень перпендикулярних відстаней до хорди
    distances = []
    denominator = math.sqrt((p2_y - p1_y)**2 + (p2_x - p1_x)**2)

    for i, point in enumerate(ranked_core):
        x0 = i
        y0 = point['pr']
        numerator = abs((p2_y - p1_y) * x0 - (p2_x - p1_x) * y0 + p2_x * p1_y - p2_y * p1_x)
        distances.append(numerator / denominator)

    distances = np.array(distances)

    # -------------------------------------------------------------------------
    # ФІГУРА 1: Крива розподілу PageRank та Хорда
    # -------------------------------------------------------------------------
    plt.figure(figsize=(11, 6))
    
    plt.plot(x_vals, y_vals, label='Крива розподілу ваг PageRank', color='#1f77b4', linewidth=2.5)
    plt.plot([p1_x, p2_x], [p1_y, p2_y], label='Хорда (вектор p1-p2)', color='gray', linestyle='--', linewidth=1.5)

    # Підсвічуємо точку зламу червоним колом
    plt.scatter(knee_x, knee_y, color='red', s=120, zorder=5, label=f'Точка зламу (ранг {cutoff_index + 1})')

    # Малюємо вертикальну штрихову лінію відхилення
    chord_y_at_knee = p1_y + (p2_y - p1_y) * (knee_x / p2_x)
    plt.plot([knee_x, knee_x], [knee_y, chord_y_at_knee], color='red', linestyle=':', label='Максимальна відстань (d)')
    plt.axvline(x=cutoff_index, color='green', linestyle=':', lw=1.5)

    # Красивий підпис зі стрілочкою до точки зламу
    plt.annotate(
        f"Межа відсікання\nСлово: «{knee_word}»\nРанг: {cutoff_index + 1}",
        xy=(knee_x, knee_y),
        xytext=(knee_x + len(ranked_core) * 0.08, knee_y + (p1_y - p2_y) * 0.15),
        arrowprops=dict(facecolor='black', shrink=0.08, width=1, headwidth=6, headlength=6),
        fontsize=10,
        bbox=dict(boxstyle="round,pad=0.3", fc="yellow", alpha=0.3)
    )

    plt.title('Обґрунтування межі семантичних примітивів методом геометричного зламу', fontsize=12, fontweight='bold', pad=12)
    plt.xlabel('Ранг слова у розподілі словника', fontsize=10)
    plt.ylabel('Значення глобального PageRank', fontsize=10)
    plt.grid(True, linestyle=':', alpha=0.5)
    plt.legend(fontsize=10, loc='upper right')
    
    plt.tight_layout()
    path_chart1 = os.path.join(RESULTS_FOLDER, "chart_1_pagerank_distribution.png")
    plt.savefig(path_chart1, dpi=300, bbox_inches='tight')

    # -------------------------------------------------------------------------
    # ФІГУРА 2: Чиста функція відстані d(x)
    # -------------------------------------------------------------------------
    plt.figure(figsize=(11, 5))
    
    plt.plot(x_vals, distances, color='#d62728', lw=2.5, label='Геометрична відстань $d(x)$ до хорди')
    plt.axvline(x=cutoff_index, color='green', linestyle=':', lw=2)

    # Ставимо велику зелену точку на вершині (глобальний екстремум)
    plt.scatter(cutoff_index, distances[cutoff_index], color='green', s=150, zorder=5,
                label=f'Глобальний екстремум (max) | Ранг {cutoff_index + 1}: "{knee_word}"')

    plt.title('Графік функції відхилення від хорди (Пошук екстремуму системи)', fontsize=12, fontweight='bold', pad=12)
    plt.xlabel('Ранг слова у розподілі словника', fontsize=10)
    plt.ylabel('Перпендикулярна відстань', fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(fontsize=10, loc='upper right')

    plt.tight_layout()
    path_chart2 = os.path.join(RESULTS_FOLDER, "chart_2_distance_function.png")
    plt.savefig(path_chart2, dpi=300, bbox_inches='tight')

    return 0

main()

