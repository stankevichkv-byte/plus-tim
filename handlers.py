# Обработчики бота PlusTim (FSM + логика уроков)
import logging
from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from datetime import datetime

import database
import keyboards as kb
import content as c
from config import XP_PER_CORRECT, XP_PER_LESSON, LESSON_WORDS_COUNT, ACHIEVEMENT_EMOJIS

router = Router()

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============ FSM States ============
class LessonStates(StatesGroup):
    """Состояния для урока"""
    idle = State()                    # Ожидание начала урока
    choosing_category = State()       # Выбор категории
    discovery = State()               # Знакомство со словом
    quiz = State()                   # Викторина "Угадай по картинке"
    missing_letter = State()          # Игра "Пропавшая буква"
    speed_round = State()            # Скоростной раунд
    lesson_complete = State()         # Урок завершён


class ProfileStates(StatesGroup):
    """Состояния для профиля"""
    viewing = State()


# ============ Глобальные переменные сессии ============
user_sessions = {}  # {user_id: {"words": [...], "current_word_index": 0, "xp_earned": 0}}


# ============ Команды ============
@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    """Обработка команды /start"""
    user_id = message.from_user.id
    username = message.from_user.username
    
    # Инициализация БД и пользователя
    db = await database.init_database()
    await database.get_user(db, user_id)
    
    # Обновляем username
    await db.execute("UPDATE users SET username = ? WHERE user_id = ?", (username, user_id))
    await db.commit()
    
    # Сбрасываем состояние
    await state.clear()
    
    # Отправляем приветствие
    welcome_text = f"""👋 Привет, {message.from_user.first_name}!

🎮 Нажми на кнопку ниже, чтобы начать играть!"""
    
    await message.answer(welcome_text, reply_markup=kb.get_main_menu())
    await state.set_state(LessonStates.idle)
    
    await database.close_database(db)


@router.message(Command("help"))
async def cmd_help(message: Message):
    """Помощь"""
    help_text = """ℹ️ PlusTim — бот для изучения английского!

📖 Как пользоваться:
1. Нажми "Начать урок"
2. Выбери тему (животные, еда и т.д.)
3. Изучай новые слова
4. Играй в игры
5. Получай звёзды и достижения!

🎯 Команды:
/start — начать заново
/profile — твой профиль
/achievements — достижения
/leaderboard — топ игроков"""
    
    await message.answer(help_text, reply_markup=kb.get_main_menu())


# ============ Главное меню ============
@router.message(F.text == "🎮 Начать урок")
async def start_lesson(message: Message, state: FSMContext):
    """Начало урока"""
    await message.answer("📚 Выбери тему:", reply_markup=kb.get_category_keyboard())
    await state.set_state(LessonStates.choosing_category)


@router.message(F.text == "📚 Мой профиль")
async def show_profile(message: Message, state: FSMContext):
    """Показать профиль пользователя"""
    db = await database.init_database()
    user = await database.get_user(db, message.from_user.id)
    
    profile_text = f"""📚 ТВОЙ ПРОФИЛЬ

⭐ Звёзды: {user[2]}
💎 Кристаллы: {user[3]}
🔥 Стрик: {user[4]} дней
📖 Уроков: {user[7]}

Дата регистрации: {user[7][:10] if user[7] else "неизвестно"}"""
    
    await message.answer_photo(
        photo="https://images.unsplash.com/photo-1633332755192-727a05c4013d?w=400",
        caption=profile_text,
        reply_markup=kb.get_profile_keyboard()
    )
    
    await state.set_state(ProfileStates.viewing)
    await database.close_database(db)


@router.message(F.text == "🏆 Достижения")
async def show_achievements(message: Message, state: FSMContext):
    """Показать достижения"""
    db = await database.init_database()
    user_id = message.from_user.id
    
    # Получаем достижения пользователя
    user_achs = await db.execute(
        "SELECT achievement_code FROM user_achievements WHERE user_id = ?",
        (user_id,)
    )
    user_achs = [row[0] for row in await user_achs.fetchall()]
    
    # Формируем текст
    ach_text = "🏆 ТВОИ ДОСТИЖЕНИЯ\n\n"
    
    all_achs = await db.execute("SELECT * FROM achievements")
    all_achs = await all_achs.fetchall()
    
    for ach in all_achs:
        emoji = ACHIEVEMENT_EMOJIS.get(ach[0], "🎯")
        status = "✅" if ach[0] in user_achs else "🔒"
        ach_text += f"{status} {emoji} {ach[1]}\n"
        ach_text += f"   {ach[2]} (+{ach[3]}⭐)\n\n"
    
    await message.answer(ach_text, reply_markup=kb.get_achievements_keyboard())
    await database.close_database(db)


@router.message(F.text == "👥 Топ игроков")
async def show_leaderboard(message: Message):
    """Показать таблицу лидеров"""
    db = await database.init_database()
    leaders = await database.get_user_leaderboard(db, 10)
    
    leader_text = "👥 ТОП ИГРОКОВ\n\n"
    
    for i, leader in enumerate(leaders, 1):
        name = leader[1] or f"Player {leader[0]}"
        leader_text += f"{i}. {name}\n"
        leader_text += f"   ⭐ {leader[2]} | 🔥 {leader[4]}\n\n"
    
    await message.answer(leader_text, reply_markup=kb.get_main_menu())
    await database.close_database(db)


@router.message(F.text.startswith("🌐 Открыть"))
async def open_webapp(message: Message):
    """Открыть Web App"""
    webapp_url = kb.WEB_APP_URL
    await message.answer(
        f"🌐 Нажми кнопку ниже, чтобы открыть интерактивное приложение PlusTim!",
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [types.InlineKeyboardButton(text="🎮 ОТКРЫТЬ ПРИЛОЖЕНИЕ", web_app=types.WebAppInfo(url=webapp_url))]
            ]
        )
    )


@router.message(F.text == "📊 Статистика")
async def show_stats(message: Message):
    """Показать статистику"""
    db = await database.init_database()
    user = await database.get_user(db, message.from_user.id)
    words_learned = await database.get_words_learned_count(db, message.from_user.id)
    
    stats_text = f"""📊 ТВОЯ СТАТИСТИКА

📚 Выучено слов: {words_learned}
⭐ Всего звёзд: {user[2]}
💎 Кристаллов: {user[3]}
🔥 Дней подряд: {user[4]}
📖 Уроков: {user[7]}

💪 Так держать!"""
    
    await message.answer(stats_text, reply_markup=kb.get_main_menu())
    await database.close_database(db)


# ============ Выбор категории ============
@router.callback_query(StateFilter(LessonStates.choosing_category))
async def choose_category(callback: CallbackQuery, state: FSMContext):
    """Обработка выбора категории"""
    category = callback.data.split(":")[1]
    
    # Получаем слова для урока
    db = await database.init_database()
    words = await database.get_words_for_lesson(db, LESSON_WORDS_COUNT, category)
    await database.close_database(db)
    
    if not words:
        await callback.message.edit_text("😢 В этой категории пока нет слов!\n\nВыбери другую тему:")
        return
    
    # Сохраняем сессию
    user_sessions[callback.from_user.id] = {
        "words": words,
        "current_word_index": 0,
        "xp_earned": 0,
        "category": category,
        "correct_in_row": 0
    }
    
    await callback.message.delete()
    
    # Начинаем урок с первого слова
    await show_word(callback.message, state)


# ============ Показ слова (Discovery) ============
async def show_word(message: types.Message, state: FSMContext):
    """Показать слово для изучения"""
    user_id = message.chat.id
    session = user_sessions.get(user_id)
    
    if not session:
        await message.answer("⚠️ Что-то пошло не так. Начни урок заново!", reply_markup=kb.get_main_menu())
        await state.set_state(LessonStates.idle)
        return
    
    if session["current_word_index"] >= len(session["words"]):
        # Все слова изучены - переходим к викторине
        await message.answer("🎉 Отлично! Все новые слова выучены!\n\nТеперь проверим, как ты их запомнил!")
        await state.set_state(LessonStates.quiz)
        await show_quiz(message, state)
        return
    
    word = session["words"][session["current_word_index"]]
    
    text = f"""📖 НОВОЕ СЛОВО!

{word['emoji']} <b>{word['word']}</b> {word['transcription']}
📝 {word['translation']}

💡 {word['example']}"""
    
    await message.answer(
        text,
        reply_markup=kb.get_lesson_keyboard()
    )
    
    await state.set_state(LessonStates.discovery)


# ============ Кнопки урока ============
@router.callback_query(StateFilter(LessonStates.discovery))
async def lesson_callback(callback: CallbackQuery, state: FSMContext):
    """Обработка кнопок в блоке Discovery"""
    action = callback.data.split(":")[1]
    
    if action == "listen":
        # Воспроизводим аудио
        session = user_sessions.get(callback.from_user.id)
        if session:
            word = session["words"][session["current_word_index"]]
            if word.audio_url:
                await callback.message.answer_audio(
                    audio=word.audio_url,
                    caption="🔊 Слушай внимательно!"
                )
    
    elif action == "next":
        # Переходим к следующему слову
        session = user_sessions.get(callback.from_user.id)
        if session:
            session["current_word_index"] += 1
        
        await callback.message.delete()
        await show_word(callback.message, state)
    
    await callback.answer()


# ============ Викторина (Quiz) ============
async def show_quiz(message: types.Message, state: FSMContext):
    """Показать вопрос викторины"""
    user_id = message.chat.id
    session = user_sessions.get(user_id)
    
    if not session or session["current_word_index"] >= len(session["words"]):
        # Все слова проверены - переходим к Missing Letter
        await message.answer("🎯 Викторина завершена!\n\nТеперь напишем слова без подсказок!")
        await state.set_state(LessonStates.missing_letter)
        await show_missing_letter(message, state)
        return
    
    word = session["words"][session["current_word_index"]]
    options = c.generate_quiz_options(word)
    
    text = f"""🎯 УГАДАЙ ПО КАРТИНКЕ!

{word['emoji']} — что это?"""
    
    await message.answer(
        text,
        reply_markup=kb.get_quiz_keyboard(word['word'], options)
    )


@router.callback_query(StateFilter(LessonStates.quiz))
async def quiz_answer(callback: CallbackQuery, state: FSMContext):
    """Обработка ответа в викторине"""
    _, _, answer = callback.data.split(":")
    
    user_id = callback.from_user.id
    session = user_sessions.get(user_id)
    
    if not session:
        await callback.message.answer("⚠️ Начни урок заново!", reply_markup=kb.get_main_menu())
        await state.set_state(LessonStates.idle)
        await callback.answer()
        return
    
    word = session["words"][session["current_word_index"]]
    
    if answer.lower() == word['word'].lower():
        # Правильный ответ
        session["xp_earned"] += XP_PER_CORRECT
        session["correct_in_row"] += 1
        
        await callback.message.edit_text(
            f"🎉 ПРАВИЛЬНО! +{XP_PER_CORRECT}⭐\n\n{word['emoji']} <b>{word['word']}</b> — {word['translation']}"
        )
        
        # Обновляем прогресс в БД
        db = await database.init_database()
        await database.update_word_progress(db, user_id, word['id'], True)
        await database.close_database(db)
    else:
        # Неправильный ответ
        session["correct_in_row"] = 0
        
        await callback.message.edit_text(
            f"🤔 Не совсем...\n\nПравильный ответ: <b>{word['word']}</b>\n{word['translation']}"
        )
    
    session["current_word_index"] += 1
    await callback.answer()
    
    # Следующий вопрос
    await show_quiz(callback.message, state)


# ============ Missing Letter ============
async def show_missing_letter(message: types.Message, state: FSMContext):
    """Показать слово с пропущенной буквой"""
    user_id = message.chat.id
    session = user_sessions.get(user_id)
    
    if not session or session["current_word_index"] >= len(session["words"]):
        # Все слова написаны - переходим к скоростному раунду
        await message.answer("✏️ Отлично! Все слова написаны!\n\nТеперь проверим скорость!")
        await state.set_state(LessonStates.speed_round)
        await show_speed_round(message, state)
        return
    
    word = session["words"][session["current_word_index"]]
    masked_word, letter_options, _ = c.get_missing_letter_word(word)
    
    text = f"""✏️ ПРОПАВШАЯ БУКВА!

Слово: <b>{masked_word}</b>
Перевод: {word['translation']} {word['emoji']}

Какой буквы не хватает?"""
    
    await message.answer(
        text,
        reply_markup=kb.get_missing_letter_keyboard(letter_options, word['id'])
    )


@router.callback_query(StateFilter(LessonStates.missing_letter))
async def missing_letter_answer(callback: CallbackQuery, state: FSMContext):
    """Обработка ответа в Missing Letter"""
    _, _, letter, word_id = callback.data.split(":")
    
    user_id = callback.from_user.id
    session = user_sessions.get(user_id)
    
    if not session:
        await callback.message.answer("⚠️ Начни урок заново!", reply_markup=kb.get_main_menu())
        await state.set_state(LessonStates.idle)
        await callback.answer()
        return
    
    word = session["words"][session["current_word_index"]]
    
    # Получаем правильный ответ
    _, _, correct_letter = c.get_missing_letter_word(word)
    
    if letter.lower() == correct_letter.lower():
        session["xp_earned"] += XP_PER_CORRECT
        session["correct_in_row"] += 1
        
        await callback.message.edit_text(
            f"🎉 ПРАВИЛЬНО! +{XP_PER_CORRECT}⭐\n\n<b>{word['word']}</b> — {word['translation']}"
        )
        
        # Обновляем прогресс в БД
        db = await database.init_database()
        await database.update_word_progress(db, user_id, word['id'], True)
        await database.close_database(db)
    else:
        session["correct_in_row"] = 0
        
        await callback.message.edit_text(
            f"🤔 Не совсем...\n\nПравильно: <b>{word['word']}</b> ({correct_letter.upper()})"
        )
    
    session["current_word_index"] += 1
    await callback.answer()
    
    await show_missing_letter(callback.message, state)


# ============ Speed Round ============
async def show_speed_round(message: types.Message, state: FSMContext):
    """Показать скоростной раунд"""
    user_id = message.chat.id
    session = user_sessions.get(user_id)
    
    if not session or session["current_word_index"] >= len(session["words"]):
        # Скоростной раунд завершён
        await finish_lesson(message, state)
        return
    
    word = session["words"][session["current_word_index"]]
    options = c.generate_quiz_options(word)
    
    text = f"""⚡ СКОРОСТНОЙ РАУНД!

Покажи, как быстро ты можешь!

{word['emoji']} {word['translation']} — ..."""
    
    await message.answer(
        text,
        reply_markup=kb.get_quiz_keyboard(word['word'], options)
    )


@router.callback_query(StateFilter(LessonStates.speed_round))
async def speed_round_answer(callback: CallbackQuery, state: FSMContext):
    """Обработка ответа в Speed Round"""
    _, _, answer = callback.data.split(":")
    
    user_id = callback.from_user.id
    session = user_sessions.get(user_id)
    
    if not session:
        await callback.message.answer("⚠️ Начни урок заново!", reply_markup=kb.get_main_menu())
        await state.set_state(LessonStates.idle)
        await callback.answer()
        return
    
    word = session["words"][session["current_word_index"]]
    
    if answer.lower() == word['word'].lower():
        session["xp_earned"] += XP_PER_CORRECT + 5  # Бонус за скорость
        session["correct_in_row"] += 1
        
        await callback.message.edit_text(
            f"⚡ БЫСТРО! +{XP_PER_CORRECT + 5}⭐"
        )
        
        db = await database.init_database()
        await database.update_word_progress(db, user_id, word['id'], True)
        await database.close_database(db)
    else:
        session["correct_in_row"] = 0
        
        await callback.message.edit_text(
            f"⏱️ Не успел!\n\nПравильный ответ: <b>{word['word']}</b>"
        )
    
    session["current_word_index"] += 1
    await callback.answer()
    
    await show_speed_round(callback.message, state)


# ============ Завершение урока ============
async def finish_lesson(message: types.Message, state: FSMContext):
    """Завершение урока"""
    user_id = message.chat.id
    session = user_sessions.pop(user_id, None)
    
    if not session:
        await message.answer("⚠️ Начни урок заново!", reply_markup=kb.get_main_menu())
        await state.set_state(LessonStates.idle)
        return
    
    # Добавляем XP за завершение урока
    total_xp = session["xp_earned"] + XP_PER_LESSON
    
    # Обновляем статистику в БД
    db = await database.init_database()
    await database.update_user_stats(db, user_id, xp_gained=total_xp, lesson_completed=True)
    
    # Проверяем достижения
    new_achievements = await database.check_and_award_achievements(db, user_id)
    
    user = await database.get_user(db, user_id)
    await database.close_database(db)
    
    # Формируем текст завершения
    result_text = f"""🏆 УРОК ЗАВЕРШЁН!

⭐ ЗА УРОК: +{total_xp} звёзд
🔥 Стрик: {user[4]} дней

"""
    
    if new_achievements:
        for ach in new_achievements:
            emoji = ACHIEVEMENT_EMOJIS.get(ach["name"], "🎯")
            result_text += f"🎊 НОВОЕ ДОСТИЖЕНИЕ!\n{emoji} +{ach['xp']}⭐\n\n"
    
    result_text += "💪 Так держать! Ты молодец!"
    
    await message.answer(
        result_text,
        reply_markup=kb.get_lesson_complete_keyboard()
    )
    
    await state.set_state(LessonStates.lesson_complete)


@router.callback_query(StateFilter(LessonStates.lesson_complete))
async def lesson_complete_callback(callback: CallbackQuery, state: FSMContext):
    """Обработка кнопок после завершения урока"""
    action = callback.data.split(":")[1]
    
    if action == "new":
        await callback.message.delete()
        await callback.message.answer("📚 Выбери тему:", reply_markup=kb.get_category_keyboard())
        await state.set_state(LessonStates.choosing_category)
    else:
        await callback.message.delete()
        await callback.message.answer("🏠 Главное меню:", reply_markup=kb.get_main_menu())
        await state.set_state(LessonStates.idle)
    
    await callback.answer()


# ============ Navigation ============
@router.callback_query(lambda c: c.data == "menu:main")
async def back_to_menu(callback: CallbackQuery, state: FSMContext):
    """Возврат в главное меню"""
    await callback.message.delete()
    await callback.message.answer("🏠 Главное меню:", reply_markup=kb.get_main_menu())
    await state.set_state(LessonStates.idle)
    await callback.answer()


@router.callback_query(lambda c: c.data == "profile:refresh")
async def refresh_profile(callback: CallbackQuery, state: FSMContext):
    """Обновить профиль"""
    await show_profile(callback.message, state)
    await callback.answer()


@router.callback_query(lambda c: c.data == "achievements:all")
async def show_all_achievements(callback: CallbackQuery):
    """Показать все достижения"""
    db = await database.init_database()
    user_id = callback.from_user.id
    
    user_achs = await db.execute(
        "SELECT achievement_code FROM user_achievements WHERE user_id = ?",
        (user_id,)
    )
    user_achs = [row[0] for row in await user_achs.fetchall()]
    
    ach_text = "🏆 ВСЕ ДОСТИЖЕНИЯ\n\n"
    
    all_achs = await db.execute("SELECT * FROM achievements")
    all_achs = await all_achs.fetchall()
    
    for ach in all_achs:
        emoji = ACHIEVEMENT_EMOJIS.get(ach[0], "🎯")
        status = "✅" if ach[0] in user_achs else "🔒"
        ach_text += f"{status} {emoji} {ach[1]}\n"
    
    await callback.message.edit_text(ach_text, reply_markup=kb.get_achievements_keyboard())
    await database.close_database(db)
    await callback.answer()


# ============ Fallback ============
@router.message()
async def unknown_message(message: Message):
    """Обработка неизвестных сообщений"""
    await message.answer(
        "😕 Не понял...\n\nНажми кнопку в меню или /start для начала!",
        reply_markup=kb.get_main_menu()
    )