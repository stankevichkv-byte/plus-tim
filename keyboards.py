# Клавиатуры бота PlusTim
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
import os

# URL Web App (localhost для разработки, production - через переменную окружения)
WEB_APP_URL = os.getenv("WEB_APP_URL", "http://localhost:3000")

# Главное меню (только Web App)
def get_main_menu() -> ReplyKeyboardMarkup:
    """Главное меню бота - только кнопка Web App"""
    builder = ReplyKeyboardBuilder()
    
    builder.add(KeyboardButton(text="🎮 ОТКРЫТЬ ПРИЛОЖЕНИЕ", web_app=WebAppInfo(url=WEB_APP_URL)))
    
    return builder.as_markup(resize_keyboard=True)


# Главное меню с Web App (альтернативная версия)
def get_main_menu_webapp() -> ReplyKeyboardMarkup:
    """Главное меню с кнопкой Web App"""
    builder = ReplyKeyboardBuilder()
    
    builder.add(KeyboardButton(text="🎮 Уроки", web_app=WebAppInfo(url=WEB_APP_URL)))
    builder.add(KeyboardButton(text="⚡ Быстрая игра", web_app=WebAppInfo(url=WEB_APP_URL)))
    builder.add(KeyboardButton(text="📚 Профиль", web_app=WebAppInfo(url=WEB_APP_URL)))
    builder.add(KeyboardButton(text="🏆 Топ игроков"))
    builder.add(KeyboardButton(text="🌐 Играть в приложении", web_app=WebAppInfo(url=WEB_APP_URL)))
    
    builder.adjust(2, 2, 1)
    return builder.as_markup(resize_keyboard=True)


# Клавиатура урока
def get_lesson_keyboard(has_audio: bool = True) -> InlineKeyboardMarkup:
    """Клавиатура для блока знакомства со словом"""
    builder = InlineKeyboardBuilder()
    
    if has_audio:
        builder.add(InlineKeyboardButton(text="🔊 Послушать", callback_data="lesson:listen"))
    
    builder.add(InlineKeyboardButton(text="➡️ Дальше", callback_data="lesson:next"))
    
    return builder.as_markup()


# Клавиатура для викторины (картинка)
def get_quiz_keyboard(word: str, options: list) -> InlineKeyboardMarkup:
    """Клавиатура для викторины с вариантами ответов"""
    builder = InlineKeyboardBuilder()
    
    # Создаём кнопки для каждого варианта
    for option in options:
        builder.add(InlineKeyboardButton(
            text=option,
            callback_data=f"quiz:answer:{option}"
        ))
    
    builder.adjust(2)
    return builder.as_markup()


# Клавиатура для Missing Letter
def get_missing_letter_keyboard(letter_options: list, word_id: int) -> InlineKeyboardMarkup:
    """Клавиатура для игры с пропущенной буквой"""
    builder = InlineKeyboardBuilder()
    
    for letter in letter_options:
        builder.add(InlineKeyboardButton(
            text=letter.upper(),
            callback_data=f"missing:letter:{letter}:{word_id}"
        ))
    
    builder.adjust(2)
    return builder.as_markup()


# Клавиатура завершения урока
def get_lesson_complete_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура после завершения урока"""
    builder = InlineKeyboardBuilder()
    
    builder.add(InlineKeyboardButton(text="🎮 Ещё урок", callback_data="lesson:new"))
    builder.add(InlineKeyboardButton(text="🏠 В меню", callback_data="menu:main"))
    
    return builder.as_markup()


# Клавиатура профиля
def get_profile_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура профиля"""
    builder = InlineKeyboardBuilder()
    
    builder.add(InlineKeyboardButton(text="🔄 Обновить", callback_data="profile:refresh"))
    builder.add(InlineKeyboardButton(text="🏠 В меню", callback_data="menu:main"))
    
    return builder.as_markup()


# Клавиатура достижений
def get_achievements_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура достижений"""
    builder = InlineKeyboardBuilder()
    
    builder.add(InlineKeyboardButton(text="🔄 Показать все", callback_data="achievements:all"))
    builder.add(InlineKeyboardButton(text="🏠 В меню", callback_data="menu:main"))
    
    return builder.as_markup()


# Клавиатура выбора категории
def get_category_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура выбора категории"""
    builder = InlineKeyboardBuilder()
    
    builder.add(InlineKeyboardButton(text="🐾 Животные", callback_data="category:animals"))
    builder.add(InlineKeyboardButton(text="🍎 Еда", callback_data="category:food"))
    builder.add(InlineKeyboardButton(text="🌈 Цвета", callback_data="category:colors"))
    builder.add(InlineKeyboardButton(text="🔢 Числа", callback_data="category:numbers"))
    builder.add(InlineKeyboardButton(text="👨‍👩‍👧 Семья", callback_data="category:family"))
    
    builder.adjust(2, 2, 1)
    return builder.as_markup()


# Клавиатура навигации
def get_navigation_keyboard() -> InlineKeyboardMarkup:
    """Навигационная клавиатура"""
    builder = InlineKeyboardBuilder()
    
    builder.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="nav:back"))
    builder.add(InlineKeyboardButton(text="🏠 В меню", callback_data="menu:main"))
    builder.add(InlineKeyboardButton(text="⬆️ В начало", callback_data="nav:top"))
    
    return builder.as_markup()


# Клавиатура для скоростного раунда
def get_speed_round_keyboard(word_id: int) -> InlineKeyboardMarkup:
    """Клавиатура для скоростного раунда"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="⚡ Быстрый ответ", callback_data=f"speed:answer:{word_id}"))
    return builder.as_markup()


# Клавиатура подтверждения
def get_confirm_keyboard(confirm_text: str = "Да", cancel_text: str = "Нет") -> InlineKeyboardMarkup:
    """Клавиатура подтверждения"""
    builder = InlineKeyboardBuilder()
    
    builder.add(InlineKeyboardButton(text=confirm_text, callback_data="confirm:yes"))
    builder.add(InlineKeyboardButton(text=cancel_text, callback_data="confirm:no"))
    
    return builder.as_markup()


# Клавиатура выбора сложности
def get_difficulty_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура выбора сложности"""
    builder = InlineKeyboardBuilder()
    
    builder.add(InlineKeyboardButton(text="🌱 Легко", callback_data="difficulty:easy"))
    builder.add(InlineKeyboardButton(text="🌿 Нормально", callback_data="difficulty:medium"))
    builder.add(InlineKeyboardButton(text="🌳 Сложно", callback_data="difficulty:hard"))
    
    return builder.as_markup()


# Inline-кнопка "Назад в меню"
def back_to_menu_button() -> InlineKeyboardMarkup:
    """Кнопка возврата в меню"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏠 В меню", callback_data="menu:main")]
        ]
    )


# Кнопка "Поделиться результатом"
def share_result_keyboard() -> InlineKeyboardMarkup:
    """Кнопка для шеринга результата"""
    builder = InlineKeyboardBuilder()
    
    builder.add(InlineKeyboardButton(
        text="📤 Поделиться",
        switch_inline_query=f"Я получил {0}⭐ в PlusTim! Присоединяйся!"
    ))
    builder.add(InlineKeyboardButton(text="🏠 В меню", callback_data="menu:main"))
    
    return builder.as_markup()