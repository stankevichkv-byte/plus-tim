import React from 'react'
import { motion } from 'framer-motion'
import { useAchievementsStore } from '../store'

// Демо-достижения
const DEMO_ACHIEVEMENTS = [
  { id: 'first_lesson', name: 'Первый шаг', emoji: '✨', description: 'Завершить первый урок', xp: 50, unlocked: true },
  { id: 'streak_7', name: 'Неделя успеха', emoji: '🚀', description: '7 дней подряд', xp: 100, unlocked: true },
  { id: 'words_50', name: 'Большой словарь', emoji: '🧠', description: '50 слов', xp: 200, unlocked: false },
  { id: 'perfect', name: 'Идеально!', emoji: '💎', description: '10 правильных подряд', xp: 150, unlocked: true },
  { id: 'explorer', name: 'Исследователь', emoji: '🎯', description: 'Все типы заданий', xp: 100, unlocked: false },
  { id: 'streak_30', name: 'Месяц побед', emoji: '🏆', description: '30 дней подряд', xp: 300, unlocked: false },
]

function Achievements() {
  const { unlockedIds } = useAchievementsStore()
  const unlockedCount = DEMO_ACHIEVEMENTS.filter(a => a.unlocked).length
  
  return (
    <div className="pb-24 px-4">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center mb-6"
      >
        <h1 className="text-2xl font-bold text-white mb-2">🏆 Достижения</h1>
        <p className="text-white/80">
          {unlockedCount} из {DEMO_ACHIEVEMENTS.length} получено
        </p>
      </motion.div>
      
      {/* Progress */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white/90 backdrop-blur rounded-xl p-4 shadow-lg mb-6"
      >
        <div className="flex items-center justify-between mb-2">
          <span className="font-bold text-gray-800">Прогресс</span>
          <span className="text-sm text-gray-500">
            {Math.round((unlockedCount / DEMO_ACHIEVEMENTS.length) * 100)}%
          </span>
        </div>
        <div className="h-3 bg-gray-200 rounded-full overflow-hidden">
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${(unlockedCount / DEMO_ACHIEVEMENTS.length) * 100}%` }}
            transition={{ duration: 1 }}
            className="h-full bg-gradient-to-r from-yellow-400 to-orange-500 rounded-full"
          />
        </div>
      </motion.div>
      
      {/* Achievements Grid */}
      <div className="space-y-3">
        {DEMO_ACHIEVEMENTS.map((achievement, index) => (
          <motion.div
            key={achievement.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className={`rounded-xl p-4 shadow-lg ${
              achievement.unlocked 
                ? 'bg-white/90 backdrop-blur' 
                : 'bg-gray-100/50'
            }`}
          >
            <div className="flex items-center gap-4">
              <div className={`w-14 h-14 rounded-xl flex items-center justify-center text-2xl ${
                achievement.unlocked 
                  ? 'bg-gradient-to-br from-yellow-400 to-orange-500' 
                  : 'bg-gray-300 grayscale'
              }`}>
                {achievement.emoji}
              </div>
              
              <div className="flex-1">
                <div className="flex items-center gap-2">
                  <h3 className={`font-bold ${achievement.unlocked ? 'text-gray-800' : 'text-gray-400'}`}>
                    {achievement.name}
                  </h3>
                  {achievement.unlocked && (
                    <span className="text-xs bg-green-100 text-green-600 px-2 py-0.5 rounded-full">
                      ✓
                    </span>
                  )}
                </div>
                <p className={`text-sm ${achievement.unlocked ? 'text-gray-500' : 'text-gray-400'}`}>
                  {achievement.description}
                </p>
              </div>
              
              <div className={`text-right ${achievement.unlocked ? 'text-primary' : 'text-gray-400'}`}>
                <div className="font-bold">+{achievement.xp}</div>
                <div className="text-xs">⭐</div>
              </div>
            </div>
          </motion.div>
        ))}
      </div>
      
      {/* Locked hint */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1 }}
        className="text-center mt-6 text-white/60 text-sm"
      >
        Продолжай заниматься, чтобы разблокировать все достижения! 💪
      </motion.div>
    </div>
  )
}

export default Achievements