# -*- coding: utf-8 -*-

import json
import multiprocessing
import os
import warnings
import stanza

LEXICONS_FOLDER = "lexicons_folder"

os.environ["PYTHONWARNINGS"] = "ignore"
warnings.filterwarnings("ignore")

prep_way = os.path.join(LEXICONS_FOLDER, "preprocessed_lexicon.json")
with open(prep_way, encoding="utf-8") as f:
    prepocessed_definition = json.load(f)

# Глобальна змінна для конвеєру (пайплайну) всередині кожного ядра процесора
nlp_pipeline = None


def init_worker():
    global nlp_pipeline
    nlp_pipeline = stanza.Pipeline(
        lang="uk", processors="tokenize,mwt,pos,lemma", logging_level="WARN"
    )


def process_definition(item):
    """Ця функція швидко обробляє одну статтю на своєму ядрі."""
    global nlp_pipeline
    
    dict_word, text = item 
    
    if not text or not isinstance(text, str):
        return dict_word, ""

    doc = nlp_pipeline(text)
    clean_lemmas = []

    for sentence in doc.sentences:
        # Перейменував на word_obj, щоб не затирати змінну dict_word
        for word_obj in sentence.words:
            # Прибираємо пунктуацію, цифри та символи за тегами Stanza
            if word_obj.upos not in ("PUNCT", "NUM", "SYM"):
                clean_lemmas.append(word_obj.lemma)

    # Повертаємо теж кортеж: (слово, лематизований текст)
    return dict_word, " ".join(clean_lemmas)


def main():
    raw_definitions = prepocessed_definition

    # Визначаємо кількість ядер процесора
    num_cores = multiprocessing.cpu_count()

    # Запускаємо пул процесів
    with multiprocessing.Pool(
        processes=num_cores, initializer=init_worker
    ) as pool:
        results = pool.map(process_definition, raw_definitions.items())

    # Перетворюємо список кортежів назад у красивий словник dict
    final_lemmatized_dict = dict(results)
    
    lem_way = os.path.join(LEXICONS_FOLDER, "lemmatized_lexicon.json")
    # Зберігаємо фінальний результат як повноцінний структурований JSON-словник
    with open(lem_way, "w", encoding="utf-8") as pd:
        json.dump(final_lemmatized_dict, pd, ensure_ascii=False, indent=4)
    

if __name__ == "__main__":
    main()