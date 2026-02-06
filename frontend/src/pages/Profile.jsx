import React from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { useUserStore } from '../store'
import { getUserData } from '../api/telegram'

// Уровни
const LEVELS = {
  1: { name: 'Новичок', emoji: '🌱', xpNeeded: 0 },
  2: { name: 'Искатель', emoji: '🔍', xpNeeded: 100 },
  3: { name: 'Исследователь', emoji: '🗺️', xpNeeded: 250 },
  4: { name: 'Знаток', emoji: '📚', xpNeeded: 500 },
  5: { name: 'Ученик', emoji: '🎒', xpNeeded: 800 },
  6: { name: 'Любопытный', emoji: '🤔', xpNeeded: 1200 },
  7: { name: 'Внимательный', emoji: '👀', xpNeeded: 1600 },
  8: { name: 'Старательный', emoji: '💪', xpNeeded: 2100 },
  9: { name: 'Талант', emoji: '⭐', xpNeeded: 2700 },
  10: { name: 'Мастер', emoji: '🏆', xpNeeded: 3400 },
  11: { name: 'Эксперт', emoji: '🎓', xpNeeded: 4200 },
  12: { name: 'Профи', emoji: '💎', xpNeeded: 5100 },
  13: { name: 'Гений', emoji: '🧠', xpNeeded: 6100 },
  14: { name: 'Легенда', emoji: '👑', xpNeeded: 7200 },
  15: { name: 'Чемпион', emoji: '🏅', xpNeeded: 8400 },
}

function Profile() {
  const navigate = useNavigate()
  const { user } = useUserStore()
  
  const tgUser = getUserData()
  const displayUser = user || tgUser ? {
    first_name: user?.first_name || tgUser?.first_name || 'Друг',
    username: user?.username || tgUser?.username,
    xp: user?.xp || 250,
    gems: user?.gems || 15,
    streak: user?.streak || 3,
    level: user?.level || 3,
    lessons_completed: user?.lessons_completed || 5,
    words_learned: user?.words_learned || 23,
  } : { first_name: 'Друг', xp: 0, gems: 0, streak: 0, level: 1, lessons_completed: 0, words_learned: 0 }
  
  const currentLevel = LEVELS[displayUser.level] || LEVELS[1]
  const nextLevel = LEVELS[displayUser.level + 1]
  const xpForNext = nextLevel ? nextLevel.xpNeeded - displayUser.xp : displayUser.xp + 500
  const xpProgress = nextLevel 
    ? Math.min(((displayUser.xp - currentLevel.xpNeeded) / (nextLevel.xpNeeded - currentLevel.xpNeeded)) * 100, 100)
    : 100

  return (
    <div className="pb-24 pt-4 px-4">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-5"
      >
        <h1 className="text-[26px] font-extrabold text-white text-center mb-5">
          Мой профиль
        </h1>
        
        {/* Profile Card with Gradient */}
        <motion.div
          initial={{ scale: 0.95, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ delay: 0.1 }}
          className="relative bg-white/95 backdrop-blur-xl rounded-3xl p-6 shadow-xl overflow-hidden"
        >
          {/* Decorative circles */}
          <div className="absolute -top-10 -right-10 w-32 h-32 bg-gradient-to-br from-violet-400/20 to-indigo-500/20 rounded-full blur-2xl" />
          <div className="absolute -bottom-10 -left-10 w-24 h-24 bg-gradient-to-br from-pink-400/20 to-rose-500/20 rounded-full blur-2xl" />
          
          <div className="flex items-center gap-4 relative z-10">
            {/* Avatar with glow */}
            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-br from-violet-500 to-indigo-600 rounded-2xl blur-lg opacity-50" />
              <div className="relative w-16 h-16 bg-gradient-to-br from-violet-500 to-indigo-600 rounded-2xl flex items-center justify-center text-3xl shadow-lg shrink-0">
                {currentLevel.emoji}
              </div>
            </div>
            
            {/* User info */}
            <div className="flex-1 min-w-0">
              <div className="font-bold text-gray-800 text-[20px] truncate">
                {displayUser.first_name}
              </div>
              <div className="text-gray-400 text-sm">@{displayUser.username || 'unknown'}</div>
            </div>
            
            {/* Badge */}
            <div className="bg-gradient-to-r from-amber-400 to-orange-500 text-white text-xs font-bold px-3 py-1 rounded-full">
              Lv.{displayUser.level}
            </div>
          </div>
          
          {/* Level progress */}
          <div className="mt-5 bg-gray-50 rounded-xl p-4 relative z-10">
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center gap-2">
                <span className="text-lg">{currentLevel.emoji}</span>
                <span className="font-bold text-gray-800 text-[15px]">
                  {currentLevel.name}
                </span>
              </div>
              {nextLevel && (
                <span className="text-gray-400 text-sm flex items-center gap-1">
                  {nextLevel.emoji} +{xpForNext}
                </span>
              )}
            </div>
            <div className="h-3 bg-gray-200 rounded-full overflow-hidden">
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${xpProgress}%` }}
                transition={{ duration: 0.8, delay: 0.3 }}
                className="h-full bg-gradient-to-r from-violet-500 via-purple-500 to-indigo-500 rounded-full"
              />
            </div>
          </div>
        </motion.div>
      </motion.div>
      
      {/* Stats Grid */}
      <motion.div
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="grid grid-cols-2 gap-3 mb-5"
      >
        <motion.div
          whileHover={{ scale: 1.02 }}
          className="bg-white/95 backdrop-blur-xl rounded-2xl p-4 shadow-lg relative overflow-hidden"
        >
          <div className="absolute top-0 right-0 w-16 h-16 bg-amber-400/10 rounded-full blur-xl" />
          <div className="text-3xl mb-1 relative z-10">⭐</div>
          <div className="text-2xl font-bold text-gray-800 relative z-10">{displayUser.xp}</div>
          <div className="text-sm text-gray-400 relative z-10">Всего звёзд</div>
        </motion.div>
        
        <motion.div
          whileHover={{ scale: 1.02 }}
          className="bg-white/95 backdrop-blur-xl rounded-2xl p-4 shadow-lg relative overflow-hidden"
        >
          <div className="absolute top-0 right-0 w-16 h-16 bg-cyan-400/10 rounded-full blur-xl" />
          <div className="text-3xl mb-1 relative z-10">💎</div>
          <div className="text-2xl font-bold text-gray-800 relative z-10">{displayUser.gems}</div>
          <div className="text-sm text-gray-400 relative z-10">Кристаллов</div>
        </motion.div>
        
        <motion.div
          whileHover={{ scale: 1.02 }}
          className="bg-white/95 backdrop-blur-xl rounded-2xl p-4 shadow-lg relative overflow-hidden"
        >
          <div className="absolute top-0 right-0 w-16 h-16 bg-orange-400/10 rounded-full blur-xl" />
          <div className="text-3xl mb-1 relative z-10">🔥</div>
          <div className="text-2xl font-bold text-gray-800 relative z-10">{displayUser.streak}</div>
          <div className="text-sm text-gray-400 relative z-10">Дней подряд</div>
        </motion.div>
        
        <motion.div
          whileHover={{ scale: 1.02 }}
          className="bg-white/95 backdrop-blur-xl rounded-2xl p-4 shadow-lg relative overflow-hidden"
        >
          <div className="absolute top-0 right-0 w-16 h-16 bg-emerald-400/10 rounded-full blur-xl" />
          <div className="text-3xl mb-1 relative z-10">📖</div>
          <div className="text-2xl font-bold text-gray-800 relative z-10">{displayUser.lessons_completed}</div>
          <div className="text-sm text-gray-400 relative z-10">Уроков</div>
        </motion.div>
      </motion.div>
      
      {/* Words Learned Card */}
      <motion.div
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.25 }}
        className="bg-white/95 backdrop-blur-xl rounded-2xl p-5 shadow-lg mb-5"
      >
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2">
            <span className="text-xl">📚</span>
            <h3 className="font-bold text-gray-800 text-[16px]">Словарь</h3>
          </div>
          <span className="bg-gray-100 text-gray-600 text-sm font-medium px-3 py-1 rounded-full">{displayUser.words_learned} слов</span>
        </div>
        <div className="h-3 bg-gray-100 rounded-full overflow-hidden">
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${Math.min(displayUser.words_learned, 100)}%` }}
            transition={{ duration: 0.8, delay: 0.4 }}
            className="h-full bg-gradient-to-r from-emerald-400 via-teal-500 to-cyan-500 rounded-full"
          />
        </div>
        <div className="flex justify-between text-xs text-gray-300 mt-2">
          <span>0</span>
          <span>50</span>
          <span>100</span>
        </div>
      </motion.div>
      
      {/* Achievements Preview */}
      <motion.button
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        whileTap={{ scale: 0.98 }}
        onClick={() => navigate('/achievements')}
        className="w-full bg-white/95 backdrop-blur-xl rounded-2xl p-4 shadow-lg flex items-center justify-between relative overflow-hidden"
      >
        <div className="absolute top-0 right-0 w-24 h-24 bg-amber-400/10 rounded-full blur-xl" />
        <div className="flex items-center gap-3 relative z-10">
          <span className="text-3xl">🏆</span>
          <div className="text-left">
            <div className="font-bold text-gray-800 text-[16px]">Достижения</div>
            <div className="text-sm text-gray-400">3 из 6 получено</div>
          </div>
        </div>
        <div className="bg-gray-100 p-2 rounded-xl relative z-10">
          <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M9 5l7 7-7 7" />
          </svg>
        </div>
      </motion.button>
    </div>
  )
}

export default Profile