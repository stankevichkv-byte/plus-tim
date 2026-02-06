# Контент бота PlusTim - слова и задания
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Word:
    """Слово для изучения"""
    id: int
    word: str
    translation: str
    transcription: str
    example: str
    category: str
    emoji: str
    image_url: str = ""
    audio_url: str = ""

# ============ ANIMALS (Животные) ============
ANIMALS: List[Word] = [
    Word(id=1, word="cat", translation="кот", transcription="[kæt]", example="The cat is sleeping.", category="animals", emoji="🐱", image_url="https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=400", audio_url="https://ssl.gstatic.com/dictionary/static/sounds/oxford/cat--_gb_1.mp3"),
    Word(id=2, word="dog", translation="собака", transcription="[dɒg]", example="The dog is running.", category="animals", emoji="🐶", image_url="https://images.unsplash.com/photo-1543466835-00a7907e9de1?w=400", audio_url="https://ssl.gstatic.com/dictionary/static/sounds/oxford/dog--_gb_1.mp3"),
    Word(id=3, word="bird", translation="птица", transcription="[bɜːrd]", example="The bird is flying.", category="animals", emoji="🐦", image_url="https://images.unsplash.com/photo-1444464666168-49d633b86797?w=400", audio_url="https://ssl.gstatic.com/dictionary/static/sounds/oxford/bird--_gb_1.mp3"),
    Word(id=4, word="fish", translation="рыба", transcription="[fɪʃ]", example="The fish is swimming.", category="animals", emoji="🐟", image_url="https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=400", audio_url="https://ssl.gstatic.com/dictionary/static/sounds/oxford/fish--_gb_1.mp3"),
    Word(id=5, word="rabbit", translation="кролик", transcription="[ˈræbɪt]", example="The rabbit is hopping.", category="animals", emoji="🐰", image_url="https://images.unsplash.com/photo-1585110396067-bfde20b6283e?w=400", audio_url="https://ssl.gstatic.com/dictionary/static/sounds/oxford/rabbit--_gb_1.mp3"),
    Word(id=6, word="hamster", translation="хомяк", transcription="[ˈhæmstər]", example="The hamster is eating.", category="animals", emoji="🐹", image_url="https://images.unsplash.com/photo-1425082661705-1834bfd09dca?w=400", audio_url="https://ssl.gstatic.com/dictionary/static/sounds/oxford/hamster--_gb_1.mp3"),
    Word(id=7, word="turtle", translation="черепаха", transcription="[ˈtɜːrtl]", example="The turtle is slow.", category="animals", emoji="🐢", image_url="https://images.unsplash.com/photo-1437622368342-7a3d73a34c8f?w=400", audio_url="https://ssl.gstatic.com/dictionary/static/sounds/oxford/turtle--_gb_1.mp3"),
    Word(id=8, word="parrot", translation="попугай", transcription="[ˈpærət]", example="The parrot can talk.", category="animals", emoji="🦜", image_url="https://images.unsplash.com/photo-1552728089-57bdde30beb3?w=400", audio_url="https://ssl.gstatic.com/dictionary/static/sounds/oxford/parrot--_gb_1.mp3"),
    Word(id=9, word="horse", translation="лошадь", transcription="[hɔːrs]", example="The horse is strong.", category="animals", emoji="🐴", image_url="https://images.unsplash.com/photo-1553284965-83fd3e82fa5a?w=400", audio_url="https://ssl.gstatic.com/dictionary/static/sounds/oxford/horse--_gb_1.mp3"),
    Word(id=10, word="elephant", translation="слон", transcription="[ˈelɪfənt]", example="The elephant has a long trunk.", category="animals", emoji="🐘", image_url="https://images.unsplash.com/photo-1557050543-4d5f4e07ef46?w=400", audio_url="https://ssl.gstatic.com/dictionary/static/sounds/oxford/elephant--_gb_1.mp3"),
]

# ============ FOOD (Еда) ============
FOOD: List[Word] = [
    Word(id=101, word="apple", translation="яблоко", transcription="[ˈæpl]", example="I eat an apple every day.", category="food", emoji="🍎", image_url="https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=400", audio_url="https://ssl.gstatic.com/dictionary/static/sounds/oxford/apple--_gb_1.mp3"),
    Word(id=102, word="banana", translation="банан", transcription="[bəˈnɑːnə]", example="Monkeys love bananas.", category="food", emoji="🍌", image_url="https://images.unsplash.com/photo-1603833665858-e61d17a86279?w=400", audio_url="https://ssl.gstatic.com/dictionary/static/sounds/oxford/banana--_gb_1.mp3"),
    Word(id=103, word="bread", translation="хлеб", transcription="[bred]", example="I eat bread for breakfast.", category="food", emoji="🍞", image_url="https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400", audio_url="https://ssl.gstatic.com/dictionary/static/sounds/oxford/bread--_gb_1.mp3"),
    Word(id=104, word="cheese", translation="сыр", transcription="[tʃiːz]", example=" Mice like cheese.", category="food", emoji="🧀", image_url="https://images.unsplash.com/photo-1618156760140-d79d48bb ce1e?w=400", audio_url="https://ssl.gstatic.com/dictionary/static/sounds/oxford/cheese--_gb_1.mp3"),
    Word(id=105, word="chocolate", translation="шоколад", transcription="[ˈtʃɒklət]", example="I love chocolate ice cream.", category="food", emoji="🍫", image_url="https://images.unsplash.com/photo-1481391319762-47dff72954d9?w=400", audio_url="https://ssl.gstatic.com/dictionary/static/sounds/oxford/chocolate--_gb_1.mp3"),
    Word(id=106, word="egg", translation="яйцо", transcription="[eg]", example="I have eggs for breakfast.", category="food", emoji="🥚", image_url="https://images.unsplash.com/photo-1486899138638-9a5c9b919d26?w=400", audio_url="https://ssl.gstatic.com/dictionary/static/sounds/oxford/egg--_gb_1.mp3"),
    Word(id=107, word="ice cream", translation="мороженое", transcription="[aɪs kriːm]", example="Vanilla ice cream is yummy.", category="food", emoji="🍦", image_url="https://images.unsplash.com/photo-1560008581-09826d1de69e?w=400", audio_url="https://ssl.gstatic.com/dictionary/static/sounds/oxford/ice%20cream--_gb_1.mp3"),
    Word(id=108, word="milk", translation="молоко", transcription="[mɪlk]", example="Cats love milk.", category="food", emoji="🥛", image_url="https://images.unsplash.com/photo-1563636619-e9143da7973b?w=400", audio_url="https://ssl.gstatic.com/dictionary/static/sounds/oxford/milk--_gb_1.mp3"),
    Word(id=109, word="orange", translation="апельсин", transcription="[ˈɒrɪndʒ]", example="An orange is juicy.", category="food", emoji="🍊", image_url="https://images.unsplash.com/photo-1547514701-42782101795e?w=400", audio_url="https://ssl.gstatic.com/dictionary/static/sounds/oxford/orange--_gb_1.mp3"),
    Word(id=110, word="pizza", translation="пицца", transcription="[ˈpiːtsə]", example="Pizza is my favorite food.", category="food", emoji="🍕", image_url="https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=400", audio_url="https://ssl.gstatic.com/dictionary/static/sounds/oxford/pizza--_gb_1.mp3"),
]

# ============ COLORS (Цвета) ============
COLORS: List[Word] = [
    Word(id=201, word="red", translation="красный", transcription="[red]", example="An apple is red.", category="colors", emoji="🔴", image_url="https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400", audio_url="https://ssl.gstatic.com/dictionary/static/sounds/oxford/red--_gb_1.mp3"),
    Word(id=202, word="blue", translation="синий", transcription="[bluː]", example="The sky is blue.", category="colors", emoji="🔵", image_url="https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400", audio_url="https://ssl.gstatic.com/dictionary/static/sounds/oxford/blue--_gb_1.mp3"),
    Word(id=203, word="green", translation="зелёный", transcription="[griːn]", example="Grass is green.", category="colors", emoji="🟢", image_url="https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400", audio_url="https://ssl.gstatic.com/dictionary/static/sounds/oxford/green--_gb_1.mp3"),
    Word(id=204, word="yellow", translation="жёлтый", transcription="[ˈjeləʊ]", example="Bananas are yellow.", category="colors", emoji="🟡", image_url="https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400", audio_url="https://ssl.gstatic.com/dictionary/static/sounds/oxford/yellow--_gb_1.mp3"),
    Word(id=205, word="orange", translation="оранжевый", transcription="[ˈɒrɪndʒ]", example="An orange is orange.", category="colors", emoji="🟠", image_url="https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400", audio_url="https://ssl.gstatic.com/dictionary/static/sounds/oxford/orange--_gb_1.mp3"),
    Word(id=206, word="purple", translation="фиолетовый", transcription="[ˈpɜːpl]", example="Grapes are purple.", category="colors", emoji="🟣", image_url="https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400", audio_url="https://ssl.gstatic.com/dictionary/static/sounds/oxford/purple--_gb_1.mp3"),
    Word(id=207, word="pink", translation="розовый", transcription="[pɪŋk]", example="Pigs are pink.", category="colors", emoji="💗", image_url="https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400", audio_url="https://ssl.gstatic.com/dictionary/static/sounds/oxford/pink--_gb_1.mp3"),
    Word(id=208, word="white", translation="белый", transcription="[waɪt]", example="Snow is white.", category="colors", emoji="⚪", image_url="https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400", audio_url="https://ssl.gstatic.com/dictionary/static/sounds/oxford/white--_gb_1.mp3"),
    Word(id=209, word="black", translation="чёрный", transcription="[blæk]", example="A cat can be black.", category="colors", emoji="⚫", image_url="https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400", audio_url="https://ssl.gstatic.com/dictionary/static/sounds/oxford/black--_gb_1.mp3"),
    Word(id=210, word="brown", translation="коричневый", transcription="[braʊn]", example="Chocolate is brown.", category="colors", emoji="🟤", image_url="https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400", audio_url="https://ssl.gstatic.com/dictionary/static/sounds/oxford/brown--_gb_1.mp3"),
]

# ============ NUMBERS (Числа) ============
NUMBERS: List[Word] = [
    Word(id=301, word="one", translation="один", transcription="[wʌn]", example="I have one apple.", category="numbers", emoji="1️⃣", image_url="", audio_url="https://ssl.gstatic.com/dictionary/static/sounds/oxford/one--_gb_1.mp3"),
    Word(id=302, word="two", translation="два", transcription="[tuː]", example="I have two dogs.", category="numbers", emoji="2️⃣", image_url="", audio_url="https://ssl.gstatic.com/dictionary/static/sounds/oxford/two--_gb_1.mp3"),
    Word(id=303, word="three", translation="три", transcription="[θriː]", example="Three cats are sleeping.", category="numbers", emoji="3️⃣", image_url="", audio_url="https://ssl.gstatic.com/dictionary/static/sounds/oxford/three--_gb_1.mp3"),
    Word(id=304, word="four", translation="четыре", transcription="[fɔːr]", example="Four birds are flying.", category="numbers", emoji="4️⃣", image_url="", audio_url="https://ssl.gstatic.com/dictionary/static/sounds/oxford/four--_gb_1.mp3"),
    Word(id=305, word="five", translation="пять", transcription="[faɪv]", example="Five stars! Great job!", category="numbers", emoji="5️⃣", image_url="", audio_url="https://ssl.gstatic.com/dictionary/static/sounds/oxford/five--_gb_1.mp3"),
    Word(id=306, word="six", translation="шесть", transcription="[sɪks]", example="I have six coins.", category="numbers", emoji="6️⃣", image_url="", audio_url="https://ssl.gstatic.com/dictionary/static/sounds/oxford/six--_gb_1.mp3"),
    Word(id=307, word="seven", translation="семь", transcription="[ˈsevn]", example="Seven days in a week.", category="numbers", emoji="7️⃣", image_url="", audio_url="https://ssl.gstatic.com/dictionary/static/sounds/oxford/seven--_gb_1.mp3"),
    Word(id=308, word="eight", translation="восемь", transcription="[eɪt]", example="Eight apples on the table.", category="numbers", emoji="8️⃣", image_url="", audio_url="https://ssl.gstatic.com/dictionary/static/sounds/oxford/eight--_gb_1.mp3"),
    Word(id=309, word="nine", translation="девять", transcription="[naɪn]", example="Nine planets in the solar system.", category="numbers", emoji="9️⃣", image_url="", audio_url="https://ssl.gstatic.com/dictionary/static/sounds/oxford/nine--_gb_1.mp3"),
    Word(id=310, word="ten", translation="десять", transcription="[ten]", example="Ten fingers on my hands.", category="numbers", emoji="🔟", image_url="", audio_url="https://ssl.gstatic.com/dictionary/static/sounds/oxford/ten--_gb_1.mp3"),
]

# ============ FAMILY (Семья) ============
FAMILY: List[Word] = [
    Word(id=401, word="mother", translation="мама", transcription="[ˈmʌðər]", example="My mother cooks dinner.", category="family", emoji="👩", image_url="https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=400", audio_url="https://ssl.gstatic.com/dictionary/static/sounds/oxford/mother--_gb_1.mp3"),
    Word(id=402, word="father", translation="папа", transcription="[ˈfɑːðər]", example="My father plays football.", category="family", emoji="👨", image_url="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400", audio_url="https://ssl.gstatic.com/dictionary/static/sounds/oxford/father--_gb_1.mp3"),
    Word(id=403, word="sister", translation="сестра", transcription="[ˈsɪstər]", example="My sister reads books.", category="family", emoji="👧", image_url="https://images.unsplash.com/photo-1519340241574-2cec6aef0c01?w=400", audio_url="https://ssl.gstatic.com/dictionary/static/sounds/oxford/sister--_gb_1.mp3"),
    Word(id=404, word="brother", translation="брат", transcription="[ˈbrʌðər]", example="My brother plays games.", category="family", emoji="👦", image_url="https://images.unsplash.com/photo-1503454537195-1dcabb73ffb9?w=400", audio_url="https://ssl.gstatic.com/dictionary/static/sounds/oxford/brother--_gb_1.mp3"),
    Word(id=405, word="grandmother", translation="бабушка", transcription="[ˈɡrænmʌðər]", example="My grandmother tells stories.", category="family", emoji="👵", image_url="https://images.unsplash.com/photo-1551836022-d5d88e9218df?w=400", audio_url="https://ssl.gstatic.com/dictionary/static/sounds/oxford/grandmother--_gb_1.mp3"),
    Word(id=406, word="grandfather", translation="дедушка", transcription="[ˈɡrænfɑːðər]", example="My grandfather walks in the park.", category="family", emoji="👴", image_url="https://images.unsplash.com/photo-1476231682828-37efd4478321?w=400", audio_url="https://ssl.gstatic.com/dictionary/static/sounds/oxford/grandfather--_gb_1.mp3"),
    Word(id=407, word="parents", translation="родители", transcription="[ˈpeərənts]", example="My parents love me.", category="family", emoji="👨‍👩‍👧", image_url="https://images.unsplash.com/photo-1519683109079-d5f539e1542f?w=400", audio_url="https://ssl.gstatic.com/dictionary/static/sounds/oxford/parents--_gb_1.mp3"),
    Word(id=408, word="children", translation="дети", transcription="[ˈtʃɪldrən]", example="The children are playing.", category="family", emoji="👶", image_url="https://images.unsplash.com/photo-1503454537195-1dcabb73ffb9?w=400", audio_url="https://ssl.gstatic.com/dictionary/static/sounds/oxford/children--_gb_1.mp3"),
    Word(id=409, word="friend", translation="друг", transcription="[frend]", example="My friend is funny.", category="family", emoji="👫", image_url="https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=400", audio_url="https://ssl.gstatic.com/dictionary/static/sounds/oxford/friend--_gb_1.mp3"),
    Word(id=410, word="family", translation="семья", transcription="[ˈfæmɪli]", example="I love my family.", category="family", emoji="👨‍👩‍👦‍👦", image_url="https://images.unsplash.com/photo-1519683109079-d5f539e1542f?w=400", audio_url="https://ssl.gstatic.com/dictionary/static/sounds/oxford/family--_gb_1.mp3"),
]

# ============ BODY PARTS (Части тела) ============
BODY_PARTS: List[Word] = [
    Word(id=501, word="head", translation="голова", transcription="[hed]", example="I have a headache.", category="body_parts", emoji="🧠", image_url="https://images.unsplash.com/photo-1559757175-5700dde675bc?w=400", audio_url="https://ssl.gstatic.com/dictionary/static/sounds/oxford/head--_gb_1.mp3"),
    Word(id=502, word="eye", translation="глаз", transcription="[aɪ]", example="I have two eyes.", category="body_parts", emoji="👁️", image_url="https://images.unsplash.com/photo-1551601651-2a8555f1a136?w=400", audio_url="https://ssl.gstatic.com/dictionary/static/sounds/oxford/eye--_gb_1.mp3"),
    Word(id=503, word="ear", translation="ухо", transcription="[ɪər]", example="I hear with my ears.", category="body_parts", emoji="👂", image_url="https://images.unsplash.com/photo-1559757175-5700dde675bc?w=400", audio_url="https://ssl.gstatic.com/dictionary/static/sounds/oxford/ear--_gb_1.mp3"),
    Word(id=504, word="nose", translation="нос", transcription="[nəʊz]", example="My nose is red.", category="body_parts", emoji="👃", image_url="https://images.unsplash.com/photo-1559757175-5700dde675bc?w=400", audio_url="https://ssl.gstatic.com/dictionary/static/sounds/oxford/nose--_gb_1.mp3"),
    Word(id=505, word="mouth", translation="рот", transcription="[maʊθ]", example="Open your mouth.", category="body_parts", emoji="👄", image_url="https://images.unsplash.com/photo-1559757175-5700dde675bc?w=400", audio_url="https://ssl.gstatic.com/dictionary/static/sounds/oxford/mouth--_gb_1.mp3"),
    Word(id=506, word="hand", translation="рука", transcription="[hænd]", example="I write with my hand.", category="body_parts", emoji="✍️", image_url="https://images.unsplash.com/photo-1559757175-5700dde675bc?w=400", audio_url="https://ssl.gstatic.com/dictionary/static/sounds/oxford/hand--_gb_1.mp3"),
    Word(id=507, word="arm", translation="рука", transcription="[ɑːrm]", example="I lift my arm.", category="body_parts", emoji="💪", image_url="https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400", audio_url="https://ssl.gstatic.com/dictionary/static/sounds/oxford/arm--_gb_1.mp3"),
    Word(id=508, word="leg", translation="нога", transcription="[leg]", example="I stand on my legs.", category="body_parts", emoji="🦵", image_url="https://images.unsplash.com/photo-1559757175-5700dde675bc?w=400", audio_url="https://ssl.gstatic.com/dictionary/static/sounds/oxford/leg--_gb_1.mp3"),
    Word(id=509, word="foot", translation="ступня", transcription="[fʊt]", example="I have two feet.", category="body_parts", emoji="🦶", image_url="https://images.unsplash.com/photo-1559757175-5700dde675bc?w=400", audio_url="https://ssl.gstatic.com/dictionary/static/sounds/oxford/foot--_gb_1.mp3"),
    Word(id=510, word="heart", translation="сердце", transcription="[hɑːrt]", example="My heart beats fast.", category="body_parts", emoji="❤️", image_url="https://images.unsplash.com/photo-1559757175-5700dde675bc?w=400", audio_url="https://ssl.gstatic.com/dictionary/static/sounds/oxford/heart--_gb_1.mp3"),
]

# Объединяем все слова
ALL_WORDS = ANIMALS + FOOD + COLORS + NUMBERS + FAMILY + BODY_PARTS
WORDS = ALL_WORDS

# Категории
CATEGORIES = {
    "animals": {"name": "🐾 Животные", "emoji": "🐾", "words_count": len(ANIMALS)},
    "food": {"name": "🍎 Еда", "emoji": "🍎", "words_count": len(FOOD)},
    "colors": {"name": "🌈 Цвета", "emoji": "🌈", "words_count": len(COLORS)},
    "numbers": {"name": "🔢 Числа", "emoji": "🔢", "words_count": len(NUMBERS)},
    "family": {"name": "👨‍👩‍👧 Семья", "emoji": "👨‍👩‍👧", "words_count": len(FAMILY)},
    "body_parts": {"name": "🧘 Части тела", "emoji": "🧘", "words_count": len(BODY_PARTS)},
}

# Все слова для быстрого доступа
WORD_LISTS = {
    "animals": ANIMALS,
    "food": FOOD,
    "colors": COLORS,
    "numbers": NUMBERS,
    "family": FAMILY,
    "body_parts": BODY_PARTS,
}

# Неправильные ответы для викторин
DISTRACTORS = {
    # Animals
    "cat": ["dog", "bird", "fish", "rabbit"],
    "dog": ["cat", "bird", "fish", "horse"],
    "bird": ["cat", "dog", "fish", "parrot"],
    "fish": ["cat", "bird", "dog", "rabbit"],
    "rabbit": ["cat", "dog", "bird", "hamster"],
    "hamster": ["rabbit", "cat", "dog", "mouse"],
    "turtle": ["fish", "bird", "cat", "snake"],
    "parrot": ["bird", "cat", "dog", "chicken"],
    "horse": ["dog", "cat", "bird", "elephant"],
    "elephant": ["horse", "cat", "dog", "lion"],
    # Food
    "apple": ["banana", "orange", "grape", "pear"],
    "banana": ["apple", "orange", "lemon", "mango"],
    "bread": ["cake", "pizza", "cheese", "butter"],
    "cheese": ["bread", "milk", "yogurt", "butter"],
    "chocolate": ["candy", "ice cream", "cake", "cookie"],
    "egg": ["meat", "fish", "chicken", "bread"],
    "ice cream": ["cake", "chocolate", "candy", "fruit"],
    "milk": ["water", "juice", "coffee", "tea"],
    "orange": ["apple", "banana", "lemon", "grape"],
    "pizza": ["burger", "pasta", "bread", "cake"],
    # Colors
    "red": ["green", "blue", "yellow", "orange"],
    "blue": ["green", "red", "yellow", "purple"],
    "green": ["red", "blue", "yellow", "brown"],
    "yellow": ["green", "red", "orange", "white"],
    "orange": ["yellow", "red", "apple", "brown"],
    "purple": ["blue", "red", "pink", "white"],
    "pink": ["red", "purple", "white", "brown"],
    "white": ["black", "gray", "yellow", "brown"],
    "black": ["white", "gray", "brown", "blue"],
    "brown": ["black", "green", "yellow", "orange"],
    # Numbers
    "one": ["two", "three", "four", "five"],
    "two": ["one", "three", "four", "five"],
    "three": ["one", "two", "four", "five"],
    "four": ["one", "two", "three", "five"],
    "five": ["one", "two", "three", "four"],
    "six": ["seven", "eight", "five", "four"],
    "seven": ["six", "eight", "five", "six"],
    "eight": ["seven", "six", "five", "nine"],
    "nine": ["eight", "seven", "six", "ten"],
    "ten": ["nine", "eight", "seven", "six"],
    # Family
    "mother": ["father", "sister", "brother", "grandmother"],
    "father": ["mother", "sister", "brother", "grandfather"],
    "sister": ["brother", "mother", "father", "friend"],
    "brother": ["sister", "mother", "father", "friend"],
    "grandmother": ["grandfather", "mother", "father", "sister"],
    "grandfather": ["grandmother", "mother", "father", "brother"],
    "parents": ["children", "friends", "family", "siblings"],
    "children": ["parents", "family", "friends", "adults"],
    "friend": ["family", "brother", "sister", "mother"],
    "family": ["friend", "parents", "children", "relatives"],
    # Body Parts
    "head": ["face", "eye", "nose", "mouth"],
    "eye": ["ear", "nose", "hand", "head"],
    "ear": ["eye", "nose", "mouth", "hand"],
    "nose": ["mouth", "ear", "eye", "face"],
    "mouth": ["nose", "eye", "ear", "hand"],
    "hand": ["arm", "foot", "leg", "finger"],
    "arm": ["hand", "leg", "foot", "shoulder"],
    "leg": ["foot", "arm", "hand", "knee"],
    "foot": ["leg", "arm", "hand", "toe"],
    "heart": ["brain", "stomach", "lung", "chest"],
}

# Сообщения для игры
MESSAGES = {
    "welcome": "🎮 Привет! Готов к уроку?",
    "discovery_title": "📖 Новое слово!",
    "listen_again": "🔊 Послушать ещё",
    "next_word": "➡️ Дальше",
    "quiz_title": "🎯 Угадай по картинке!",
    "missing_letter_title": "✏️ Пропавшая буква!",
    "speed_title": "⚡ Скоростной раунд!",
    "correct": "🎉 Правильно! +{xp}⭐",
    "wrong": "🤔 Не совсем... Попробуй ещё!",
    "lesson_complete": "🏆 Урок завершён!",
    "xp_earned": "⭐ Всего за урок: {xp} звёзд",
    "streak": "🔥 Стрик: {streak} дней!",
    "new_achievement": "🎊 Новое достижение!",
    "keep_going": "💪 Так держать!",
    "come_back": "⏰ Возвращайся завтра!",
}


def get_word_by_id(word_id: int) -> Word:
    """Получить слово по ID"""
    for word in WORDS:
        if word.id == word_id:
            return word
    return None


def get_words_for_category(category: str) -> List[Word]:
    """Получить все слова категории"""
    return WORD_LISTS.get(category, [])


def generate_quiz_options(correct_word, distractors: Dict[str, List[str]] = None) -> List[str]:
    """Сгенерировать варианты ответа для викторины"""
    if distractors is None:
        distractors = DISTRACTORS
    
    # Поддержка Word dataclass и словаря
    word_text = correct_word.word if hasattr(correct_word, 'word') else correct_word['word']
    
    options = [word_text]
    
    if word_text in distractors:
        wrong_options = distractors[word_text]
        options.extend(wrong_options[:3])
    
    import random
    random.shuffle(options)
    
    return options


def get_missing_letter_word(word) -> tuple:
    """Получить слово с пропущенной буквой и варианты"""
    import random
    
    # Поддержка Word dataclass и словаря
    word_text = word.word if hasattr(word, 'word') else word['word']
    
    if len(word_text) > 3:
        pos = random.randint(1, len(word_text) - 2)
    else:
        pos = random.randint(0, len(word_text) - 1)
    
    correct_letter = word_text[pos]
    masked_word = word_text[:pos] + "_" + word_text[pos + 1:]
    
    alphabet = [chr(i) for i in range(ord('a'), ord('z') + 1)]
    alphabet.remove(correct_letter)
    wrong_letters = random.sample(alphabet, 3)
    
    options = [correct_letter] + wrong_letters
    random.shuffle(options)
    
    return masked_word, options, correct_letter


def get_random_words(count: int, category: str = "animals") -> List[Word]:
    """Получить случайные слова для урока"""
    import random
    
    category_words = get_words_for_category(category)
    
    if len(category_words) <= count:
        return category_words
    
    return random.sample(category_words, count)