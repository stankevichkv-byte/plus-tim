"""
Заполнение БД контентом для PlusTim - Расширенная версия
15 категорий, 10 слов в каждой = 150 слов
"""
import sqlite3
import os
import json
import random

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'plustim.db')

# Расширенные слова для уроков
WORDS_DATA = {
    "animals": [  # Животные
        {"word": "cat", "translation": "кот", "transcription": "[kæt]", "emoji": "🐱", "example": "The cat is sleeping."},
        {"word": "dog", "translation": "собака", "transcription": "[dɒg]", "emoji": "🐶", "example": "The dog is running."},
        {"word": "bird", "translation": "птица", "transcription": "[bɜːrd]", "emoji": "🐦", "example": "The bird is flying."},
        {"word": "fish", "translation": "рыба", "transcription": "[fɪʃ]", "emoji": "🐟", "example": "The fish is swimming."},
        {"word": "rabbit", "translation": "кролик", "transcription": "[ˈræbɪt]", "emoji": "🐰", "example": "The rabbit is hopping."},
        {"word": "horse", "translation": "лошадь", "transcription": "[hɔːrs]", "emoji": "🐴", "example": "The horse is galloping."},
        {"word": "cow", "translation": "корова", "transcription": "[kaʊ]", "emoji": "🐄", "example": "The cow is eating grass."},
        {"word": "pig", "translation": "свинья", "transcription": "[pɪɡ]", "emoji": "🐷", "example": "The pig is oinking."},
        {"word": "sheep", "translation": "овца", "transcription": "[ʃiːp]", "emoji": "🐑", "example": "The sheep is baaing."},
        {"word": "chicken", "translation": "курица", "transcription": "[ˈtʃɪkɪn]", "emoji": "🐔", "example": "The chicken is clucking."},
    ],
    "food": [  # Еда
        {"word": "apple", "translation": "яблоко", "transcription": "[ˈæpl]", "emoji": "🍎", "example": "I eat an apple."},
        {"word": "bread", "translation": "хлеб", "transcription": "[bred]", "emoji": "🍞", "example": "I eat bread for breakfast."},
        {"word": "milk", "translation": "молоко", "transcription": "[mɪlk]", "emoji": "🥛", "example": "I drink milk."},
        {"word": "cheese", "translation": "сыр", "transcription": "[tʃiːz]", "emoji": "🧀", "example": "I like cheese."},
        {"word": "water", "translation": "вода", "transcription": "[ˈwɔːtər]", "emoji": "💧", "example": "Water is essential."},
        {"word": "banana", "translation": "банан", "transcription": "[bəˈnɑːnə]", "emoji": "🍌", "example": "Bananas are yellow."},
        {"word": "egg", "translation": "яйцо", "transcription": "[eɡ]", "emoji": "🥚", "example": "I eat eggs for breakfast."},
        {"word": "pizza", "translation": "пицца", "transcription": "[ˈpiːtsə]", "emoji": "🍕", "example": "Pizza is delicious."},
        {"word": "ice cream", "translation": "мороженое", "transcription": "[aɪs kriːm]", "emoji": "🍦", "example": "Ice cream is cold."},
        {"word": "cake", "translation": "торт", "transcription": "[keɪk]", "emoji": "🍰", "example": "This is my birthday cake."},
    ],
    "colors": [  # Цвета
        {"word": "red", "translation": "красный", "transcription": "[red]", "emoji": "🔴", "example": "An apple is red."},
        {"word": "blue", "translation": "синий", "transcription": "[bluː]", "emoji": "🔵", "example": "The sky is blue."},
        {"word": "green", "translation": "зелёный", "transcription": "[griːn]", "emoji": "🟢", "example": "Grass is green."},
        {"word": "yellow", "translation": "жёлтый", "transcription": "[ˈjeləʊ]", "emoji": "🟡", "example": "The sun is yellow."},
        {"word": "orange", "translation": "оранжевый", "transcription": "[ˈɒrɪndʒ]", "emoji": "🟠", "example": "Oranges are orange."},
        {"word": "purple", "translation": "фиолетовый", "transcription": "[ˈpɜːpl]", "emoji": "🟣", "example": "Grapes are purple."},
        {"word": "pink", "translation": "розовый", "transcription": "[pɪŋk]", "emoji": "🎀", "example": "Pink is a pretty color."},
        {"word": "black", "translation": "чёрный", "transcription": "[blæk]", "emoji": "⚫", "example": "The night is black."},
        {"word": "white", "translation": "белый", "transcription": "[waɪt]", "emoji": "⚪", "example": "Snow is white."},
        {"word": "brown", "translation": "коричневый", "transcription": "[braʊn]", "emoji": "🟤", "example": "Chocolate is brown."},
    ],
    "numbers": [  # Числа
        {"word": "one", "translation": "один", "transcription": "[wʌn]", "emoji": "1️⃣", "example": "I have one apple."},
        {"word": "two", "translation": "два", "transcription": "[tuː]", "emoji": "2️⃣", "example": "I have two dogs."},
        {"word": "three", "translation": "три", "transcription": "[θriː]", "emoji": "3️⃣", "example": "Three cats are sleeping."},
        {"word": "four", "translation": "четыре", "transcription": "[fɔːr]", "emoji": "4️⃣", "example": "Four seasons in a year."},
        {"word": "five", "translation": "пять", "transcription": "[faɪv]", "emoji": "5️⃣", "example": "Five fingers on hand."},
        {"word": "six", "translation": "шесть", "transcription": "[sɪks]", "emoji": "6️⃣", "example": "Six sides on a cube."},
        {"word": "seven", "translation": "семь", "transcription": "[ˈsevn]", "emoji": "7️⃣", "example": "Seven days in a week."},
        {"word": "eight", "translation": "восемь", "transcription": "[eɪt]", "emoji": "8️⃣", "example": "Eight legs on a spider."},
        {"word": "nine", "translation": "девять", "transcription": "[naɪn]", "emoji": "9️⃣", "example": "Nine planets (maybe)."},
        {"word": "ten", "translation": "десять", "transcription": "[ten]", "emoji": "🔟", "example": "Ten toes on feet."},
    ],
    "family": [  # Семья
        {"word": "mother", "translation": "мама", "transcription": "[ˈmʌðər]", "emoji": "👩", "example": "My mother cooks dinner."},
        {"word": "father", "translation": "папа", "transcription": "[ˈfɑːðər]", "emoji": "👨", "example": "My father plays football."},
        {"word": "sister", "translation": "сестра", "transcription": "[ˈsɪstər]", "emoji": "👧", "example": "My sister reads books."},
        {"word": "brother", "translation": "брат", "transcription": "[ˈbrʌðər]", "emoji": "👦", "example": "My brother plays games."},
        {"word": "grandmother", "translation": "бабушка", "transcription": "[ˈɡrænmʌðər]", "emoji": "👵", "example": "Grandmother tells stories."},
        {"word": "grandfather", "translation": "дедушка", "transcription": "[ˈɡrænfɑːðər]", "emoji": "👴", "example": "Grandfather gardens."},
        {"word": "son", "translation": "сын", "transcription": "[sʌn]", "emoji": "👦", "example": "My son is funny."},
        {"word": "daughter", "translation": "дочь", "transcription": "[ˈdɔːtər]", "emoji": "👧", "example": "My daughter sings."},
        {"word": "parents", "translation": "родители", "transcription": "[ˈpeərənts]", "emoji": "👨‍👩‍👧", "example": "My parents love me."},
        {"word": "children", "translation": "дети", "transcription": "[ˈtʃɪldrən]", "emoji": "👶", "example": "Children are playing."},
    ],
    "body": [  # Части тела
        {"word": "head", "translation": "голова", "transcription": "[hed]", "emoji": "🧠", "example": "Use your head!"},
        {"word": "eye", "translation": "глаз", "transcription": "[aɪ]", "emoji": "👁️", "example": "I see with my eye."},
        {"word": "ear", "translation": "ухо", "transcription": "[ɪər]", "emoji": "👂", "example": "I hear with my ear."},
        {"word": "nose", "translation": "нос", "transcription": "[nəʊz]", "emoji": "👃", "example": "I smell with my nose."},
        {"word": "mouth", "translation": "рот", "transcription": "[maʊθ]", "emoji": "👄", "example": "I speak with my mouth."},
        {"word": "hand", "translation": "рука", "transcription": "[hænd]", "emoji": "✋", "example": "I write with my hand."},
        {"word": "foot", "translation": "нога", "transcription": "[fʊt]", "emoji": "🦶", "example": "I walk with my foot."},
        {"word": "arm", "translation": "рука (рука)", "transcription": "[ɑːrm]", "emoji": "💪", "example": "I lift with my arm."},
        {"word": "leg", "translation": "нога (нога)", "transcription": "[leɡ]", "emoji": "🦵", "example": "I run with my leg."},
        {"word": "heart", "translation": "сердце", "transcription": "[hɑːrt]", "emoji": "❤️", "example": "My heart beats."},
    ],
    "clothes": [  # Одежда
        {"word": "shirt", "translation": "рубашка", "transcription": "[ʃɜːrt]", "emoji": "👔", "example": "I wear a shirt."},
        {"word": "pants", "translation": "брюки", "transcription": "[pænts]", "emoji": "👖", "example": "These are my pants."},
        {"word": "dress", "translation": "платье", "transcription": "[dres]", "emoji": "👗", "example": "She wears a dress."},
        {"word": "shoes", "translation": "туфли", "transcription": "[ʃuːz]", "emoji": "👟", "example": "Put on your shoes."},
        {"word": "hat", "translation": "шляпа", "transcription": "[hæt]", "emoji": "👒", "example": "Hat keeps sun away."},
        {"word": "coat", "translation": "пальто", "transcription": "[kəʊt]", "emoji": "🧥", "example": "Coat is warm."},
        {"word": "sock", "translation": "носок", "transcription": "[sɒk]", "emoji": "🧦", "example": "One sock is missing."},
        {"word": "gloves", "translation": "перчатки", "transcription": "[ɡlʌvz]", "emoji": "🧤", "example": "Gloves keep hands warm."},
        {"word": "scarf", "translation": "шарф", "transcription": "[skɑːrf]", "emoji": "🧣", "example": "Scarf is around neck."},
        {"word": "umbrella", "translation": "зонт", "transcription": "[ʌmˈbrelə]", "emoji": "☂️", "example": "Umbrella keeps dry."},
    ],
    "weather": [  # Погода
        {"word": "sun", "translation": "солнце", "transcription": "[sʌn]", "emoji": "☀️", "example": "The sun is shining."},
        {"word": "rain", "translation": "дождь", "transcription": "[reɪn]", "emoji": "🌧️", "example": "Rain is falling."},
        {"word": "snow", "translation": "снег", "transcription": "[snəʊ]", "emoji": "❄️", "example": "Snow is falling."},
        {"word": "wind", "translation": "ветер", "transcription": "[wɪnd]", "emoji": "💨", "example": "Wind is blowing."},
        {"word": "cloud", "translation": "облако", "transcription": "[klaʊd]", "emoji": "☁️", "example": "Cloud in the sky."},
        {"word": "storm", "translation": "буря", "transcription": "[stɔːrm]", "emoji": "⛈️", "example": "Storm is coming."},
        {"word": "hot", "translation": "жаркий", "transcription": "[hɒt]", "emoji": "🔥", "example": "It's very hot today."},
        {"word": "cold", "translation": "холодный", "transcription": "[kəʊld]", "emoji": "🧊", "example": "It's cold outside."},
        {"word": "warm", "translation": "тёплый", "transcription": "[wɔːrm]", "emoji": "🟤", "example": "It's warm today."},
        {"word": "rainbow", "translation": "радуга", "transcription": "[ˈreɪnbəʊ]", "emoji": "🌈", "example": "Rainbow after rain."},
    ],
    "school": [  # Школа
        {"word": "book", "translation": "книга", "transcription": "[bʊk]", "emoji": "📚", "example": "I read a book."},
        {"word": "pen", "translation": "ручка", "transcription": "[pen]", "emoji": "🖊️", "example": "I write with a pen."},
        {"word": "pencil", "translation": "карандаш", "transcription": "[ˈpensl]", "emoji": "✏️", "example": "I draw with pencil."},
        {"word": "notebook", "translation": "тетрадь", "transcription": "[ˈnəʊtbʊk]", "emoji": "📓", "example": "I write in notebook."},
        {"word": "teacher", "translation": "учитель", "transcription": "[ˈtiːtʃər]", "emoji": "👨‍🏫", "example": "Teacher helps us learn."},
        {"word": "student", "translation": "ученик", "transcription": "[ˈstjuːdnt]", "emoji": "🎒", "example": "Student goes to school."},
        {"word": "desk", "translation": "парта", "transcription": "[desk]", "emoji": "🪑", "example": "I sit at the desk."},
        {"word": "chalkboard", "translation": "доска", "transcription": "[ˈtʃɔːkbɔːrd]", "emoji": "📋", "example": "Teacher writes on board."},
        {"word": "backpack", "translation": "рюкзак", "transcription": "[ˈbækpæk]", "emoji": "🎒", "example": "Backpack carries books."},
        {"word": "homework", "translation": "домашнее задание", "transcription": "[ˈhəʊmwɜːrk]", "emoji": "📝", "example": "I do homework."},
    ],
    "time": [  # Время
        {"word": "morning", "translation": "утро", "transcription": "[ˈmɔːrnɪŋ]", "emoji": "🌅", "example": "Good morning!"},
        {"word": "afternoon", "translation": "день", "transcription": "[ˌæftərˈnuːn]", "emoji": "☀️", "example": "See you in afternoon."},
        {"word": "evening", "translation": "вечер", "transcription": "[ˈiːvnɪŋ]", "emoji": "🌆", "example": "Evening is here."},
        {"word": "night", "translation": "ночь", "transcription": "[naɪt]", "emoji": "🌙", "example": "Good night!"},
        {"word": "today", "translation": "сегодня", "transcription": "[təˈdeɪ]", "emoji": "📅", "example": "Today is Monday."},
        {"word": "yesterday", "translation": "вчера", "transcription": "[ˈjestədeɪ]", "emoji": "📆", "example": "Yesterday was Sunday."},
        {"word": "tomorrow", "translation": "завтра", "transcription": "[təˈmɒrəʊ]", "emoji": "📌", "example": "Tomorrow is Tuesday."},
        {"word": "week", "translation": "неделя", "transcription": "[wiːk]", "emoji": "📆", "example": "One week has seven days."},
        {"word": "month", "translation": "месяц", "transcription": "[mʌnθ]", "emoji": "🗓️", "example": "January is a month."},
        {"word": "year", "translation": "год", "transcription": "[jɪər]", "emoji": "🗓️", "example": "One year has twelve months."},
    ],
    "transport": [  # Транспорт
        {"word": "car", "translation": "машина", "transcription": "[kɑːr]", "emoji": "🚗", "example": "Car drives on road."},
        {"word": "bus", "translation": "автобус", "transcription": "[bʌs]", "emoji": "🚌", "example": "Bus takes many people."},
        {"word": "train", "translation": "поезд", "transcription": "[treɪn]", "emoji": "🚂", "example": "Train is on tracks."},
        {"word": "plane", "translation": "самолёт", "transcription": "[pleɪn]", "emoji": "✈️", "example": "Plane flies in sky."},
        {"word": "ship", "translation": "корабль", "transcription": "[ʃɪp]", "emoji": "🚢", "example": "Ship sails on sea."},
        {"word": "bike", "translation": "велосипед", "transcription": "[baɪk]", "emoji": "🚲", "example": "I ride a bike."},
        {"word": "motorcycle", "translation": "мотоцикл", "transcription": "[ˈməʊtəsaɪkl]", "emoji": "🏍️", "example": "Motorcycle is fast."},
        {"word": "taxi", "translation": "такси", "transcription": "[ˈtæksi]", "emoji": "🚕", "example": "Taxi takes you places."},
        {"word": "subway", "translation": "метро", "transcription": "[ˈsʌbweɪ]", "emoji": "🚇", "example": "Subway is underground."},
        {"word": "boat", "translation": "лодка", "transcription": "[bəʊt]", "emoji": "🚤", "example": "Boat on the water."},
    ],
    "home": [  # Дом
        {"word": "house", "translation": "дом", "transcription": "[haʊs]", "emoji": "🏠", "example": "This is my house."},
        {"word": "door", "translation": "дверь", "transcription": "[dɔːr]", "emoji": "🚪", "example": "Open the door."},
        {"word": "window", "translation": "окно", "transcription": "[ˈwɪndəʊ]", "emoji": "🪟", "example": "Window lets light in."},
        {"word": "room", "translation": "комната", "transcription": "[ruːm]", "emoji": "🛏️", "example": "My room is cozy."},
        {"word": "kitchen", "translation": "кухня", "transcription": "[ˈkɪtʃɪn]", "emoji": "🍳", "example": "Kitchen is for cooking."},
        {"word": "bed", "translation": "кровать", "transcription": "[bed]", "emoji": "🛏️", "example": "I sleep in bed."},
        {"word": "table", "translation": "стол", "transcription": "[ˈteɪbl]", "emoji": "🪑", "example": "Table for eating."},
        {"word": "chair", "translation": "стул", "transcription": "[tʃeər]", "emoji": "🪑", "example": "Chair to sit on."},
        {"word": "bathroom", "translation": "ванная", "transcription": "[ˈbɑːθruːm]", "emoji": "🚿", "example": "Bathroom has shower."},
        {"word": "living room", "translation": "гостиная", "transcription": "[ˈlɪvɪŋ ruːm]", "emoji": "🛋️", "example": "Living room for relaxing."},
    ],
    "nature": [  # Природа
        {"word": "tree", "translation": "дерево", "transcription": "[triː]", "emoji": "🌳", "example": "Tree has leaves."},
        {"word": "flower", "translation": "цветок", "transcription": "[ˈflaʊər]", "emoji": "🌸", "example": "Flower smells sweet."},
        {"word": "grass", "translation": "трава", "transcription": "[ɡrɑːs]", "emoji": "🌱", "example": "Grass is green."},
        {"word": "mountain", "translation": "гора", "transcription": "[ˈmaʊntɪn]", "emoji": "🏔️", "example": "Mountain is very high."},
        {"word": "river", "translation": "река", "transcription": "[ˈrɪvər]", "emoji": "🌊", "example": "River flows to sea."},
        {"word": "lake", "translation": "озеро", "transcription": "[leɪk]", "emoji": "🏞️", "example": "Lake has fresh water."},
        {"word": "forest", "translation": "лес", "transcription": "[ˈfɒrɪst]", "emoji": "🌲", "example": "Forest has many trees."},
        {"word": "beach", "translation": "пляж", "transcription": "[biːtʃ]", "emoji": "🏖️", "example": "Beach has sand."},
        {"word": "ocean", "translation": "океан", "transcription": "[ˈəʊʃn]", "emoji": "🌊", "example": "Ocean is very big."},
        {"word": "sky", "translation": "небо", "transcription": "[skaɪ]", "emoji": "🌌", "example": "Sky is blue."},
    ],
    "actions": [  # Действия
        {"word": "run", "translation": "бегать", "transcription": "[rʌn]", "emoji": "🏃", "example": "I run fast."},
        {"word": "walk", "translation": "идти", "transcription": "[wɔːk]", "emoji": "🚶", "example": "I walk to school."},
        {"word": "eat", "translation": "есть", "transcription": "[iːt]", "emoji": "🍽️", "example": "I eat breakfast."},
        {"word": "sleep", "translation": "спать", "transcription": "[sliːp]", "emoji": "😴", "example": "I sleep at night."},
        {"word": "read", "translation": "читать", "transcription": "[riːd]", "emoji": "📖", "example": "I read a book."},
        {"word": "write", "translation": "писать", "transcription": "[raɪt]", "emoji": "✍️", "example": "I write a letter."},
        {"word": "speak", "translation": "говорить", "transcription": "[spiːk]", "emoji": "🗣️", "example": "I speak English."},
        {"word": "listen", "translation": "слушать", "transcription": "[ˈlɪsn]", "emoji": "👂", "example": "I listen to music."},
        {"word": "see", "translation": "видеть", "transcription": "[siː]", "emoji": "👁️", "example": "I see a bird."},
        {"word": "love", "translation": "любить", "transcription": "[lʌv]", "emoji": "❤️", "example": "I love my family."},
    ],
    "emotions": [  # Эмоции
        {"word": "happy", "translation": "счастливый", "transcription": "[ˈhæpi]", "emoji": "😊", "example": "I am happy today."},
        {"word": "sad", "translation": "грустный", "transcription": "[sæd]", "emoji": "😢", "example": "I feel sad."},
        {"word": "angry", "translation": "злой", "transcription": "[ˈæŋɡri]", "emoji": "😠", "example": "I am angry!"},
        {"word": "tired", "translation": "усталый", "transcription": "[ˈtaɪərd]", "emoji": "😴", "example": "I am tired."},
        {"word": "excited", "translation": "взволнованный", "transcription": "[ɪkˈsaɪtɪd]", "emoji": "🤩", "example": "I am excited!"},
        {"word": "scared", "translation": "испуганный", "transcription": "[skeərd]", "emoji": "😨", "example": "I am scared of dark."},
        {"word": "surprised", "translation": "удивлённый", "transcription": "[səˈpraɪzd]", "emoji": "😲", "example": "I am surprised!"},
        {"word": "proud", "translation": "гордый", "transcription": "[praʊd]", "emoji": "🏆", "example": "I am proud of you."},
        {"word": "bored", "translation": "скучный", "transcription": "[bɔːrd]", "emoji": "😑", "example": "I am bored."},
        {"word": "calm", "translation": "спокойный", "transcription": "[kɑːm]", "emoji": "😌", "example": "I feel calm."},
    ],
    
    # ============ НОВЫЕ КАТЕГОРИИ ============
    
    "adjectives": [  # Прилагательные
        {"word": "big", "translation": "большой", "transcription": "[bɪɡ]", "emoji": "🐘", "example": "The elephant is big."},
        {"word": "small", "translation": "маленький", "transcription": "[smɔːl]", "emoji": "🐁", "example": "The mouse is small."},
        {"word": "fast", "translation": "быстрый", "transcription": "[fɑːst]", "emoji": "⚡", "example": "The cheetah is fast."},
        {"word": "slow", "translation": "медленный", "transcription": "[sləʊ]", "emoji": "🐢", "example": "The turtle is slow."},
        {"word": "hot", "translation": "горячий", "transcription": "[hɒt]", "emoji": "🔥", "example": "The coffee is hot."},
        {"word": "cold", "translation": "холодный", "transcription": "[kəʊld]", "emoji": "🧊", "example": "Ice is cold."},
        {"word": "good", "translation": "хороший", "transcription": "[ɡʊd]", "emoji": "👍", "example": "This is a good book."},
        {"word": "bad", "translation": "плохой", "transcription": "[bæd]", "emoji": "👎", "example": "This is a bad apple."},
        {"word": "new", "translation": "новый", "transcription": "[njuː]", "emoji": "🆕", "example": "I have a new bike."},
        {"word": "old", "translation": "старый", "transcription": "[əʊld]", "emoji": "📚", "example": "This is an old house."},
    ],
    
    "places": [  # Места
        {"word": "school", "translation": "школа", "transcription": "[skuːl]", "emoji": "🏫", "example": "I go to school."},
        {"word": "park", "translation": "парк", "transcription": "[pɑːrk]", "emoji": "🌳", "example": "We play in the park."},
        {"word": "store", "translation": "магазин", "transcription": "[stɔːr]", "emoji": "🏪", "example": "Mom goes to the store."},
        {"word": "hospital", "translation": "больница", "transcription": "[ˈhɒspɪtl]", "emoji": "🏥", "example": "Doctor works at hospital."},
        {"word": "library", "translation": "библиотека", "transcription": "[ˈlaɪbrəri]", "emoji": "📚", "example": "I read books in library."},
        {"word": "restaurant", "translation": "ресторан", "transcription": "[ˈrestrɒnt]", "emoji": "🍽️", "example": "We eat at restaurant."},
        {"word": "cinema", "translation": "кино", "transcription": "[ˈsɪnəmə]", "emoji": "🎬", "example": "We watch films at cinema."},
        {"word": "zoo", "translation": "зоопарк", "transcription": "[zuː]", "emoji": "🦁", "example": "Lions live in zoo."},
        {"word": "beach", "translation": "пляж", "transcription": "[biːtʃ]", "emoji": "🏖️", "example": "We swim at the beach."},
        {"word": "farm", "translation": "ферма", "transcription": "[fɑːrm]", "emoji": "🚜", "example": "Cows live on a farm."},
    ],
    
    "days": [  # Дни недели
        {"word": "Monday", "translation": "понедельник", "transcription": "[ˈmʌndeɪ]", "emoji": "📅", "example": "Monday is the first day."},
        {"word": "Tuesday", "translation": "вторник", "transcription": "[ˈtjuːzdeɪ]", "emoji": "📅", "example": "Tuesday is the second day."},
        {"word": "Wednesday", "translation": "среда", "transcription": "[ˈwenzdeɪ]", "emoji": "📅", "example": "Wednesday is in the middle."},
        {"word": "Thursday", "translation": "четверг", "transcription": "[ˈθɜːrzdeɪ]", "emoji": "📅", "example": "Thursday is almost Friday."},
        {"word": "Friday", "translation": "пятница", "transcription": "[ˈfraɪdeɪ]", "emoji": "🎉", "example": "Friday is fun day!"},
        {"word": "Saturday", "translation": "суббота", "transcription": "[ˈsætərdeɪ]", "emoji": "🎮", "example": "Saturday is weekend!"},
        {"word": "Sunday", "translation": "воскресенье", "transcription": "[ˈsʌndeɪ]", "emoji": "🌟", "example": "Sunday is rest day."},
        {"word": "today", "translation": "сегодня", "transcription": "[təˈdeɪ]", "emoji": "📆", "example": "Today is Monday."},
        {"word": "tomorrow", "translation": "завтра", "transcription": "[təˈmɒrəʊ]", "emoji": "📌", "example": "Tomorrow is Tuesday."},
        {"word": "yesterday", "translation": "вчера", "transcription": "[ˈjestədeɪ]", "emoji": "📆", "example": "Yesterday was Sunday."},
    ],
    
    "months": [  # Месяцы
        {"word": "January", "translation": "январь", "transcription": "[ˈdʒænjuəri]", "emoji": "❄️", "example": "January is the first month."},
        {"word": "February", "translation": "февраль", "transcription": "[ˈfebruəri]", "emoji": "❄️", "example": "February is cold."},
        {"word": "March", "translation": "март", "transcription": "[mɑːrtʃ]", "emoji": "🌸", "example": "March is spring month."},
        {"word": "April", "translation": "апрель", "transcription": "[ˈeɪprəl]", "emoji": "🌷", "example": "April showers bring May flowers."},
        {"word": "May", "translation": "май", "transcription": "[meɪ]", "emoji": "🌸", "example": "May is a warm month."},
        {"word": "June", "translation": "июнь", "transcription": "[dʒuːn]", "emoji": "☀️", "example": "June starts summer."},
        {"word": "July", "translation": "июль", "transcription": "[dʒuˈlaɪ]", "emoji": "🔥", "example": "July is the hottest month."},
        {"word": "August", "translation": "август", "transcription": "[ˈɔːɡəst]", "emoji": "🌻", "example": "August is summer too."},
        {"word": "September", "translation": "сентябрь", "transcription": "[sepˈtembər]", "emoji": "🍎", "example": "School starts in September."},
        {"word": "October", "translation": "октябрь", "transcription": "[ɒkˈtəʊbər]", "emoji": "🎃", "example": "October has Halloween."},
    ],
    
    "fruit": [  # Фрукты
        {"word": "apple", "translation": "яблоко", "transcription": "[ˈæpl]", "emoji": "🍎", "example": "An apple a day keeps doctor away."},
        {"word": "banana", "translation": "банан", "transcription": "[bəˈnɑːnə]", "emoji": "🍌", "example": "Monkeys eat bananas."},
        {"word": "orange", "translation": "апельсин", "transcription": "[ˈɒrɪndʒ]", "emoji": "🍊", "example": "Oranges are juicy."},
        {"word": "grape", "translation": "виноград", "transcription": "[ɡreɪp]", "emoji": "🍇", "example": "Grapes grow in bunches."},
        {"word": "strawberry", "translation": "клубника", "transcription": "[ˈstrɔːbəri]", "emoji": "🍓", "example": "Strawberries are red and sweet."},
        {"word": "watermelon", "translation": "арбуз", "transcription": "[ˈwɔːtəmelən]", "emoji": "🍉", "example": "Watermelon is big and juicy."},
        {"word": "lemon", "translation": "лимон", "transcription": "[ˈlemən]", "emoji": "🍋", "example": "Lemons are sour."},
        {"word": "mango", "translation": "манго", "transcription": "[ˈmæŋɡəʊ]", "emoji": "🥭", "example": "Mangoes are tropical fruit."},
        {"word": "peach", "translation": "персик", "transcription": "[piːtʃ]", "emoji": "🍑", "example": "Peaches are fuzzy."},
        {"word": "cherry", "translation": "вишня", "transcription": "[ˈtʃeri]", "emoji": "🍒", "example": "Cherries are small and red."},
    ],
    
    "vegetables": [  # Овощи
        {"word": "carrot", "translation": "морковь", "transcription": "[ˈkærət]", "emoji": "🥕", "example": "Rabbits eat carrots."},
        {"word": "potato", "translation": "картофель", "transcription": "[pəˈteɪtəʊ]", "emoji": "🥔", "example": "Potatoes grow underground."},
        {"word": "tomato", "translation": "помидор", "transcription": "[təˈmɑːtəʊ]", "emoji": "🍅", "example": "Tomatoes are red."},
        {"word": "cucumber", "translation": "огурец", "transcription": "[ˈkjuːkʌmbər]", "emoji": "🥒", "example": "Cucumbers are long and green."},
        {"word": "onion", "translation": "лук", "transcription": "[ˈʌnjən]", "emoji": "🧅", "example": "Onions make us cry."},
        {"word": "garlic", "translation": "чеснок", "transcription": "[ˈɡɑːrlɪk]", "emoji": "🧄", "example": "Garlic is strong."},
        {"word": "pepper", "translation": "перец", "transcription": "[ˈpepər]", "emoji": "🫑", "example": "Peppers can be hot."},
        {"word": "cabbage", "translation": "капуста", "transcription": "[ˈkæbɪdʒ]", "emoji": "🥬", "example": "Cabbage makes good salad."},
        {"word": "corn", "translation": "кукуруза", "transcription": "[kɔːrn]", "emoji": "🌽", "example": "Corn is yellow."},
        {"word": "broccoli", "translation": "брокколи", "transcription": "[ˈbrɒkəli]", "emoji": "🥦", "example": "Broccoli is green vegetable."},
    ],
    
    "drinks": [  # Напитки
        {"word": "juice", "translation": "сок", "transcription": "[dʒuːs]", "emoji": "🧃", "example": "I drink orange juice."},
        {"word": "tea", "translation": "чай", "transcription": "[tiː]", "emoji": "🍵", "example": "Grandma drinks tea."},
        {"word": "coffee", "translation": "кофе", "transcription": "[ˈkɒfi]", "emoji": "☕", "example": "Dad drinks coffee."},
        {"word": "water", "translation": "вода", "transcription": "[ˈwɔːtər]", "emoji": "💧", "example": "Water is essential for life."},
        {"word": "milk", "translation": "молоко", "transcription": "[mɪlk]", "emoji": "🥛", "example": "Kids drink milk."},
        {"word": "soda", "translation": "газировка", "transcription": "[ˈsəʊdə]", "emoji": "🥤", "example": "Soda is sweet."},
        {"word": "smoothie", "translation": "смузи", "transcription": "[ˈsmuːði]", "emoji": "🥤", "example": "Smoothie is fruit drink."},
        {"word": "lemonade", "translation": "лимонад", "transcription": "[ˌleməˈneɪd]", "emoji": "🍋", "example": "Lemonade is refreshing."},
        {"word": "shake", "translation": "молочный коктейль", "transcription": "[ʃeɪk]", "emoji": "🥤", "example": "Chocolate shake is delicious."},
        {"word": "cocktail", "translation": "коктейль", "transcription": "[ˈkɒkteɪl]", "emoji": "🍹", "example": "Fruit cocktail is sweet."},
    ],
    
    "jobs": [  # Профессии
        {"word": "doctor", "translation": "врач", "transcription": "[ˈdɒktər]", "emoji": "👨‍⚕️", "example": "Doctor helps sick people."},
        {"word": "teacher", "translation": "учитель", "transcription": "[ˈtiːtʃər]", "emoji": "👨‍🏫", "example": "Teacher teaches children."},
        {"word": "farmer", "translation": "фермер", "transcription": "[ˈfɑːrmər]", "emoji": "👨‍🌾", "example": "Farmer grows food."},
        {"word": "firefighter", "translation": "пожарный", "transcription": "[ˈfaɪərfaɪtər]", "emoji": "👨‍🚒", "example": "Firefighter puts out fires."},
        {"word": "policeman", "translation": "полицейский", "transcription": "[pəˈliːsmæn]", "emoji": "👮", "example": "Policeman keeps us safe."},
        {"word": "chef", "translation": "шеф-повар", "transcription": "[ʃef]", "emoji": "👨‍🍳", "example": "Chef cooks food."},
        {"word": "pilot", "translation": "пилот", "transcription": "[ˈpaɪlət]", "emoji": "👨‍✈️", "example": "Pilot flies planes."},
        {"word": "nurse", "translation": "медсестра", "transcription": "[nɜːrs]", "emoji": "👩‍⚕️", "example": "Nurse helps doctors."},
        {"word": "scientist", "translation": "учёный", "transcription": "[ˈsaɪəntɪst]", "emoji": "🔬", "example": "Scientist does experiments."},
        {"word": "artist", "translation": "художник", "transcription": "[ˈɑːrtɪst]", "emoji": "🎨", "example": "Artist paints pictures."},
    ],
    
    "sports": [  # Виды спорта
        {"word": "football", "translation": "футбол", "transcription": "[ˈfʊtbɔːl]", "emoji": "⚽", "example": "Football is popular game."},
        {"word": "basketball", "translation": "баскетбол", "transcription": "[ˈbæskɪtbɔːl]", "emoji": "🏀", "example": "Basketball uses a hoop."},
        {"word": "tennis", "translation": "теннис", "transcription": "[ˈtenɪs]", "emoji": "🎾", "example": "Tennis uses a racket."},
        {"word": "swimming", "translation": "плавание", "transcription": "[ˈswɪmɪŋ]", "emoji": "🏊", "example": "Swimming is good exercise."},
        {"word": "running", "translation": "бег", "transcription": "[ˈrʌnɪŋ]", "emoji": "🏃", "example": "Running makes us fit."},
        {"word": "gymnastics", "translation": "гимнастика", "transcription": "[dʒɪmˈnæstɪks]", "emoji": "🤸", "example": "Gymnastics is artistic."},
        {"word": "boxing", "translation": "бокс", "transcription": "[ˈbɒksɪŋ]", "emoji": "🥊", "example": "Boxing uses gloves."},
        {"word": "skiing", "translation": "лыжи", "transcription": "[ˈskiːɪŋ]", "emoji": "⛷️", "example": "Skiing is winter sport."},
        {"word": "cycling", "translation": "велоспорт", "transcription": "[ˈsaɪklɪŋ]", "emoji": "🚴", "example": "Cycling is fun."},
        {"word": "hockey", "translation": "хоккей", "transcription": "[ˈhɒki]", "emoji": "🏒", "example": "Hockey uses a stick."},
    ],
    
    "hobbies": [  # Хобби
        {"word": "reading", "translation": "чтение", "transcription": "[ˈriːdɪŋ]", "emoji": "📖", "example": "Reading is fun."},
        {"word": "swimming", "translation": "плавание", "transcription": "[ˈswɪmɪŋ]", "emoji": "🏊", "example": "Swimming is my hobby."},
        {"word": "dancing", "translation": "танцы", "transcription": "[ˈdɑːnsɪŋ]", "emoji": "💃", "example": "Dancing is artistic."},
        {"word": "singing", "translation": "пение", "transcription": "[ˈsɪŋɪŋ]", "emoji": "🎤", "example": "Singing makes me happy."},
        {"word": "drawing", "translation": "рисование", "transcription": "[ˈdrɔːɪŋ]", "emoji": "🎨", "example": "Drawing is creative."},
        {"word": "fishing", "translation": "рыбалка", "transcription": "[ˈfɪʃɪŋ]", "emoji": "🎣", "example": "Fishing needs patience."},
        {"word": "gaming", "translation": "игры", "transcription": "[ˈɡeɪmɪŋ]", "emoji": "🎮", "example": "Gaming is exciting."},
        {"word": "cooking", "translation": "готовка", "transcription": "[ˈkʊkɪŋ]", "emoji": "👨‍🍳", "example": "Cooking is useful skill."},
        {"word": "gardening", "translation": "садоводство", "transcription": "[ˈɡɑːrdnɪŋ]", "emoji": "🌱", "example": "Gardening grows plants."},
        {"word": "photography", "translation": "фотография", "transcription": "[fəˈtɒɡrəfi]", "emoji": "📷", "example": "Photography captures moments."},
    ],
    
    "rooms": [  # Комнаты
        {"word": "bedroom", "translation": "спальня", "transcription": "[ˈbedruːm]", "emoji": "🛏️", "example": "I sleep in my bedroom."},
        {"word": "bathroom", "translation": "ванная", "transcription": "[ˈbɑːθruːm]", "emoji": "🚿", "example": "Bathroom has a shower."},
        {"word": "kitchen", "translation": "кухня", "transcription": "[ˈkɪtʃɪn]", "emoji": "🍳", "example": "Mom cooks in kitchen."},
        {"word": "living room", "translation": "гостиная", "transcription": "[ˈlɪvɪŋ ruːm]", "emoji": "🛋️", "example": "Family watches TV in living room."},
        {"word": "dining room", "translation": "столовая", "transcription": "[ˈdaɪnɪŋ ruːm]", "emoji": "🍽️", "example": "We eat in dining room."},
        {"word": "office", "translation": "кабинет", "transcription": "[ˈɒfɪs]", "emoji": "💼", "example": "Dad works in office."},
        {"word": "garage", "translation": "гараж", "transcription": "[ˈɡærɑːʒ]", "emoji": "🚗", "example": "Car is in garage."},
        {"word": "basement", "translation": "подвал", "transcription": "[ˈbeɪsmənt]", "emoji": "🏚️", "example": "Basement is underground."},
        {"word": "attic", "translation": "чердак", "transcription": "[ˈætɪk]", "emoji": "🏠", "example": "Attic is under the roof."},
        {"word": "balcony", "translation": "балкон", "transcription": "[ˈbælkəni]", "emoji": "🏡", "example": "Balcony has a view."},
    ],
    
    "furniture": [  # Мебель
        {"word": "chair", "translation": "стул", "transcription": "[tʃeər]", "emoji": "🪑", "example": "I sit on a chair."},
        {"word": "table", "translation": "стол", "transcription": "[ˈteɪbl]", "emoji": "🪑", "example": "We eat at the table."},
        {"word": "sofa", "translation": "диван", "transcription": "[ˈsəʊfə]", "emoji": "🛋️", "example": "Sofa is comfortable."},
        {"word": "bed", "translation": "кровать", "transcription": "[bed]", "emoji": "🛏️", "example": "I sleep in my bed."},
        {"word": "wardrobe", "translation": "шкаф", "transcription": "[ˈwɔːrdrəʊb]", "emoji": "🚪", "example": "Clothes are in wardrobe."},
        {"word": "desk", "translation": "письменный стол", "transcription": "[desk]", "emoji": "🪑", "example": "I study at desk."},
        {"word": "bookshelf", "translation": "книжная полка", "transcription": "[ˈbʊkʃelf]", "emoji": "📚", "example": "Books are on bookshelf."},
        {"word": "mirror", "translation": "зеркало", "transcription": "[ˈmɪrər]", "emoji": "🪞", "example": "Mirror reflects our image."},
        {"word": "lamp", "translation": "лампа", "transcription": "[læmp]", "emoji": "💡", "example": "Lamp gives light."},
        {"word": "shelf", "translation": "полка", "transcription": "[ʃelf]", "emoji": "📌", "example": "Shelf holds things."},
    ],
    
    "electronics": [  # Электроника
        {"word": "phone", "translation": "телефон", "transcription": "[fəʊn]", "emoji": "📱", "example": "I call on phone."},
        {"word": "computer", "translation": "компьютер", "transcription": "[kəmˈpjuːtər]", "emoji": "💻", "example": "Computer helps us work."},
        {"word": "tablet", "translation": "планшет", "transcription": "[ˈtæblət]", "emoji": "📱", "example": "Tablet is portable computer."},
        {"word": "television", "translation": "телевизор", "transcription": "[ˈtelɪvɪʒn]", "emoji": "📺", "example": "We watch TV on television."},
        {"word": "radio", "translation": "радио", "transcription": "[ˈreɪdiəʊ]", "emoji": "📻", "example": "Radio plays music."},
        {"word": "camera", "translation": "камера", "transcription": "[ˈkæmərə]", "emoji": "📷", "example": "Camera takes photos."},
        {"word": "headphones", "translation": "наушники", "transcription": "[ˈhedfəʊnz]", "emoji": "🎧", "example": "Headphones let me hear music."},
        {"word": "keyboard", "translation": "клавиатура", "transcription": "[ˈkiːbɔːrd]", "emoji": "⌨️", "example": "Keyboard has letters."},
        {"word": "mouse", "translation": "мышь", "transcription": "[maʊs]", "emoji": "🖱️", "example": "Mouse moves the cursor."},
        {"word": "printer", "translation": "принтер", "transcription": "[ˈprɪntər]", "emoji": "🖨️", "example": "Printer makes copies."},
    ],
    
    "sea_animals": [  # Морские животные
        {"word": "whale", "translation": "кит", "transcription": "[weɪl]", "emoji": "🐋", "example": "Whale is the biggest animal."},
        {"word": "shark", "translation": "акула", "transcription": "[ʃɑːrk]", "emoji": "🦈", "example": "Shark has many teeth."},
        {"word": "dolphin", "translation": "дельфин", "transcription": "[ˈdɒlfɪn]", "emoji": "🐬", "example": "Dolphin is friendly."},
        {"word": "octopus", "translation": "осьминог", "transcription": "[ˈɒktəpəs]", "emoji": "🐙", "example": "Octopus has eight arms."},
        {"word": "crab", "translation": "краб", "transcription": "[kræb]", "emoji": "🦀", "example": "Crab walks sideways."},
        {"word": "jellyfish", "translation": "медуза", "transcription": "[ˈdʒelifɪʃ]", "emoji": "🪼", "example": "Jellyfish floats in water."},
        {"word": "starfish", "translation": "морская звезда", "transcription": "[ˈstɑːrfɪʃ]", "emoji": "⭐", "example": "Starfish has five arms."},
        {"word": "seahorse", "translation": "морской конёк", "transcription": "[ˈsiːhɔːrs]", "emoji": "🐴", "example": "Seahorse looks like horse."},
        {"word": "squid", "translation": "кальмар", "transcription": "[skwɪd]", "emoji": "🦑", "example": "Squid has long tentacles."},
        {"word": "seal", "translation": "тюлень", "transcription": "[siːl]", "emoji": "🦭", "example": "Seal lives in water."},
    ],
}

def seed_database():
    """Заполнение БД"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Proverka est' li uze slova
    cursor.execute("SELECT COUNT(*) FROM lessons")
    lessons_count = cursor.fetchone()[0]
    
    if lessons_count > 0:
        print(f"[!] DB already has {lessons_count} lessons! Clearing old content...")
        
        # Ochishchaem starye dannye (avtomaticheski)
        cursor.execute("DELETE FROM user_progress")
        cursor.execute("DELETE FROM user_achievements")
        cursor.execute("DELETE FROM daily_quests")
        cursor.execute("DELETE FROM lessons")
        cursor.execute("DROP TABLE IF EXISTS words")
        cursor.execute("DELETE FROM achievements")
        conn.commit()
        print("[+] Old data deleted")
    
    print("[*] Filling DB with PlusTim content...")
    print(f"[*] Total categories: {len(WORDS_DATA)}")
    print(f"[*] Words per category: 10")
    print()
    
    # Создаём таблицу слов если нет
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT NOT NULL,
            translation TEXT NOT NULL,
            transcription TEXT,
            emoji TEXT,
            category TEXT NOT NULL,
            example TEXT
        )
    """)
    
    # Вставляем слова и создаём уроки
    lesson_counter = 0
    for category, words in WORDS_DATA.items():
        for i, w in enumerate(words):
            # Вставляем слово
            cursor.execute("""
                INSERT INTO words (word, translation, transcription, emoji, category, example)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (w['word'], w['translation'], w['transcription'], w['emoji'], category, w['example']))
            word_id = cursor.lastrowid
            
            # Создаём урок для слова
            questions_json = create_questions_for_word(w, category)
            
            cursor.execute("""
                INSERT INTO lessons (title, description, category, difficulty, xp_reward, questions_json, order_num)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                f"Изучаем: {w['word']}",
                f"Учим слово {w['word']} - {w['translation']}",
                category,
                min(3, i // 3 + 1),  # Сложность 1-3
                10 + min(i * 2, 20),  # XP 10-30
                json.dumps(questions_json, ensure_ascii=False),
                lesson_counter
            ))
            lesson_counter += 1
    
    # Достижения (имя, описание, иконка, XP, тип условия, значение условия)
    achievements = [
        ("First Step", "Complete first lesson", "🌟", 50, "lessons_completed", 1),
        ("Beginner", "Learn 10 words", "📚", 100, "words_learned", 10),
        ("Vocabulary", "Learn 50 words", "📖", 250, "words_learned", 50),
        ("Encyclopedia", "Learn 100 words", "🧠", 500, "words_learned", 100),
        ("Genius", "Learn 150 words", "👑", 1000, "words_learned", 150),
        ("Three Days", "Three days in a row", "🔥", 75, "streak_days", 3),
        ("Week Success", "Seven days in a row", "🏆", 200, "streak_days", 7),
        ("Month Wins", "Thirty days in a row", "🥇", 500, "streak_days", 30),
        ("Perfect", "10 correct answers in a row", "💯", 150, "perfect_answers", 10),
        ("Explorer", "Complete all categories", "🌍", 300, "categories_completed", 15),
        ("Zoologist", "All words: Animals", "🐱", 100, "category_words", 10),
        ("Cook", "All words: Food", "🍎", 100, "category_words", 10),
        ("Artist", "All words: Colors", "🎨", 100, "category_words", 10),
        ("Mathematician", "All words: Numbers", "🔢", 100, "category_words", 10),
    ]
    
    for name, desc, icon, xp, cond_type, cond_value in achievements:
        cursor.execute("""
            INSERT INTO achievements (name, description, icon, xp_reward, condition_type, condition_value)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, desc, icon, xp, cond_type, cond_value))
    
    conn.commit()
    
    # Статистика
    cursor.execute("SELECT COUNT(*) FROM words")
    word_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM lessons")
    lesson_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM achievements")
    achievement_count = cursor.fetchone()[0]
    
    print("[+] Content added:")
    print(f"    [*] Words: {word_count}")
    print(f"    [*] Lessons: {lesson_count}")
    print(f"    [*] Achievements: {achievement_count}")
    print()
    print("[*] Categories:")
    for cat in WORDS_DATA.keys():
        print(f"    - {cat.capitalize()}")
    
    conn.close()

def create_questions_for_word(target_word, category):
    """Создание вопросов для слова (10 типов вопросов)"""
    questions = []
    category_words = WORDS_DATA.get(category, [])
    wrong_words = [w['word'] for w in category_words if w['word'] != target_word['word']]
    
    # ============ ТИП 1: translation ============
    wrong_translations = random.sample(
        [w['translation'] for w in category_words if w['translation'] != target_word['translation']],
        min(3, len(category_words) - 1)
    )
    options = wrong_translations.copy()
    correct_idx = random.randint(0, 3)
    options.insert(correct_idx, target_word['translation'])
    
    questions.append({
        "type": "translation",
        "question": f"Как переводится \"{target_word['word']}\" {target_word['transcription']}?",
        "options": options,
        "correct_answer": correct_idx,
        "word": target_word['word'],
        "emoji": target_word['emoji']
    })
    
    # ============ ТИП 2: word_choice ============
    options = random.sample(wrong_words, min(3, len(wrong_words)))
    correct_idx = random.randint(0, 3)
    options.insert(correct_idx, target_word['word'])
    
    questions.append({
        "type": "word_choice",
        "question": f"Какое слово подходит к картинке {target_word['emoji']}?",
        "options": options,
        "correct_answer": correct_idx,
        "translation": target_word['translation']
    })
    
    # ============ ТИП 3: transcription ============
    options = random.sample(wrong_words, min(3, len(wrong_words)))
    correct_idx = random.randint(0, 3)
    options.insert(correct_idx, target_word['word'])
    
    questions.append({
        "type": "transcription",
        "question": f"Какое слово произносится как \"{target_word['transcription']}\"?",
        "options": options,
        "correct_answer": correct_idx,
        "emoji": target_word['emoji']
    })
    
    # ============ ТИП 4: missing_letter ============
    if len(target_word['word']) > 2:
        missing_idx = random.randint(0, len(target_word['word']) - 1)
        missing_letter = target_word['word'][missing_idx]
        word_display = target_word['word'][:missing_idx] + "_" + target_word['word'][missing_idx + 1:]
        
        letter_pool = list(set([c for c in 'aeiou'] + [c for c in 'bcdfghjklmnpqrstvwxyz']))
        wrong_letters = [c for c in letter_pool if c != missing_letter]
        wrong_letters = random.sample(wrong_letters, 3)
        options = wrong_letters.copy()
        correct_answer = random.randint(0, 3)
        options.insert(correct_answer, missing_letter)
        
        questions.append({
            "type": "missing_letter",
            "question": f"Какой буквы не хватает: {word_display}?",
            "options": options,
            "correct_answer": correct_answer,
            "emoji": target_word['emoji']
        })
    
    # ============ ТИП 5: example ============
    options = random.sample(wrong_words, min(3, len(wrong_words)))
    correct_idx = random.randint(0, 3)
    options.insert(correct_idx, target_word['word'])
    
    questions.append({
        "type": "example",
        "question": f"Какое слово пропущено: \"{target_word['example']}\"?",
        "options": options,
        "correct_answer": correct_idx,
        "transcription": target_word['transcription']
    })
    
    # ============ ТИП 6: listening_choice (НОВЫЙ) ============
    # Слушаем аудио и выбираем правильное слово
    options = random.sample(wrong_words, min(3, len(wrong_words)))
    correct_idx = random.randint(0, 3)
    options.insert(correct_idx, target_word['word'])
    
    questions.append({
        "type": "listening_choice",
        "question": f"🔊 Что ты услышал? {target_word['translation']}",
        "options": options,
        "correct_answer": correct_idx,
        "emoji": target_word['emoji'],
        "audio_url": f"/api/tts/{target_word['word']}"
    })
    
    # ============ ТИП 7: matching (НОВЫЙ) ============
    # Сопоставление: слово - перевод (target ВСЕГДА включен)
    other_words = random.sample([w for w in category_words if w['word'] != target_word['word']], min(3, len(category_words) - 1))
    selected_words = other_words + [target_word]
    random.shuffle(selected_words)
    shuffled_translations = [w['translation'] for w in selected_words]
    
    questions.append({
        "type": "matching",
        "question": f"Сопоставь: {target_word['emoji']} - это что?",
        "options": shuffled_translations,
        "correct_answer": shuffled_translations.index(target_word['translation']),
        "word": target_word['word']
    })
    
    # ============ ТИП 8: listening (НОВЫЙ) ============
    # Аудио-диктант: напиши слово
    questions.append({
        "type": "listening",
        "question": f"🔊 Напиши слово, которое ты услышал: {target_word['translation']}",
        "options": [],  # Для ввода текста
        "correct_answer": -1,  # special: text input
        "word": target_word['word'],
        "emoji": target_word['emoji'],
        "audio_url": f"/api/tts/{target_word['word']}"
    })
    
    # ============ ТИП 9: writing (НОВЫЙ) ============
    # Написание слова по переводу
    if len(target_word['word']) <= 8:  # Только короткие слова
        # Варианты с ошибками
        wrong_options = []
        for _ in range(3):
            wrong = list(target_word['word'])
            swap_idx = random.randint(0, len(wrong) - 2)
            wrong[swap_idx], wrong[swap_idx + 1] = wrong[swap_idx + 1], wrong[swap_idx]
            wrong_options.append(''.join(wrong))
        
        options = wrong_options.copy()
        correct_idx = random.randint(0, 3)
        options.insert(correct_idx, target_word['word'])
        
        questions.append({
            "type": "writing",
            "question": f"Напиши по-английски: \"{target_word['translation']}\"",
            "options": options,
            "correct_answer": correct_idx,
            "transcription": target_word['transcription']
        })
    
    # ============ ТИП 10: sentence (НОВЫЙ) ============
    # Составь предложение из слов (только если слово есть в предложении)
    sentence_words = target_word['example'].replace('.', '').split()
    
    # Проверяем есть ли слово в предложении (case-insensitive)
    word_in_sentence = target_word['word'].lower() in [w.lower() for w in sentence_words]
    
    if word_in_sentence:
        shuffled = list(sentence_words)
        random.shuffle(shuffled)
        
        questions.append({
            "type": "sentence",
            "question": f"Составь предложение: {target_word['emoji']}",
            "options": shuffled,
            "correct_answer": -1,  # special: ordering
            "word": target_word['word'],
            "correct_order": sentence_words
        })
    
    return questions

if __name__ == "__main__":
    random.seed(42)
    seed_database()