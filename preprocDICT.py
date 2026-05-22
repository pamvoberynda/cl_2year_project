# -*- coding: utf-8 -*-
import json
import re
from bs4 import BeautifulSoup
import tempfunctions as tf


ALL_CHARACTERS = r'[\[\]\(\)a-zA-zа-яА-ЯєЄіІїЇґҐ’.,:;?!\s…\-*«»—\d]'
ALL_LETTERS = r'[a-zA-zа-яА-ЯєЄіІїЇґҐ’]'
ONLY_LATIN = r'[a-zA-Z]'
META_CHARACTERS = r'[;:\'\"…\-*«»—\.,\//]'
STOP_WORDS = (
    "Прикм.", "Дієпр.", "т.", "ін.",
    "Жін.", "Чол.", "пас.",
    "мин.", "філос.", "лінгв.", "ст."
)
SUPPER_NUMBERS = ("⁰","¹","²","³","⁴",
                  "⁵","⁶","⁷","⁸","⁹") # це треба адекватної роботи з омонімами а-ля КЛЮЧ¹ і КЛЮЧ²


#reading sum11
with open("sum11.json", encoding="utf-8") as f:
    parseddata = json.load(f)

# Перетворюємо всі ключі на список і шукаємо індекс


indx = tf.find_index("просвітництво", parseddata)
print(indx)


#data = dict(list(data.items())[indx:indx+1])
data = dict(list(parseddata.items())[indx:indx+1])


def xnum2tenB(number: str, system: tuple = ("⁰","¹","²","³","⁴","⁵","⁶","⁷","⁸","⁹")) -> int: #recive a "number" and exchange it in normal 10-based number. for ex: ¹² => 12; ab => 12
    number = str(number) #для впевненості
    xnumber = str() #output, x = transformed
    for letter in number:
        i = int()
        while i < len(system):
            if letter == system[i]:
                xnumber += str(i)
                break
            i+= 1
    return xnumber

def purify_dict_word(word, definition) -> tuple:
    article = [word, definition]

    for i in range(len(article)):
        clean_text = article[i]
        # видаленнє прикладів вжитку, самого слова та метаслів а-ля <div>
        #clean_text = re.sub(r'(<b>.*?</b>)', ' ', clean_text, count = 1)
        #clean_text = re.sub(r'(<div>[♦◊] <b>.*?</b>.*?</div><div>\d{1,2})', ' ', clean_text) #видаляє фразеологізми, ну принаймні пробує видалити...
        
        clean_text = re.sub(fr'<div>(\s*[♦◊▲∆]\s*<b>|\s*<b>\s*[♦◊▲∆]\s*){ALL_CHARACTERS}*?<\/b>.*?<\/div>', ' ', clean_text) #видаляє фразеологізми, ну принаймні пробує видалити...
        #clean_text = re.sub(fr'<div>(?:\s*[♦◊▲]\s*)?<b>(?:(?!<\/div>).)*?<\/b>(?:(?!<\/div>).)*? — (?:(?!<\/div>).)*?<\/div>(?:\s*<div>\s*<span>(?:(?!<\/div>).)*?<\/span>\s*<\/div>)?', ' ', clean_text) #видаляє фразеологізми, ну принаймні пробує видалити...

        # видалення відмінювання
        # дуже докладний варіант, нижче простіший чи точніший хтозна #clean_text = re.sub(r'(\b((ів)|(і)|(ую)|(юю)|(юєш)|(аюся)|(аєшся)|(у)|(уєшся)|(ується)|(уєш)|(юється)|(уживається)|(очуся)|(отишся)|(\b[аеияжч][,.\s])))(?=[,.\s]|\b)', ' ', clean_text) 
        clean_text = re.sub(fr'(?<=</b>,)\s*{ALL_LETTERS}+\s*(?=,)', ' ', clean_text)
        clean_text = re.sub(fr'(?<=</i>)\s*{ALL_LETTERS}+\s*(?=:)', ' ', clean_text) # ця дура видаляє срань по типу «уживається»

        clean_text = re.sub(fr'(<i>\s*{ALL_CHARACTERS}*?\s*</i>)|(<div>|</div>|<span>|</span>|<b>|</b>)', ' ', clean_text)

        #анігіляція цитат а-ля (Сракожуєв, ІІ, 1967)
        clean_text = re.sub(r'\([^)]*\)|\[[^\]]*\]|\{[^\{}]*\}', ' ', clean_text)
        
        # це символ наголосу, окрема діякритика
        clean_text = re.sub(r'\u0301', '', clean_text)

        stopwords_regex = "|".join(f"({re.escape(word.lower())})" for word in STOP_WORDS)
        clean_text = re.sub(rf'{stopwords_regex}', ' ', clean_text) #видалення скорочень та всякого


        clean_text = re.sub(r'\d+\.', ' ', clean_text) #видалення номерів лсв
        clean_text = re.sub(rf'{ONLY_LATIN}',' ', clean_text) #выдаленнє латинськихъ лѣтеръ
        clean_text = re.sub(rf'{META_CHARACTERS}', ' ', clean_text) #видалення не-літер
        

        # Прибираємо зайві пробіли і крапки з комою
        #clean_text = re.sub(r'([\s,.;]+[,.;]+[\s,.;]+)', '', clean_text)
        clean_text = re.sub(r'\s+([,.;]+)', '', clean_text)
        clean_text = re.sub(r'\s{2,}', ' ', clean_text)
        
        article[i] = clean_text

    #print("purified:")
    #print(f"{article[0]}: {article[1]}")


    return article[0], article[1]

def separate_homonyms(lexicon_artcl: str) -> tuple:
    suppernums_regex = fr"[{''.join(SUPPER_NUMBERS)}]"
    raw_homonyms = re.split(rf'(?=<div><b>{ALL_CHARACTERS}+{suppernums_regex}*</b>,)', lexicon_artcl)

    newlexicon = []
    for homonym_part in raw_homonyms:
        # Шукаємо омонім разом з його індексом всередині тегів <b>
        #match_word = re.search(fr'(<div><b>{ALL_CHARACTERS}+({suppernums_regex}*)</b>(?!<i>))', homonym_part) # задавання пошуку визначення негативним шляхом 
        match_word = re.search(fr'(<div><b>{ALL_CHARACTERS}+({suppernums_regex}*)</b>),', homonym_part) # задавання пошуку визначення позитивним шляхом
        if match_word:
            if match_word.group(2): #якщо є індекс, якщо це кляті омоніми. Наприклад: "КЛЮЧ¹" або "КЛЮЧ²"
                homonym_title = match_word.group(1).replace(match_word.group(2), xnum2tenB(match_word.group(2)))
                homonym_part = homonym_part.replace(match_word.group(2), xnum2tenB(match_word.group(2))) 
            else:
                homonym_title = match_word.group(1) #просто сам <div><b>КОЛОТИ́ТИСЯ</b>
            newlexicon.append((homonym_title,homonym_part))
    print(newlexicon)
    return newlexicon

def main(data: dict):
    #creating preprocessed dictionary for following lemmatization
    preprocessed_dict = {} 
    for index, (word, html) in enumerate(data.items()): #тут надмірна якась структура, але уже маємо що маємо цей релікт
        oneArtclDic = {}
        #print()
        #print(html)

        clean_text = html.lower()
        clean_text = re.sub(r'\u0301', '', clean_text) # одразу видаляю цей потрачений наголос
        
        artcls = separate_homonyms(clean_text) # -> list of tuples
        for pair in artcls:
            puredtuple = purify_dict_word(pair[0],pair[1]) #deleting trash from the textus, keeping pure definitions
            oneArtclDic[puredtuple[0]] = puredtuple[1] #creating small dictionary, containing 1 preprocessed artcile

        preprocessed_dict = preprocessed_dict | oneArtclDic
    
    """"""
    for prepocessed_word, prepocessed_definition in preprocessed_dict.items():
        print(f"{prepocessed_word}: {prepocessed_definition}")
        print()
    return 0

main(data)
