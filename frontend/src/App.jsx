import React, { useEffect, useState } from 'react'
import { BrowserRouter, Routes, Route, useNavigate, useLocation } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import Confetti from 'react-confetti'
import { useUserStore, useAchievementsStore } from './store'

// Страницы
import Home from './pages/Home'
import Lesson from './pages/Lesson'
import Profile from './pages/Profile'
import Achievements from './pages/Achievements'
import Leaderboard from './pages/Leaderboard'

// Компоненты UI
import NavigationBar from './components/shared/NavigationBar'
import AchievementUnlock from './components/ui/AchievementUnlock'

// Telegram WebApp
import { initWebApp, hideBackButton, showBackButton, vibrate, getUserData } from './api/telegram'

// Loading Screen
function LoadingScreen() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500">
      <motion.div
        animate={{ rotate: 360 }}
        transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
        className="w-20 h-20 mb-6"
      >
        <div className="w-full h-full bg-white/20 backdrop-blur rounded-2xl flex items-center justify-center text-4xl">
          ⚡
        </div>
      </motion.div>
      <motion.p
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-white text-xl font-bold"
      >
        Загрузка PlusTim...
      </motion.p>
    </div>
  )
}

// Animated Routes
function AnimatedRoutes({ isAuthenticated }) {
  const location = useLocation()
  
  const pageVariants = {
    initial: { opacity: 0, x: 20 },
    animate: { opacity: 1, x: 0 },
    exit: { opacity: 0, x: -20 }
  }
  
  return (
    <AnimatePresence mode="wait">
      <Routes location={location} key={location.pathname}>
        <Route path="/" element={
          <motion.div
            variants={pageVariants}
            initial="initial"
            animate="animate"
            exit="exit"
            className="flex-1"
          >
            <Home />
          </motion.div>
        } />
        <Route path="/lesson/:category" element={
          <motion.div
            variants={pageVariants}
            initial="initial"
            animate="animate"
            exit="exit"
            className="flex-1"
          >
            <Lesson />
          </motion.div>
        } />
        <Route path="/profile" element={
          <motion.div
            variants={pageVariants}
            initial="initial"
            animate="animate"
            exit="exit"
            className="flex-1"
          >
            <Profile />
          </motion.div>
        } />
        <Route path="/achievements" element={
          <motion.div
            variants={pageVariants}
            initial="initial"
            animate="animate"
            exit="exit"
            className="flex-1"
          >
            <Achievements />
          </motion.div>
        } />
        <Route path="/leaderboard" element={
          <motion.div
            variants={pageVariants}
            initial="initial"
            animate="animate"
            exit="exit"
            className="flex-1"
          >
            <Leaderboard />
          </motion.div>
        } />
      </Routes>
    </AnimatePresence>
  )
}

// Main App Content
function AppContent() {
  const [showConfetti, setShowConfetti] = useState(false)
  const { initUser, isAuthenticated, isLoading, user } = useUserStore()
  const { newUnlocked, clearNewUnlocked } = useAchievementsStore()
  const [dimensions, setDimensions] = useState({ width: 0, height: 0 })
  
  useEffect(() => {
    // Инициализация Telegram WebApp
    initWebApp()
    
    // Получаем данные пользователя из Telegram
    const tgUser = getUserData()
    const tgId = tgUser?.id
    
    // Инициализация пользователя с tg_id
    if (tgId) {
      initUser(tgId, tgUser.username, tgUser.first_name)
    } else {
      // Демо-режим без Telegram
      initUser(12345, 'demo', 'Demo User')
    }
    
    // Размеры для confetti
    setDimensions({
      width: window.innerWidth,
      height: window.innerHeight
    })
    
    // Resize listener
    const handleResize = () => {
      setDimensions({
        width: window.innerWidth,
        height: window.innerHeight
      })
    }
    window.addEventListener('resize', handleResize)
    return () => window.removeEventListener('resize', handleResize)
  }, [])
  
  // Показать confetti при разблокировке достижения
  useEffect(() => {
    if (newUnlocked) {
      setShowConfetti(true)
      vibrate('success')
      setTimeout(() => {
        setShowConfetti(false)
      }, 5000)
    }
  }, [newUnlocked])
  
  // Navigation guard
  const navigate = useNavigate()
  const location = useLocation()
  
  useEffect(() => {
    // Показать кнопку назад если не на главной
    if (location.pathname !== '/') {
      showBackButton(() => {
        hideBackButton()
        navigate('/')
      })
    } else {
      hideBackButton()
    }
  }, [location.pathname])
  
  if (isLoading) {
    return <LoadingScreen />
  }
  
  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500">
      {/* Confetti */}
      {showConfetti && (
        <Confetti
          width={dimensions.width}
          height={dimensions.height}
          recycle={false}
          numberOfPieces={200}
          gravity={0.3}
        />
      )}
      
      {/* Achievement Unlock Popup */}
      <AnimatePresence>
        {newUnlocked && (
          <AchievementUnlock
            achievement={newUnlocked}
            onClose={() => {
              clearNewUnlocked()
              setShowConfetti(false)
            }}
          />
        )}
      </AnimatePresence>
      
      {/* Main Content */}
      <div className="min-h-screen flex flex-col">
        {/* Header Area (for non-lesson pages) */}
        {location.pathname !== '/lesson/:category' && (
          <div className="pt-4 px-4 pb-20">
            {/* Status bar placeholder */}
          </div>
        )}
        
        {/* Page Content */}
        <div className="flex-1">
          <AnimatedRoutes isAuthenticated={isAuthenticated} />
        </div>
        
        {/* Bottom Navigation */}
        {location.pathname !== '/lesson/:category' && (
          <NavigationBar active={location.pathname} />
        )}
      </div>
    </div>
  )
}

// Root App with Router
function App() {
  return (
    <BrowserRouter>
      <AppContent />
    </BrowserRouter>
  )
}

export default App