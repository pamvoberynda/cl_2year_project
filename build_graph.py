# -*- coding: utf-8 -*-

import json
import re
import math
import networkx as nx
from tempfunctions import unite_subarticles
import os

LEXICAL_STOP_WORDS = {
    "за", "з", "на", "в", "у", "від", "для", "по", "при", "через", "під", 
    "про", "із", "без", "між", "відносно", "завдяки", "хто",
    "що", "як", "або", "і", "й", "та", "але", "чи", "ніби", "наче", "немов", 
    "то", "док", "якийсь", "цей", "тощо", "означати", "позначати",
    "яка", "яке", "які", "це", "те", "той", "така", "таке", "певний", "такий",
    "його", "її", "їх", "сам", "самий", "він", "вона", "вони", "саме", "який", "до",
}
RESULTS_FOLDER = "results_folder"
LEXICONS_FOLDER = "lexicons_folder"

def mk_graph():
    lemmatized_way = os.path.join(LEXICONS_FOLDER, "lemmatized_lexicon.json")
    with open(lemmatized_way, "r", encoding="utf-8") as f:
        raw_lexicon = json.load(f)

    raw_lexicon = unite_subarticles(raw_lexicon)

    collapsed_lexicon = {}
    for headword, text in raw_lexicon.items():
        clean_headword = re.sub(r'\d+$', '', headword).lower().strip()
        if clean_headword in LEXICAL_STOP_WORDS:
            continue
        if clean_headword in collapsed_lexicon:
            collapsed_lexicon[clean_headword] += " " + (text or "")
        else:
            collapsed_lexicon[clean_headword] = text or ""

    # Будуємо глобальний граф
    G = nx.DiGraph()
    all_headwords = set(collapsed_lexicon.keys())

    for headword, definition_text in collapsed_lexicon.items():
        defining_words = definition_text.split()
        for def_word in defining_words:
            def_word_clean = def_word.lower().strip()
            if def_word_clean in all_headwords and def_word_clean != headword:
                G.add_edge(def_word_clean, headword)

    # 1. PAGERANK
    G_reversed = G.reverse(copy=True)
    global_pagerank = nx.pagerank(G_reversed, alpha=0.85, max_iter=150, tol=1e-06)

    # 2. K-CORE DECOMPOSITION
    core_numbers = nx.core_number(G)
    k_max = max(core_numbers.values())
    core_nodes = set([node for node, k in core_numbers.items() if k == k_max])
    
    print(f"k_max={k_max}: {len(core_nodes)}")

    # Збираємо та сортуємо всі слова ядра за спаданням глобальної ваги
    H = G.subgraph(core_nodes)
    ranked_core = []
    for node in core_nodes:
        ranked_core.append({
            'word': node,
            'pr': global_pagerank[node],
            'out_global': G.out_degree(node),
            'in_core': H.in_degree(node)
        })
    ranked_core.sort(key=lambda x: x['pr'], reverse=True)

    list_ranked_core = ""
    for item in ranked_core:
        list_ranked_core += f"{item['word']} {item['pr']:.6f}\n"


    kcore_ranked_way = os.path.join(RESULTS_FOLDER, "kcoreres_ranked.txt")
    with open(kcore_ranked_way, "w", encoding="utf-8") as txt:
        txt.write(list_ranked_core)


    # 3. ELBOW METHOD
    
    # Координати початку і кінця кривої (хорди)
    p1_x, p1_y = 0, ranked_core[0]['pr']
    p2_x, p2_y = len(ranked_core) - 1, ranked_core[-1]['pr']
    
    max_distance = -1
    cutoff_index = 0

    # Шукаємо точку максимального перпендикулярного відхилення від хорди
    for i, point in enumerate(ranked_core):
        x0 = i
        y0 = point['pr']
        
        # Формула відстані від точки до прямої лінії
        numerator = abs((p2_y - p1_y) * x0 - (p2_x - p1_x) * y0 + p2_x * p1_y - p2_y * p1_x)
        denominator = math.sqrt((p2_y - p1_y)**2 + (p2_x - p1_x)**2)
        distance = numerator / denominator
        
        if distance > max_distance:
            max_distance = distance
            cutoff_index = i

    # Формуємо фінальний ізольований список примітивів
    final_primitives = ranked_core[:cutoff_index + 1]
    

    # safe values for charts
    dump_data = {
        "cutoff_index": cutoff_index,
        "p1_x": p1_x,
        "p1_y": p1_y,
        "p2_x": p2_x,
        "p2_y": p2_y,
        "ranked_core": ranked_core  # наш список словників [{'word':..., 'pr':...}]
    }

    dump_path = os.path.join(RESULTS_FOLDER, "analysis_dump.json")
    with open(dump_path, "w", encoding="utf-8") as f:
        json.dump(dump_data, f, ensure_ascii=False, indent=4)

    
    pure_words = [p['word'] for p in final_primitives]
    pure_words = "\n".join(pure_words)

    res_way = os.path.join(RESULTS_FOLDER, "results.txt")

    with open(res_way, "w") as res:
        res = res.write(pure_words)
    
    return 0

mk_graph()