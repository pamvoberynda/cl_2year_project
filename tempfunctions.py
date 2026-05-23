# -*- coding: utf-8 -*-

import re

def find_index(word: str, lexicon: dict) -> int:
    keys_list = list(lexicon.keys())
    try:
        seeked_index = keys_list.index(word)
        return seeked_index
    except ValueError:
        return None
    

def find_homonyms(lexicon: dict):
    for word, definition in lexicon.items():
        if f"<div><b>{word}</b>" in definition:
            return "goooooooll"
    return "No match found"

exmpl ={"a": "<div><b>a</b>", "b": "<div><b>v</b>"}

#print(find_homonyms(exmpl))

system1 = ("addd","aa","c","d","e","f","g","h","i","o") 

#x - exchange, num - number, 2 - to, ten - ten, B - based
#works only with similфк 10-based counting systems
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

exmpl = "<div><b>КОСА́¹</b>, и, <i>ж</i>.</div><div>1. Заплетене волосся.</div><div><i>Якраз під старою вишнею.. стояла дівчина, хороша, як зоря ясна; руса коса нижче пояса </i>(Вовчок, І, 1955, 38);</div><div><i>Очі в неї були великі, дві чорні коси, перекинуті наперед, обрамляли лице </i>(Сенч., На Бат. горі, 1960, 32).</div><div><b>◊ До си́вої коси́</b> — до старості.</div><div><span><i>— Я ждатиму Йвана хоч до сивої коси </i>(Л. Укр., III, 1952, 739);</span></div><div><b>Зав’яза́ти косу́</b><i> див. </i><b>завя́зувати</b>.</div><div>2. <i>перев. мн.</i> Довге волосся.</div><div><i>Хто се, хто се по тім боці Рве на собі коси?.. </i>(Шевч., І, 1951, 164);</div><div><i>Густі, золото-жовті коси буйними хвилями спадали на її груди і плечі </i>(Фр., II, 1950, 378);</div><div><i>Дівча біжить в тяжкім одчаї, Коса їй плечі устеляє </i>(Стельмах, Жито.., 1954, 90);</div><div><i>*Образно. По один бік глибокого темного шляху білокорі берези в розпущених зелених косах </i>(Вас., II, 1959, 54).</div><div><b>КОСА́²</b>, и, <i>ж.</i> Сільськогосподарське знаряддя для косіння трави, збіжжя тощо, що має вигляд вузького зігнутого леза, прикріпленого до держака.</div><div><i>Свідок слави, дідівщини З вітром розмовляє, А внук косу несе в росу. За ними співає </i>(Шевч., І, 1951, 60);</div><div>[Конон:]<i> Косарі косять, А вітер повіває. Шовкова трава На коси полягає </i>(Кроп., II, 1958, 431);</div><div><i>Ти пам’ятаєш, як косили ми в полі жито, як порвав я косу, бо косив невміло </i>(Сос., II, 1958, 369);</div><div>// Ніж косарки.</div><div><span><i>В обід Тимко приїхав у село за нагостреними косами для косарки </i>(Тют., Вир, 1960, 271).</span></div><div><b>◊ Наско́чила (зайшла́, найшла́, напа́ла, тра́пила</b> <i>і т. ін.</i><b>) коса́ на ка́мінь</b> — про тих, що не хочуть уступити один одному.</div><div>[Ліхтаренко:]<i> Ви не сваріться зо мною, бо наскочила коса на камінь. Я не з тих, що бояться! </i>(К.-Карий, II, 1960, 336);</div><div>[Арсен:]<i> Сам же образив дівчину, а ждав, щоб вона вибачилась. А Надія горда ж була! </i>[Ганна:]<i> О, і не говори! Напала коса на камінь </i>(Мороз, П’єси, 1959, 242);</div><div><b>Смерть занесла́ свою́ го́стру косу́</b><i> див. </i><b>зано́сити</b>.</div><div><b>КОСА́³</b>, и, <i>ж.</i> Вузька намивна смуга суходолу в морі, річці тощо, сполучена одним кінцем із берегом; мис.</div><div><i>Човен повернув за гострий ріг піскуватої коси і вступив у Чорне море </i>(Н.-Лев., II, 1956, 225);</div><div><i>Скільки оком скинеш — леліє Дніпро, вигинаючись помежи горами, тихо миючи піскуваті коси </i>(Коцюб., III, 1956, 45);</div><div><i>На піщаній косі, що кинджалом врізалась у море, стояв маяк </i>(Шиян, Переможці, 1950, 44).</div><div><b>КОСА́⁴</b>, и, <i>ж., діал.</i> Селезінка.</div><div><span><i>Коса свиняча, що коло печінки, довгенька </i>(Номис, 1864, № 310).</span></div>"

SUPPER_NUMBERS = ("⁰","¹","²","³","⁴",
                  "⁵","⁶","⁷","⁸","⁹") # це треба адекватної роботи з омонімами а-ля КЛЮЧ¹ і КЛЮЧ²
ALL_CYRRILIC = r'[\[\]\(\)a-zA-zа-яА-ЯєЄіІїЇґҐ’.,:;?!\s…\-*«»—]'
def separate_homonyms(lexicon_artcl: str) -> tuple:
    suppernums_regex = fr"[{''.join(SUPPER_NUMBERS)}]"
    raw_homonyms = re.split(rf'(?=<div><b>[^<]+(?:{suppernums_regex}+)</b>)', lexicon_artcl)
    newlexicon = {}

    for homonym_part in raw_homonyms:
        # Шукаємо омонім разом з його індексом всередині тегів <b>
        match_word = re.search(fr'(<div><b>[^<]+({suppernums_regex}+)</b>)', homonym_part)
        if match_word:
            if match_word.group(2): #якщо є індекс, якщо це кляті омоніми. Наприклад: "КЛЮЧ¹" або "КЛЮЧ²"
                homonym_title = match_word.group(1).replace(match_word.group(2), xnum2tenB(match_word.group(2)))
                homonym_part = homonym_part.replace(match_word.group(2), xnum2tenB(match_word.group(2))) 
            else:
                homonym_title = match_word.group(1) #просто сам <div><b>КОЛОТИ́ТИСЯ</b>
            newlexicon[homonym_title] = homonym_part
    return newlexicon

