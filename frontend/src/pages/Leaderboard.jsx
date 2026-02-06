import React from 'react'
import { motion } from 'framer-motion'

// Демо-данные лидерборда
const DEMO_LEADERS = [
  { id: 1, name: 'Алиса', username: 'alisa', xp: 2450, streak: 15, level: 8 },
  { id: 2, name: 'Миша', username: 'misha', xp: 2100, streak: 12, level: 7 },
  { id: 3, name: 'Даша', username: 'dasha', xp: 1850, streak: 10, level: 6 },
  { id: 4, name: 'Костя', username: 'kostya', xp: 1600, streak: 8, level: 6 },
  { id: 5, name: 'Лиза', username: 'liza', xp: 1400, streak: 7, level: 5 },
  { id: 6, name: 'Саша', username: 'sasha', xp: 1200, streak: 5, level: 5 },
  { id: 7, name: 'Маша', username: 'masha', xp: 1000, streak: 4, level: 4 },
  { id: 8, name: 'Петя', username: 'petya', xp: 850, streak: 3, level: 4 },
  { id: 9, name: 'Ваня', username: 'vania', xp: 650, streak: 2, level: 3 },
  { id: 10, name: 'Ты', username: 'you', xp: 250, streak: 3, level: 3 },
]

// Уровни
const LEVELS = {
  3: { emoji: '🗺️' },
  4: { emoji: '📚' },
  5: { emoji: '🎒' },
  6: { emoji: '🤔' },
  7: { emoji: '👀' },
  8: { emoji: '💪' },
}

function Leaderboard() {
  const currentUserPlace = DEMO_LEADERS.findIndex(l => l.name === 'Ты') + 1
  
  return (
    <div className="pb-24 pt-4 px-4">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center mb-5"
      >
        <h1 className="text-[26px] font-extrabold text-white mb-2">
          Топ игроков
        </h1>
        <p className="text-white/70 text-[15px]">
          Соревнуйся с друзьями!
        </p>
      </motion.div>
      
      {/* Top 3 Podium */}
      <motion.div
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="flex items-end justify-center gap-3 mb-6"
      >
        {/* 2nd Place */}
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.2 }}
          className="text-center"
        >
          <div className="w-14 h-14 bg-gradient-to-br from-gray-300 to-gray-400 rounded-full flex items-center justify-center text-2xl mb-2 mx-auto shadow-lg">
            {LEVELS[DEMO_LEADERS[1].level]?.emoji || '🎒'}
          </div>
          <div className="bg-white/95 backdrop-blur-xl rounded-xl p-3 min-w-[75px] shadow-lg">
            <div className="font-bold text-gray-800 text-[14px]">{DEMO_LEADERS[1].name}</div>
            <div className="text-xs text-gray-400">{DEMO_LEADERS[1].xp} XP</div>
          </div>
          <div className="text-3xl mt-1">🥈</div>
        </motion.div>
        
        {/* 1st Place */}
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.15 }}
          className="text-center"
        >
          <div className="w-18 h-18 bg-gradient-to-br from-amber-400 to-yellow-500 rounded-full flex items-center justify-center text-[28px] mb-2 mx-auto shadow-xl shadow-amber-500/30">
            {LEVELS[DEMO_LEADERS[0].level]?.emoji || '🏆'}
          </div>
          <div className="bg-white/95 backdrop-blur-xl rounded-xl p-4 min-w-[90px] shadow-xl">
            <div className="font-bold text-gray-800 text-[15px]">{DEMO_LEADERS[0].name}</div>
            <div className="text-sm text-gray-400">{DEMO_LEADERS[0].xp} XP</div>
          </div>
          <div className="text-[36px] mt-1">🥇</div>
        </motion.div>
        
        {/* 3rd Place */}
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.25 }}
          className="text-center"
        >
          <div className="w-14 h-14 bg-gradient-to-br from-orange-400 to-orange-500 rounded-full flex items-center justify-center text-2xl mb-2 mx-auto shadow-lg">
            {LEVELS[DEMO_LEADERS[2].level]?.emoji || '🎒'}
          </div>
          <div className="bg-white/95 backdrop-blur-xl rounded-xl p-3 min-w-[75px] shadow-lg">
            <div className="font-bold text-gray-800 text-[14px]">{DEMO_LEADERS[2].name}</div>
            <div className="text-xs text-gray-400">{DEMO_LEADERS[2].xp} XP</div>
          </div>
          <div className="text-3xl mt-1">🥉</div>
        </motion.div>
      </motion.div>
      
      {/* Rest of the list */}
      <div className="space-y-2.5">
        {DEMO_LEADERS.slice(3).map((leader, index) => (
          <motion.div
            key={leader.id}
            initial={{ opacity: 0, x: -15 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.35 + index * 0.05 }}
            whileTap={{ scale: 0.98 }}
            className={`rounded-xl p-3.5 flex items-center gap-3 ${
              leader.name === 'Ты' 
                ? 'bg-violet-500/20 border-2 border-violet-500/40' 
                : 'bg-white/95 backdrop-blur-xl shadow-lg'
            }`}
          >
            <div className="w-7 text-center font-bold text-gray-400 text-[15px]">
              {index + 4}
            </div>
            
            <div className="w-12 h-12 bg-gradient-to-br from-violet-500/20 to-indigo-500/20 rounded-xl flex items-center justify-center text-xl">
              {LEVELS[leader.level]?.emoji || '🌱'}
            </div>
            
            <div className="flex-1 min-w-0">
              <div className="font-bold text-gray-800 text-[15px] truncate">
                {leader.name}
                {leader.name === 'Ты' && <span className="ml-2 text-violet-500">(ты)</span>}
              </div>
              <div className="flex items-center gap-2 text-sm text-gray-400">
                <span>🔥 {leader.streak}</span>
                <span>•</span>
                <span>ур. {leader.level}</span>
              </div>
            </div>
            
            <div className="text-right">
              <div className="font-bold text-violet-600 text-[16px]">{leader.xp}</div>
              <div className="text-xs text-gray-300">XP</div>
            </div>
          </motion.div>
        ))}
      </div>
      
      {/* Your Position */}
      <motion.div
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.8 }}
        className="mt-6 bg-white/95 backdrop-blur-xl rounded-2xl p-5 text-center shadow-lg"
      >
        <div className="text-gray-400 text-sm mb-1">Твоё место</div>
        <div className="text-[32px] font-extrabold text-violet-600">{currentUserPlace}</div>
        <div className="text-sm text-gray-300">из {DEMO_LEADERS.length}</div>
      </motion.div>
    </div>
  )
}

export default Leaderboard