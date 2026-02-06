import React from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import { motion } from 'framer-motion'

function NavigationBar({ active }) {
  const navigate = useNavigate()
  const location = useLocation()
  
  const items = [
    { path: '/', icon: '🏠', label: 'Главная', color: 'from-violet-500 to-indigo-500' },
    { path: '/profile', icon: '📚', label: 'Профиль', color: 'from-blue-500 to-cyan-500' },
    { path: '/achievements', icon: '🏆', label: 'Награды', color: 'from-amber-400 to-orange-500' },
    { path: '/leaderboard', icon: '👥', label: 'Топ', color: 'from-emerald-400 to-teal-500' },
  ]
  
  return (
    <div className="fixed bottom-0 left-0 right-0 pb-safe z-50">
      <div className="bg-white/95 backdrop-blur-xl border-t border-gray-200/50 px-2 py-2">
        <div className="flex items-center justify-around">
          {items.map((item) => {
            const isActive = location.pathname === item.path
            
            return (
              <button
                key={item.path}
                onClick={() => navigate(item.path)}
                className="relative flex flex-col items-center gap-1 px-3 py-2 rounded-xl transition-all"
              >
                <motion.div
                  animate={{
                    scale: isActive ? 1.15 : 1,
                    y: isActive ? -3 : 0
                  }}
                  className={`text-2xl transition-all ${isActive ? 'opacity-100' : 'opacity-50'}`}
                >
                  {item.icon}
                </motion.div>
                
                <span className={`text-[10px] font-bold ${
                  isActive 
                    ? 'bg-gradient-to-r bg-clip-text text-transparent ' + item.color 
                    : 'text-gray-400'
                }`}>
                  {item.label}
                </span>
                
                {isActive && (
                  <motion.div
                    layoutId="activeTab"
                    className={`absolute inset-0 bg-gradient-to-r ${item.color}/10 rounded-xl`}
                    transition={{ type: "spring", bounce: 0.2 }}
                  />
                )}
                
                {isActive && (
                  <motion.div
                    layoutId="activeDot"
                    className={`absolute -bottom-0.5 w-1 h-1 rounded-full bg-gradient-to-r ${item.color}`}
                    transition={{ type: "spring", bounce: 0.2 }}
                  />
                )}
              </button>
            )
          })}
        </div>
      </div>
      
      {/* Safe area padding for iPhone */}
      <div className="h-safe bg-white/95 backdrop-blur-xl" />
    </div>
  )
}

export default NavigationBar