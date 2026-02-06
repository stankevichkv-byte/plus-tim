"""
Заполнение базы данных тестовыми уроками
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "plustim.db")

LESSONS = [
    {
        "title": "Животные",
        "description": "Учим названия животных на английском",
        "category": "animals",
        "difficulty": 1,
        "xp_reward": 15,
        "order_num": 1,
        "questions": [
            {
                "id": 1,
                "question": "Как будет 'собака' на английском?",
                "options": ["Cat", "Dog", "Bird", "Fish"],
                "correct_answer": 1
            },
            {
                "id": 2,
                "question": "Как будет 'кошка' на английском?",
                "options": ["Dog", "Cat", "Mouse", "Horse"],
                "correct_answer": 1
            },
            {
                "id": 3,
                "question": "Переведи: 'The cat is sleeping'",
                "options": ["Собака спит", "Кошка спит", "Птица летит", "Рыба плывет"],
                "correct_answer": 1
            },
            {
                "id": 4,
                "question": "Какое слово лишнее?",
                "options": ["Dog", "Cat", "Elephant", "Apple"],
                "correct_answer": 3
            },
            {
                "id": 5,
                "question": "Как будет 'слон' на английском?",
                "options": ["Lion", "Elephant", "Tiger", "Bear"],
                "correct_answer": 1
            }
        ]
    },
    {
        "title": "Цвета",
        "description": "Изучаем цвета на английском",
        "category": "colors",
        "difficulty": 1,
        "xp_reward": 15,
        "order_num": 2,
        "questions": [
            {
                "id": 1,
                "question": "Как будет 'красный' на английском?",
                "options": ["Blue", "Red", "Green", "Yellow"],
                "correct_answer": 1
            },
            {
                "id": 2,
                "question": "Как будет 'синий' на английском?",
                "options": ["Red", "Green", "Blue", "Black"],
                "correct_answer": 2
            },
            {
                "id": 3,
                "question": "Переведи: 'The sky is blue'",
                "options": ["Трава зеленая", "Небо синее", "Солнце желтое", "Море голубое"],
                "correct_answer": 1
            },
            {
                "id": 4,
                "question": "Какого цвета grass?",
                "options": ["Green", "Red", "Blue", "Brown"],
                "correct_answer": 0
            },
            {
                "id": 5,
                "question": "Как будет 'желтый' на английском?",
                "options": ["Yellow", "White", "Orange", "Purple"],
                "correct_answer": 0
            }
        ]
    },
    {
        "title": "Еда",
        "description": "Учим названия продуктов питания",
        "category": "food",
        "difficulty": 2,
        "xp_reward": 20,
        "order_num": 3,
        "questions": [
            {
                "id": 1,
                "question": "Как будет 'яблоко' на английском?",
                "options": ["Orange", "Apple", "Banana", "Grape"],
                "correct_answer": 1
            },
            {
                "id": 2,
                "question": "Как будет 'хлеб' на английском?",
                "options": ["Water", "Bread", "Milk", "Cheese"],
                "correct_answer": 1
            },
            {
                "id": 3,
                "question": "Переведи: 'I like pizza'",
                "options": ["Я люблю пиццу", "Я люблю пасту", "Я люблю суп", "Я люблю торт"],
                "correct_answer": 0
            },
            {
                "id": 4,
                "question": "Какое слово лишнее?",
                "options": ["Apple", "Banana", "Car", "Orange"],
                "correct_answer": 2
            },
            {
                "id": 5,
                "question": "Как будет 'молоко' на английском?",
                "options": ["Water", "Juice", "Milk", "Tea"],
                "correct_answer": 2
            }
        ]
    },
    {
        "title": "Семья",
        "description": "Учим названия членов семьи",
        "category": "family",
        "difficulty": 2,
        "xp_reward": 20,
        "order_num": 4,
        "questions": [
            {
                "id": 1,
                "question": "Как будет 'мама' на английском?",
                "options": ["Father", "Mother", "Sister", "Brother"],
                "correct_answer": 1
            },
            {
                "id": 2,
                "question": "Как будет 'папа' на английском?",
                "options": ["Dad", "Mom", "Uncle", "Aunt"],
                "correct_answer": 0
            },
            {
                "id": 3,
                "question": "Переведи: 'My sister is 10 years old'",
                "options": ["Моему брату 10 лет", "Моей сестре 10 лет", "Моему другу 10 лет", "Мне 10 лет"],
                "correct_answer": 1
            },
            {
                "id": 4,
                "question": "Кто такой 'grandmother'?",
                "options": ["Тетя", "Бабушка", "Двоюродная сестра", "Прабабушка"],
                "correct_answer": 1
            },
            {
                "id": 5,
                "question": "Как будет 'брат' на английском?",
                "options": ["Sister", "Brother", "Cousin", "Nephew"],
                "correct_answer": 1
            }
        ]
    },
    {
        "title": "Время",
        "description": "Учим называть время на английском",
        "category": "time",
        "difficulty": 3,
        "xp_reward": 25,
        "order_num": 5,
        "questions": [
            {
                "id": 1,
                "question": "Как будет 'час' на английском?",
                "options": ["Minute", "Second", "Hour", "Day"],
                "correct_answer": 2
            },
            {
                "id": 2,
                "question": "Как будет 'понедельник' на английском?",
                "options": ["Sunday", "Monday", "Tuesday", "Saturday"],
                "correct_answer": 1
            },
            {
                "id": 3,
                "question": "Переведи: 'What time is it?'",
                "options": ["Сколько лет?", "Который час?", "Какое число?", "Где ты?"],
                "correct_answer": 1
            },
            {
                "id": 4,
                "question": "Как будет 'сегодня' на английском?",
                "options": ["Tomorrow", "Yesterday", "Today", "Now"],
                "correct_answer": 2
            },
            {
                "id": 5,
                "question": "Как будет 'завтра' на английском?",
                "options": ["Yesterday", "Today", "Tomorrow", "Tonight"],
                "correct_answer": 2
            }
        ]
    }
]

def seed_lessons():
    """Заполнение уроков"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    for lesson in LESSONS:
        cursor.execute("""
            INSERT OR REPLACE INTO lessons 
            (title, description, category, difficulty, xp_reward, order_num, questions_json)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            lesson["title"],
            lesson["description"],
            lesson["category"],
            lesson["difficulty"],
            lesson["xp_reward"],
            lesson["order_num"],
            json.dumps(lesson["questions"], ensure_ascii=False)
        ))
    
    conn.commit()
    conn.close()
    print(f"Добавлено {len(LESSONS)} уроков!")

def seed_achievements():
    """Заполнение достижений"""
    achievements = [
        ("Первые шаги", "Пройди первый урок", "🎯", 50, "lessons_completed", 1),
        ("Любопытный", "Пройди 5 уроков", "📚", 100, "lessons_completed", 5),
        ("Знаток", "Пройди 10 уроков", "🏆", 200, "lessons_completed", 10),
        ("Неделю подряд", "Посети приложение 7 дней", "🔥", 150, "streak_days", 7),
        ("Месяц усердия", "Посети приложение 30 дней", "💪", 500, "streak_days", 30),
        ("Первый уровень", "Достигни 2 уровня", "⭐", 50, "level", 2),
        ("Продвинутый", "Достигни 5 уровня", "🌟", 150, "level", 5),
        ("Эксперт", "Достигни 10 уровня", "💎", 500, "level", 10),
    ]
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    for ach in achievements:
        cursor.execute("""
            INSERT OR REPLACE INTO achievements 
            (name, description, icon, xp_reward, condition_type, condition_value)
            VALUES (?, ?, ?, ?, ?, ?)
        """, ach)
    
    conn.commit()
    conn.close()
    print(f"Добавлено {len(achievements)} достижений!")

if __name__ == "__main__":
    seed_lessons()
    seed_achievements()