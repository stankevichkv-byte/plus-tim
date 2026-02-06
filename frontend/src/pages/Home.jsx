import React, { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { useUserStore } from '../store'
import { vibrate, getUserData, getInitData } from '../api/telegram'

// Icons
import LessonIcon from '../assets/lesson.svg'
import GameIcon from '../assets/game.svg'
import TrophyIcon from '../assets/trophy.svg'
import StarIcon from '../assets/star.svg'

// Уровни с эмодзи
const LEVELS = {
  1: { name: 'Новичок', emoji: '🌱' },
  2: { name: 'Искатель', emoji: '🔍' },
  3: { name: 'Исследователь', emoji: '🗺️' },
  4: { name: 'Знаток', emoji: '📚' },
  5: { name: 'Ученик', emoji: '🎒' },
  6: { name: 'Любопытный', emoji: '🤔' },
  7: { name: 'Внимательный', emoji: '👀' },
  8: { name: 'Старательный', emoji: '💪' },
  9: { name: 'Талант', emoji: '⭐' },
  10: { name: 'Мастер', emoji: '🏆' },
  11: { name: 'Эксперт', emoji: '🎓' },
  12: { name: 'Профи', emoji: '💎' },
  13: { name: 'Гений', emoji: '🧠' },
  14: { name: 'Легенда', emoji: '👑' },
  15: { name: 'Чемпион', emoji: '🏅' },
}

// Категории уроков с иконками
const CATEGORIES = [
  { id: 'animals', name: '🐾 Животные', emoji: '🦁', color: 'from-green-400 to-emerald-500', bgColor: 'bg-green-500', words: 10 },
  { id: 'food', name: '🍎 Еда', emoji: '🍕', color: 'from-orange-400 to-red-500', bgColor: 'bg-orange-500', words: 10 },
  { id: 'colors', name: '🌈 Цвета', emoji: '🎨', color: 'from-purple-400 to-pink-500', bgColor: 'bg-purple-500', words: 10 },
  { id: 'numbers', name: '🔢 Числа', emoji: '🔢', color: 'from-blue-400 to-indigo-500', bgColor: 'bg-blue-500', words: 10 },
  { id: 'family', name: '👨‍👩‍👧 Семья', emoji: '👨‍👩‍👧‍👦', color: 'from-yellow-400 to-orange-500', bgColor: 'bg-yellow-500', words: 10 },
]

function Home() {
  const navigate = useNavigate()
  const { user } = useUserStore()
  
  // Получаем данные из Telegram если есть
  const tgUser = getUserData()
  const displayUser = user || tgUser ? {
    first_name: user?.first_name || tgUser?.first_name || 'Друг',
    xp: user?.xp || 250,
    gems: user?.gems || 15,
    streak: user?.streak || 3,
    level: user?.level || 3,
  } : { first_name: 'Друг', xp: 0, gems: 0, streak: 0, level: 1 }
  
  const currentLevel = LEVELS[displayUser.level] || LEVELS[1]
  
  // Расчёт прогресса до следующего уровня
  const xpForNextLevel = displayUser.level < 15 ? displayUser.level * 100 : displayUser.xp + 500
  const xpProgress = Math.min((displayUser.xp / xpForNextLevel) * 100, 100)
  
  const handleCategorySelect = (categoryId) => {
    vibrate('impact')
    navigate(`/lesson/${categoryId}`)
  }
  
  const handleQuickGame = () => {
    vibrate('impact')
    navigate('/lesson/animals')
  }
  
  return (
    <div className="pb-24 pt-4 px-4">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-5"
      >
        {/* User greeting */}
        <div className="flex items-center justify-between mb-4">
          <div>
            <h1 className="text-[26px] font-extrabold text-white leading-tight">
              Привет, {displayUser.first_name}!
            </h1>
            <p className="text-white/70 text-[15px] mt-1">
              Готов к приключениям?
            </p>
          </div>
          {/* Streak badge */}
          <div className="flex items-center gap-1.5 bg-white/15 backdrop-blur-md rounded-full px-3 py-1.5">
            <span className="text-lg">🔥</span>
            <span className="text-white font-bold text-[15px]">{displayUser.streak}</span>
          </div>
        </div>
        
        {/* Level Card */}
        <motion.div
          initial={{ scale: 0.95, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ delay: 0.1 }}
          className="bg-white/95 backdrop-blur-xl rounded-2xl p-5 shadow-xl"
        >
          <div className="flex items-center gap-4">
            {/* Level icon */}
            <div className="w-14 h-14 bg-gradient-to-br from-violet-500 to-indigo-600 rounded-2xl flex items-center justify-center text-3xl shadow-lg shrink-0">
              {currentLevel.emoji}
            </div>
            
            {/* Level info */}
            <div className="flex-1 min-w-0">
              <div className="flex items-center justify-between mb-2">
                <span className="font-bold text-gray-800 text-[17px] truncate">
                  Уровень {displayUser.level}
                </span>
                <span className="text-gray-400 text-sm font-medium">
                  {displayUser.xp} / {xpForNextLevel} XP
                </span>
              </div>
              {/* Progress bar */}
              <div className="h-2.5 bg-gray-100 rounded-full overflow-hidden">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: `${xpProgress}%` }}
                  transition={{ duration: 0.8, delay: 0.3 }}
                  className="h-full bg-gradient-to-r from-violet-500 to-indigo-500 rounded-full"
                />
              </div>
            </div>
          </div>
          
          {/* Stats row */}
          <div className="flex items-center gap-5 mt-4 pt-4 border-t border-gray-100">
            <div className="flex items-center gap-2">
              <span className="text-xl">⭐</span>
              <span className="font-bold text-gray-700 text-[16px]">{displayUser.xp}</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-xl">💎</span>
              <span className="font-bold text-gray-700 text-[16px]">{displayUser.gems}</span>
            </div>
          </div>
        </motion.div>
      </motion.div>
      
      {/* Quick Actions */}
      <motion.div
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="mb-6"
      >
        <div className="grid grid-cols-2 gap-3">
          <motion.button
            whileTap={{ scale: 0.96 }}
            onClick={handleQuickGame}
            className="bg-gradient-to-br from-violet-500 to-indigo-600 rounded-2xl p-5 text-white shadow-lg shadow-violet-500/25"
          >
            <div className="text-4xl mb-2">🎮</div>
            <div className="font-bold text-[17px]">Быстрая игра</div>
            <div className="text-white/70 text-sm mt-1">3 слова</div>
          </motion.button>
          <motion.button
            whileTap={{ scale: 0.96 }}
            onClick={() => navigate('/achievements')}
            className="bg-gradient-to-br from-amber-400 to-orange-500 rounded-2xl p-5 text-white shadow-lg shadow-amber-500/25"
          >
            <div className="text-4xl mb-2">🏆</div>
            <div className="font-bold text-[17px]">Достижения</div>
            <div className="text-white/70 text-sm mt-1">6 доступно</div>
          </motion.button>
        </div>
      </motion.div>
      
      {/* Categories */}
      <motion.div
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.25 }}
      >
        <h2 className="text-white font-bold text-[18px] mb-4">
          Выбери тему
        </h2>
        
        <div className="grid grid-cols-1 gap-3">
          {CATEGORIES.map((category, index) => (
            <motion.button
              key={category.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.35 + index * 0.1 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => handleCategorySelect(category.id)}
              className="w-full bg-white/95 backdrop-blur-xl rounded-2xl p-4 shadow-lg flex items-center gap-4 relative overflow-hidden group"
            >
              {/* Gradient accent */}
              <div className={`absolute left-0 top-0 bottom-0 w-1.5 bg-gradient-to-b ${category.color}`} />
              
              {/* Emoji icon */}
              <div className={`w-14 h-14 bg-gradient-to-br ${category.color} rounded-xl flex items-center justify-center text-2xl shadow-md shrink-0 group-hover:scale-110 transition-transform duration-300`}>
                {category.emoji}
              </div>
              
              {/* Text content */}
              <div className="flex-1 text-left">
                <div className="font-bold text-gray-800 text-[17px]">{category.name}</div>
                <div className="text-gray-400 text-sm flex items-center gap-2">
                  <span className="bg-gray-100 px-2 py-0.5 rounded-full text-xs font-medium">{category.words} слов</span>
                  <span>📚 Изучай</span>
                </div>
              </div>
              
              {/* Arrow */}
              <div className="text-gray-300 group-hover:text-gray-500 transition-colors">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M9 5l7 7-7 7" />
                </svg>
              </div>
            </motion.button>
          ))}
        </div>
      </motion.div>
      
      {/* Leaderboard Preview */}
      <motion.button
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.6 }}
        whileTap={{ scale: 0.98 }}
        onClick={() => navigate('/leaderboard')}
        className="w-full mt-6 bg-white/10 backdrop-blur-md rounded-2xl p-4 flex items-center justify-between border border-white/15"
      >
        <div className="flex items-center gap-3">
          <span className="text-2xl">👥</span>
          <span className="text-white font-semibold text-[16px]">Топ игроков</span>
        </div>
        <svg className="w-5 h-5 text-white/50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M9 5l7 7-7 7" />
        </svg>
      </motion.button>
      
      {/* Daily Reward */}
      <motion.div
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.7 }}
        className="mt-3"
      >
        <div className="bg-gradient-to-r from-emerald-400 to-teal-500 rounded-2xl p-4 flex items-center gap-4 shadow-lg shadow-emerald-500/25">
          <span className="text-4xl">🎁</span>
          <div className="flex-1">
            <div className="font-bold text-white text-[17px]">Ежедневная награда</div>
            <div className="text-white/80 text-sm">Забери +10⭐!</div>
          </div>
          <motion.button
            whileTap={{ scale: 0.95 }}
            onClick={() => vibrate('success')}
            className="bg-white text-emerald-600 font-bold px-5 py-2.5 rounded-xl text-[15px]"
          >
            Забрать
          </motion.button>
        </div>
      </motion.div>
    </div>
  )
}

export default Home