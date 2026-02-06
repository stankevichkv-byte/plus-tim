import React, { useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import Confetti from 'react-confetti'

function AchievementUnlock({ achievement, onClose }) {
  // Автоматически закрыть через 5 секунд
  useEffect(() => {
    const timer = setTimeout(onClose, 5000)
    return () => clearTimeout(timer)
  }, [onClose])
  
  return (
    <div className="fixed inset-0 bg-black/60 flex items-center justify-center z-50 p-4">
      {/* Confetti */}
      <Confetti
        width={window.innerWidth}
        height={window.innerHeight}
        recycle={false}
        numberOfPieces={300}
        gravity={0.3}
        colors={['#F59E0B', '#FBBF24', '#6366F1', '#818CF8', '#10B981']}
      />
      
      <motion.div
        initial={{ scale: 0, rotate: -180 }}
        animate={{ scale: 1, rotate: 0 }}
        exit={{ scale: 0, rotate: 180 }}
        transition={{ type: "spring", bounce: 0.5 }}
        className="bg-white rounded-3xl p-8 shadow-2xl max-w-sm w-full text-center relative overflow-hidden"
      >
        {/* Background glow */}
        <motion.div
          animate={{
            scale: [1, 1.2, 1],
            opacity: [0.3, 0.5, 0.3]
          }}
          transition={{ duration: 2, repeat: Infinity }}
          className="absolute inset-0 bg-gradient-to-br from-yellow-400/20 to-orange-500/20"
        />
        
        {/* Content */}
        <div className="relative z-10">
          <motion.div
            animate={{ rotate: [0, 10, -10, 0] }}
            transition={{ duration: 1, repeat: Infinity, repeatDelay: 2 }}
            className="text-7xl mb-4"
          >
            {achievement.emoji}
          </motion.div>
          
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="mb-2"
          >
            <span className="text-sm text-gray-400 uppercase tracking-wider">
              Достижение!
            </span>
          </motion.div>
          
          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="text-2xl font-bold text-gray-800 mb-2"
          >
            {achievement.name}
          </motion.h2>
          
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5 }}
            className="text-gray-500 mb-4"
          >
            {achievement.description}
          </motion.p>
          
          {/* Rewards */}
          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.6 }}
            className="flex justify-center gap-4 mb-6"
          >
            <div className="bg-primary/10 rounded-xl px-4 py-2">
              <span className="text-xl mr-1">⭐</span>
              <span className="font-bold text-primary text-lg">+{achievement.xp}</span>
            </div>
            <div className="bg-secondary/10 rounded-xl px-4 py-2">
              <span className="text-xl mr-1">💎</span>
              <span className="font-bold text-secondary text-lg">+{achievement.gems || 10}</span>
            </div>
          </motion.div>
          
          {/* Close button */}
          <motion.button
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.7 }}
            onClick={onClose}
            className="w-full bg-gradient-to-r from-primary to-primary-light text-white font-bold py-3 rounded-xl shadow-lg active:scale-95 transition-transform"
          >
            Круто! 🎉
          </motion.button>
        </div>
      </motion.div>
    </div>
  )
}

export default AchievementUnlock