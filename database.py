# База данных PlusTim (SQLite + aiosqlite)
import aiosqlite
import asyncio
from datetime import datetime, date
from config import DATABASE_PATH

# SQL для создания таблиц
CREATE_TABLES_SQL = """
-- Пользователи
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    xp INTEGER DEFAULT 0,
    gems INTEGER DEFAULT 0,
    streak INTEGER DEFAULT 0,
    last_activity DATE,
    lessons_completed INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Слова для изучения
CREATE TABLE IF NOT EXISTS words (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word TEXT NOT NULL,
    translation TEXT NOT NULL,
    transcription TEXT,
    emoji TEXT,
    example TEXT,
    category TEXT DEFAULT 'animals'
);

-- Прогресс пользователя по словам
CREATE TABLE IF NOT EXISTS user_progress (
    user_id INTEGER,
    word_id INTEGER,
    correct_count INTEGER DEFAULT 0,
    wrong_count INTEGER DEFAULT 0,
    next_review DATE,
    PRIMARY KEY (user_id, word_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (word_id) REFERENCES words(id)
);

-- Достижения
CREATE TABLE IF NOT EXISTS achievements (
    code TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    xp_reward INTEGER DEFAULT 50,
    gems_reward INTEGER DEFAULT 10
);

-- Полученные достижения
CREATE TABLE IF NOT EXISTS user_achievements (
    user_id INTEGER,
    achievement_code TEXT,
    unlocked_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, achievement_code),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (achievement_code) REFERENCES achievements(code)
);

-- История занятий
CREATE TABLE IF NOT EXISTS lesson_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    lesson_date DATE DEFAULT CURRENT_DATE,
    words_learned INTEGER DEFAULT 0,
    xp_earned INTEGER DEFAULT 0,
    duration_seconds INTEGER DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
"""

# Данные достижений по умолчанию
DEFAULT_ACHIEVEMENTS = [
    ("first_lesson", "Первый шаг ✨", "Завершить первый урок", 50, 10),
    ("streak_7", "Неделя успеха 🚀", "Заниматься 7 дней подряд", 100, 25),
    ("streak_30", "Месяц побед 🏆", "Заниматься 30 дней подряд", 300, 100),
    ("words_50", "Большой словарь 🧠", "Выучить 50 слов", 200, 50),
    ("words_100", "Словарный запас 💎", "Выучить 100 слов", 500, 150),
    ("perfect", "Идеально! 🎯", "10 правильных ответов подряд", 150, 30),
    ("early_bird", "Ранняя пташка ☀️", "Заняться до 9 утра", 50, 10),
    ("explorer", "Исследователь 🗺️", "Попробовать все типы заданий", 100, 20),
    ("speed_demon", "Скорость света ⚡", "Ответить правильно за 3 секунды", 75, 15),
    ("night_owl", "Ночная сова 🌙", "Заняться после 21:00", 50, 10),
]


async def init_database():
    """Инициализация базы данных"""
    db = await aiosqlite.connect(DATABASE_PATH)
    await db.executescript(CREATE_TABLES_SQL)
    
    # Добавляем достижения, если их нет
    for ach in DEFAULT_ACHIEVEMENTS:
        await db.execute(
            """INSERT OR IGNORE INTO achievements (code, name, description, xp_reward, gems_reward)
            VALUES (?, ?, ?, ?, ?)""",
            ach
        )
    
    await db.commit()
    return db


async def get_user(db, user_id):
    """Получить пользователя или создать нового"""
    user = await db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = await user.fetchone()
    
    if not user:
        await db.execute(
            """INSERT INTO users (user_id, username, last_activity) VALUES (?, ?, ?)""",
            (user_id, None, date.today().isoformat())
        )
        await db.commit()
        user = await db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        user = await user.fetchone()
    
    return user


async def update_user_stats(db, user_id, xp_gained=0, gems_gained=0, lesson_completed=False):
    """Обновить статистику пользователя"""
    today = date.today().isoformat()
    
    user = await get_user(db, user_id)
    last_activity = user[5]  # last_activity column
    
    # Проверка и обновление стрика
    streak = user[4]
    if last_activity == today:
        # Сегодня уже был активен - стрик не меняется
        pass
    elif last_activity == date.today().isoformat():  # Вчера
        streak += 1
    else:
        streak = 1  # Стрик сброшен
    
    # Обновляем пользователя
    await db.execute(
        """UPDATE users SET 
        xp = xp + ?,
        gems = gems + ?,
        streak = ?,
        last_activity = ?,
        lessons_completed = lessons_completed + ? 
        WHERE user_id = ?""",
        (xp_gained, gems_gained, streak, today, 1 if lesson_completed else 0, user_id)
    )
    await db.commit()
    
    return {"streak": streak, "new_achievements": []}


async def add_achievement(db, user_id, achievement_code):
    """Добавить достижение пользователю"""
    # Проверяем, есть ли уже это достижение
    existing = await db.execute(
        "SELECT * FROM user_achievements WHERE user_id = ? AND achievement_code = ?",
        (user_id, achievement_code)
    )
    existing = await existing.fetchone()
    
    if existing:
        return None  # Достижение уже получено
    
    # Получаем данные достижения
    ach = await db.execute(
        "SELECT xp_reward, gems_reward FROM achievements WHERE code = ?",
        (achievement_code,)
    )
    ach = await ach.fetchone()
    
    if ach:
        # Добавляем достижение
        await db.execute(
            "INSERT INTO user_achievements (user_id, achievement_code) VALUES (?, ?)",
            (user_id, achievement_code)
        )
        
        # Начисляем награды
        await db.execute(
            "UPDATE users SET xp = xp + ?, gems = gems + ? WHERE user_id = ?",
            (ach[0], ach[1], user_id)
        )
        await db.commit()
        
        return {"xp": ach[0], "gems": ach[1], "name": achievement_code}
    
    return None


async def get_words_for_lesson(db, count=3, category="animals"):
    """Получить слова для урока"""
    words = await db.execute(
        """SELECT * FROM words WHERE category = ? 
        ORDER BY RANDOM() LIMIT ?""",
        (category, count)
    )
    return await words.fetchall()


async def check_and_award_achievements(db, user_id):
    """Проверить и выдать достижения"""
    user = await get_user(db, user_id)
    new_achievements = []
    
    # Проверяем условия достижений
    lessons_completed = user[7]
    xp = user[2]
    gems = user[3]
    streak = user[4]
    words_learned = await get_words_learned_count(db, user_id)
    
    # Первый урок
    if lessons_completed >= 1:
        result = await add_achievement(db, user_id, "first_lesson")
        if result:
            new_achievements.append(result)
    
    # Стрик 7 дней
    if streak >= 7:
        result = await add_achievement(db, user_id, "streak_7")
        if result:
            new_achievements.append(result)
    
    # Стрик 30 дней
    if streak >= 30:
        result = await add_achievement(db, user_id, "streak_30")
        if result:
            new_achievements.append(result)
    
    # 50 слов
    if words_learned >= 50:
        result = await add_achievement(db, user_id, "words_50")
        if result:
            new_achievements.append(result)
    
    # 100 слов
    if words_learned >= 100:
        result = await add_achievement(db, user_id, "words_100")
        if result:
            new_achievements.append(result)
    
    await db.commit()
    return new_achievements


async def get_words_learned_count(db, user_id):
    """Получить количество выученных слов"""
    result = await db.execute(
        "SELECT COUNT(*) FROM user_progress WHERE user_id = ? AND correct_count >= 3",
        (user_id,)
    )
    result = await result.fetchone()
    return result[0] if result else 0


async def update_word_progress(db, user_id, word_id, correct):
    """Обновить прогресс по слову"""
    progress = await db.execute(
        "SELECT * FROM user_progress WHERE user_id = ? AND word_id = ?",
        (user_id, word_id)
    )
    progress = await progress.fetchone()
    
    if progress:
        if correct:
            await db.execute(
                """UPDATE user_progress SET 
                correct_count = correct_count + 1,
                wrong_count = wrong_count 
                WHERE user_id = ? AND word_id = ?""",
                (user_id, word_id)
            )
        else:
            await db.execute(
                """UPDATE user_progress SET 
                wrong_count = wrong_count + 1 
                WHERE user_id = ? AND word_id = ?""",
                (user_id, word_id)
            )
    else:
        await db.execute(
            """INSERT INTO user_progress 
            (user_id, word_id, correct_count, wrong_count, next_review)
            VALUES (?, ?, ?, ?, ?)""",
            (user_id, word_id, 1 if correct else 0, 0 if correct else 1, date.today().isoformat())
        )
    
    await db.commit()


async def get_user_leaderboard(db, limit=10):
    """Получить таблицу лидеров"""
    cursor = await db.execute(
        "SELECT user_id, username, xp, gems, streak FROM users ORDER BY xp DESC LIMIT ?",
        (limit,)
    )
    return await cursor.fetchall()


async def close_database(db):
    """Закрыть соединение с БД"""
    await db.close()


# Функция для запуска инициализации
async def setup():
    db = await init_database()
    print("✅ База данных инициализирована")
    return db


if __name__ == "__main__":
    asyncio.run(setup())