"""
PlusTim API - FastAPI backend для Telegram Web App
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List
import sqlite3
import os
from datetime import datetime, timedelta
import random
import uuid
from gtts import gTTS

app = FastAPI(title="PlusTim API", description="API для изучения английского языка")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database path
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "plustim.db")

def get_db():
    """Подключение к БД"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Инициализация БД"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tg_id INTEGER UNIQUE NOT NULL,
            username TEXT,
            first_name TEXT,
            level INTEGER DEFAULT 1,
            xp INTEGER DEFAULT 0,
            xp_to_next_level INTEGER DEFAULT 100,
            streak_days INTEGER DEFAULT 0,
            last_activity DATE,
            diamonds INTEGER DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS lessons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            category TEXT NOT NULL,
            difficulty INTEGER DEFAULT 1,
            xp_reward INTEGER DEFAULT 10,
            questions_json TEXT NOT NULL,
            order_num INTEGER DEFAULT 0
        );
        
        CREATE TABLE IF NOT EXISTS user_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            lesson_id INTEGER,
            completed INTEGER DEFAULT 0,
            correct_answers INTEGER DEFAULT 0,
            total_questions INTEGER DEFAULT 0,
            xp_earned INTEGER DEFAULT 0,
            completed_at DATETIME,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (lesson_id) REFERENCES lessons(id)
        );
        
        CREATE TABLE IF NOT EXISTS achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            icon TEXT,
            xp_reward INTEGER DEFAULT 50,
            condition_type TEXT,
            condition_value INTEGER
        );
        
        CREATE TABLE IF NOT EXISTS user_achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            achievement_id INTEGER,
            unlocked_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (achievement_id) REFERENCES achievements(id)
        );
        
        CREATE TABLE IF NOT EXISTS daily_quests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            quest_type TEXT NOT NULL,
            target_value INTEGER DEFAULT 1,
            current_value INTEGER DEFAULT 0,
            completed INTEGER DEFAULT 0,
            xp_reward INTEGER DEFAULT 10,
            date DATE DEFAULT CURRENT_DATE,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        
        -- Слова для изучения
        CREATE TABLE IF NOT EXISTS words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT NOT NULL,
            translation TEXT NOT NULL,
            transcription TEXT,
            emoji TEXT,
            category TEXT NOT NULL,
            example TEXT,
            difficulty INTEGER DEFAULT 1
        );
        
        -- Spaced Repetition: слова для повторения
        CREATE TABLE IF NOT EXISTS word_reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            word_id INTEGER,
            next_review DATE NOT NULL,
            interval_days INTEGER DEFAULT 1,
            ease_factor REAL DEFAULT 2.5,
            correct_streak INTEGER DEFAULT 0,
            total_reviews INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (word_id) REFERENCES words(id),
            UNIQUE(user_id, word_id)
        );
    """)
    conn.commit()
    conn.close()

# Инициализация при запуске
init_db()

# ============ MODELS ============

class UserCreate(BaseModel):
    tg_id: int
    username: Optional[str] = None
    first_name: str

class UserResponse(BaseModel):
    id: int
    tg_id: int
    username: Optional[str]
    first_name: str
    level: int
    xp: int
    xp_to_next_level: int
    streak_days: int
    diamonds: int

class LessonResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    category: str
    difficulty: int
    xp_reward: int
    order_num: int

class QuizResult(BaseModel):
    lesson_id: int
    correct_answers: int
    total_questions: int
    xp_earned: int

# ============ ROUTES ============

@app.get("/")
async def root():
    return {"message": "PlusTim API работает!", "version": "1.0.0"}

@app.post("/api/users/", response_model=UserResponse)
async def create_user(user: UserCreate):
    """Создание/получение пользователя"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE tg_id = ?", (user.tg_id,))
    existing = cursor.fetchone()
    
    if existing:
        conn.close()
        return dict(existing)
    
    cursor.execute("""
        INSERT INTO users (tg_id, username, first_name)
        VALUES (?, ?, ?)
    """, (user.tg_id, user.username, user.first_name))
    
    user_id = cursor.lastrowid
    
    daily_quests = [
        ("complete_lesson", 1, 10),
        ("earn_xp", 20, 15),
        ("streak", 1, 5),
    ]
    for quest_type, target, xp in daily_quests:
        cursor.execute("""
            INSERT INTO daily_quests (user_id, quest_type, target_value, xp_reward)
            VALUES (?, ?, ?, ?)
        """, (user_id, quest_type, target, xp))
    
    conn.commit()
    conn.close()
    
    return await get_user(user.tg_id)

@app.get("/api/users/{tg_id}", response_model=UserResponse)
async def get_user(tg_id: int):
    """Получение пользователя"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE tg_id = ?", (tg_id,))
    user = cursor.fetchone()
    conn.close()
    
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    return dict(user)

@app.get("/api/lessons/", response_model=List[LessonResponse])
async def get_lessons(category: Optional[str] = None):
    """Получение списка уроков"""
    conn = get_db()
    cursor = conn.cursor()
    
    if category:
        cursor.execute("SELECT * FROM lessons WHERE category = ? ORDER BY order_num", (category,))
    else:
        cursor.execute("SELECT * FROM lessons ORDER BY order_num")
    
    lessons = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return lessons

@app.get("/api/lessons/{lesson_id}/questions")
async def get_lesson_questions(lesson_id: int):
    """Получение вопросов урока"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT questions_json FROM lessons WHERE id = ?", (lesson_id,))
    result = cursor.fetchone()
    conn.close()
    
    if not result:
        raise HTTPException(status_code=404, detail="Урок не найден")
    
    import json
    questions = json.loads(result['questions_json'])
    
    for q in questions:
        correct_idx = q['correct_answer']
        options_with_idx = list(enumerate(q['options']))
        random.shuffle(options_with_idx)
        q['options'] = [opt[1] for opt in options_with_idx]
        q['correct_answer'] = next(i for i, (orig_idx, _) in enumerate(options_with_idx) if orig_idx == correct_idx)
    
    return questions

@app.post("/api/quiz/{lesson_id}/complete")
async def complete_quiz(tg_id: int, result: QuizResult):
    """Завершение викторины"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE tg_id = ?", (tg_id,))
    user = cursor.fetchone()
    
    if not user:
        conn.close()
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    user_id = user['id']
    
    cursor.execute("""
        INSERT OR REPLACE INTO user_progress 
        (user_id, lesson_id, completed, correct_answers, total_questions, xp_earned, completed_at)
        VALUES (?, ?, 1, ?, ?, ?, CURRENT_TIMESTAMP)
    """, (user_id, result.lesson_id, result.correct_answers, result.total_questions, result.xp_earned))
    
    new_xp = user['xp'] + result.xp_earned
    new_level = user['level']
    xp_to_next = user['xp_to_next_level']
    
    while new_xp >= xp_to_next:
        new_xp -= xp_to_next
        new_level += 1
        xp_to_next = int(xp_to_next * 1.5)
    
    cursor.execute("""
        UPDATE users SET xp = ?, level = ?, xp_to_next_level = ?,
        last_activity = CURRENT_TIMESTAMP WHERE id = ?
    """, (new_xp, new_level, xp_to_next, user_id))
    
    cursor.execute("""
        UPDATE daily_quests SET current_value = current_value + 1,
        completed = CASE WHEN current_value + 1 >= target_value THEN 1 ELSE 0 END
        WHERE user_id = ? AND quest_type = 'complete_lesson' AND completed = 0
    """, (user_id,))
    
    cursor.execute("""
        UPDATE daily_quests SET current_value = current_value + ?,
        completed = CASE WHEN current_value + ? >= target_value THEN 1 ELSE 0 END
        WHERE user_id = ? AND quest_type = 'earn_xp' AND completed = 0
    """, (result.xp_earned, result.xp_earned, user_id))
    
    conn.commit()
    conn.close()
    
    return {
        "new_xp": new_xp,
        "new_level": new_level,
        "xp_to_next_level": xp_to_next,
        "xp_earned": result.xp_earned
    }

@app.get("/api/achievements/")
async def get_achievements(tg_id: int):
    """Получение достижений пользователя"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM achievements")
    all_achievements = [dict(row) for row in cursor.fetchall()]
    
    cursor.execute("""
        SELECT achievement_id FROM user_achievements WHERE user_id = 
        (SELECT id FROM users WHERE tg_id = ?)
    """, (tg_id,))
    unlocked_ids = {row['achievement_id'] for row in cursor.fetchall()}
    
    conn.close()
    
    return [{
        **a,
        "unlocked": a['id'] in unlocked_ids
    } for a in all_achievements]

@app.get("/api/leaderboard/")
async def get_leaderboard(limit: int = 10):
    """Получение таблицы лидеров"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT tg_id, username, first_name, level, xp, streak_days
        FROM users ORDER BY level DESC, xp DESC LIMIT ?
    """, (limit,))
    
    leaderboard = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return leaderboard

@app.get("/api/daily-quests/{tg_id}")
async def get_daily_quests(tg_id: int):
    """Получение ежедневных заданий"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM daily_quests WHERE user_id = 
        (SELECT id FROM users WHERE tg_id = ?) AND date = CURRENT_DATE
    """, (tg_id,))
    
    quests = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return quests

@app.post("/api/daily-quests/{tg_id}/{quest_id}/claim")
async def claim_quest_reward(tg_id: int, quest_id: int):
    """Получение награды за задание"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT u.*, dq.xp_reward, dq.completed
        FROM users u
        JOIN daily_quests dq ON u.id = dq.user_id
        WHERE u.tg_id = ? AND dq.id = ?
    """, (tg_id, quest_id))
    
    result = cursor.fetchone()
    
    if not result:
        conn.close()
        raise HTTPException(status_code=404, detail="Квест не найден")
    
    if not result['completed']:
        conn.close()
        raise HTTPException(status_code=400, detail="Квест не выполнен")
    
    cursor.execute("""
        UPDATE users SET xp = xp + ? WHERE tg_id = ?
    """, (result['xp_reward'], tg_id))
    
    cursor.execute("""
        UPDATE daily_quests SET completed = 2 WHERE id = ?
    """, (quest_id,))
    
    conn.commit()
    conn.close()
    
    return {"xp_reward": result['xp_reward']}

# ============ TTS Audio Routes ============

@app.get("/api/tts/{word}")
async def get_word_pronunciation(word: str):
    """Получение аудио произношения слова через TTS"""
    try:
        tts = gTTS(text=word.lower(), lang='en', slow=False)
        
        audio_dir = os.path.join(os.path.dirname(__file__), "..", "static", "audio")
        os.makedirs(audio_dir, exist_ok=True)
        
        filename = f"{word.lower()}_{uuid.uuid4().hex[:8]}.mp3"
        filepath = os.path.join(audio_dir, filename)
        
        tts.save(filepath)
        
        return FileResponse(
            filepath, 
            media_type="audio/mpeg",
            headers={"Content-Disposition": f"inline; filename={filename}"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка генерации аудио: {str(e)}")

# ============ CATEGORIES & WORDS ROUTES ============

CATEGORY_NAMES = {
    "animals": "🐱 Животные",
    "food": "🍎 Еда",
    "colors": "🎨 Цвета",
    "numbers": "🔢 Числа",
    "family": "👨‍👩‍👧 Семья",
    "body": "💪 Части тела",
    "clothes": "👕 Одежда",
    "weather": "🌤️ Погода",
    "school": "🏫 Школа",
    "time": "⏰ Время",
    "transport": "🚗 Транспорт",
    "home": "🏠 Дом",
    "nature": "🌳 Природа",
    "actions": "🏃 Действия",
    "emotions": "😊 Эмоции",
    "adjectives": "📝 Прилагательные",
    "places": "📍 Места",
    "days": "📅 Дни недели",
    "months": "🗓️ Месяцы",
    "fruit": "🍇 Фрукты",
    "vegetables": "🥦 Овощи",
    "drinks": "🥤 Напитки",
    "jobs": "💼 Профессии",
    "sports": "⚽ Спорт",
    "hobbies": "🎨 Хобби",
    "rooms": "🚪 Комнаты",
    "furniture": "🪑 Мебель",
    "electronics": "💻 Электроника",
    "sea_animals": "🐋 Морские животные",
}

@app.get("/api/categories/")
async def get_categories():
    """Получение всех категорий с метаданными"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT DISTINCT category, COUNT(*) as word_count,
               MIN(difficulty) as min_difficulty,
               MAX(difficulty) as max_difficulty
        FROM words GROUP BY category ORDER BY category
    """)
    
    categories = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return [{
        **cat,
        "name": CATEGORY_NAMES.get(cat['category'], cat['category'].replace('_', ' ').title()),
        "level": "A1" if cat['min_difficulty'] == 1 else "A2" if cat['min_difficulty'] == 2 else "B1"
    } for cat in categories]

@app.get("/api/categories/{category}/info")
async def get_category_info(category: str):
    """Получение информации о категории"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT category, COUNT(*) as word_count,
               MIN(difficulty) as min_difficulty,
               MAX(difficulty) as max_difficulty,
               SUM(CASE WHEN difficulty = 1 THEN 1 ELSE 0 END) as a1_count,
               SUM(CASE WHEN difficulty = 2 THEN 1 ELSE 0 END) as a2_count,
               SUM(CASE WHEN difficulty = 3 THEN 1 ELSE 0 END) as b1_count
        FROM words WHERE category = ?
    """, (category,))
    
    result = cursor.fetchone()
    
    if not result:
        conn.close()
        raise HTTPException(status_code=404, detail="Категория не найдена")
    
    conn.close()
    
    return {
        "category": result['category'],
        "name": CATEGORY_NAMES.get(category, category.replace('_', ' ').title()),
        "total_words": result['word_count'],
        "difficulty": {
            "min": result['min_difficulty'],
            "max": result['max_difficulty'],
            "level": "A1" if result['min_difficulty'] == 1 else "A2" if result['min_difficulty'] == 2 else "B1"
        },
        "breakdown": {
            "A1": result['a1_count'],
            "A2": result['a2_count'],
            "B1": result['b1_count']
        }
    }

@app.get("/api/words/")
async def get_all_words():
    """Получение всех слов"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM words ORDER BY category, word")
    words = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return words

@app.get("/api/words/{category}")
async def get_words_by_category(category: str):
    """Получение слов по категории"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM words WHERE category = ?", (category,))
    words = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return words

@app.get("/api/words/{category}/random/{count}")
async def get_random_words(category: str, count: int = 5):
    """Получение случайных слов из категории"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM words WHERE category = ?", (category,))
    all_words = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    if len(all_words) <= count:
        return all_words
    
    return random.sample(all_words, count)

# ============ SPACED REPETITION ROUTES ============

@app.get("/api/reviews/{tg_id}")
async def get_reviews(tg_id: int):
    """Получить слова для повторения сегодня"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM users WHERE tg_id = ?", (tg_id,))
    user = cursor.fetchone()
    if not user:
        conn.close()
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    user_id = user['id']
    today = datetime.now().strftime('%Y-%m-%d')
    
    cursor.execute("""
        SELECT wr.id, wr.word_id, wr.interval_days, wr.correct_streak, 
               w.word, w.translation, w.transcription, w.emoji
        FROM word_reviews wr
        JOIN words w ON wr.word_id = w.id
        WHERE wr.user_id = ? AND wr.next_review <= ?
        ORDER BY wr.correct_streak ASC, wr.interval_days ASC
        LIMIT 10
    """, (user_id, today))
    
    reviews = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return {
        "count": len(reviews),
        "words": reviews
    }

@app.post("/api/reviews/{tg_id}/{word_id}/result")
async def record_review_result(tg_id: int, word_id: int, correct: bool):
    """Записать результат повторения (алгоритм SM-2)"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM users WHERE tg_id = ?", (tg_id,))
    user = cursor.fetchone()
    if not user:
        conn.close()
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    user_id = user['id']
    
    cursor.execute("""
        SELECT * FROM word_reviews WHERE user_id = ? AND word_id = ?
    """, (user_id, word_id))
    review = cursor.fetchone()
    
    today = datetime.now().strftime('%Y-%m-%d')
    
    if not review:
        if correct:
            interval = 1
            ease_factor = 2.5
            streak = 1
        else:
            interval = 1
            ease_factor = 2.5
            streak = 0
        
        next_review = datetime.now() + timedelta(days=interval)
        
        cursor.execute("""
            INSERT INTO word_reviews 
            (user_id, word_id, next_review, interval_days, ease_factor, correct_streak, total_reviews)
            VALUES (?, ?, ?, ?, ?, ?, 1)
        """, (user_id, word_id, next_review.strftime('%Y-%m-%d'), interval, ease_factor, streak))
    else:
        review = dict(review)
        interval = review['interval_days']
        ease_factor = review['ease_factor']
        streak = review['correct_streak']
        total_reviews = review['total_reviews'] + 1
        
        if correct:
            if streak == 0:
                interval = 1
            elif streak == 1:
                interval = 3
            else:
                interval = int(interval * ease_factor)
            streak += 1
            ease_factor = min(2.5, ease_factor + 0.1)
        else:
            interval = 1
            streak = 0
            ease_factor = max(1.3, ease_factor - 0.2)
        
        next_review = datetime.now() + timedelta(days=interval)
        
        cursor.execute("""
            UPDATE word_reviews 
            SET next_review = ?, interval_days = ?, ease_factor = ?, 
                correct_streak = ?, total_reviews = ?
            WHERE user_id = ? AND word_id = ?
        """, (
            next_review.strftime('%Y-%m-%d'), interval, ease_factor, 
            streak, total_reviews, user_id, word_id
        ))
    
    conn.commit()
    conn.close()
    
    xp_reward = 5 if correct else 1
    
    return {
        "correct": correct,
        "next_review_days": interval,
        "xp_earned": xp_reward
    }

@app.post("/api/reviews/{tg_id}/add")
async def add_words_for_review(tg_id: int, word_ids: List[int]):
    """Добавить слова для отслеживания повторений"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM users WHERE tg_id = ?", (tg_id,))
    user = cursor.fetchone()
    if not user:
        conn.close()
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    user_id = user['id']
    today = datetime.now().strftime('%Y-%m-%d')
    
    added = 0
    for word_id in word_ids:
        try:
            cursor.execute("""
                INSERT OR IGNORE INTO word_reviews 
                (user_id, word_id, next_review, interval_days, ease_factor, correct_streak, total_reviews)
                VALUES (?, ?, ?, 1, 2.5, 0, 0)
            """, (user_id, word_id, today))
            if cursor.rowcount > 0:
                added += 1
        except:
            pass
    
    conn.commit()
    conn.close()
    
    return {"added": added}

@app.get("/api/reviews/{tg_id}/stats")
async def get_review_stats(tg_id: int):
    """Статистика повторений"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM users WHERE tg_id = ?", (tg_id,))
    user = cursor.fetchone()
    if not user:
        conn.close()
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    user_id = user['id']
    today = datetime.now().strftime('%Y-%m-%d')
    
    cursor.execute("SELECT COUNT(*) FROM word_reviews WHERE user_id = ?", (user_id,))
    total_words = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM word_reviews WHERE user_id = ? AND next_review <= ?", (user_id, today))
    due_today = cursor.fetchone()[0]
    
    cursor.execute("SELECT MAX(correct_streak) FROM word_reviews WHERE user_id = ?", (user_id,))
    max_streak = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT SUM(total_reviews) FROM word_reviews WHERE user_id = ?", (user_id,))
    total_reviews = cursor.fetchone()[0] or 0
    
    conn.close()
    
    return {
        "total_words": total_words,
        "due_today": due_today,
        "max_correct_streak": max_streak,
        "total_reviews": total_reviews
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)