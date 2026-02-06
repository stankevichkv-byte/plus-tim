import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { isTelegramWebApp } from '../api/telegram'
import { userAPI, lessonsAPI, achievementsAPI, leaderboardAPI, questsAPI } from '../api/client'

// ============ User Store ============
export const useUserStore = create(
  persist(
    (set, get) => ({
      user: null,
      isAuthenticated: false,
      isLoading: true,
      tg_id: null,
      
      // Инициализация пользователя
      initUser: async (tgId, username, firstName) => {
        set({ isLoading: true, tg_id: tgId })
        
        try {
          const response = await userAPI.createOrGet(tgId, username, firstName)
          set({
            user: response.data,
            isAuthenticated: true,
            isLoading: false
          })
          return response.data
        } catch (error) {
          console.error('User init error:', error)
          // Демо-режим при ошибке
          set({
            user: {
              id: Date.now(),
              tg_id: tgId,
              first_name: firstName,
              username,
              xp: 250,
              diamonds: 15,
              streak_days: 3,
              level: 3,
              xp_to_next_level: 100
            },
            isAuthenticated: true,
            isLoading: false
          })
        }
      },
      
      // Войти (старый метод для совместимости)
      authenticate: async () => {
        const { tg_id } = get()
        if (tg_id) {
          await get().initUser(tg_id, null, 'User')
        } else {
          // Демо-режим
          set({
            user: {
              id: 12345,
              tg_id: 12345,
              first_name: 'Test User',
              username: 'testuser',
              xp: 250,
              diamonds: 15,
              streak_days: 3,
              level: 3,
              xp_to_next_level: 100
            },
            isAuthenticated: true,
            isLoading: false
          })
        }
      },
      
      // Обновить данные пользователя
      updateUser: (updates) => {
        const currentUser = get().user
        if (currentUser) {
          set({ user: { ...currentUser, ...updates } })
        }
      },
      
      // Выйти
      logout: () => {
        localStorage.removeItem('plus-tim-user')
        set({ user: null, isAuthenticated: false, tg_id: null })
      }
    }),
    {
      name: 'plus-tim-user',
      partialize: (state) => ({ 
        user: state.user, 
        isAuthenticated: state.isAuthenticated,
        tg_id: state.tg_id
      })
    }
  )
)

// ============ Lesson Store ============
export const useLessonStore = create((set, get) => ({
  lessons: [],
  currentLesson: null,
  questions: [],
  currentQuestionIndex: 0,
  answers: {},
  isComplete: false,
  xpEarned: 0,
  isLoading: false,
  
  // Загрузить все уроки
  loadLessons: async (category = null) => {
    set({ isLoading: true })
    try {
      const response = await lessonsAPI.getAll(category)
      set({ lessons: response.data, isLoading: false })
    } catch (error) {
      console.error('Load lessons error:', error)
      // Демо-данные
      set({
        lessons: DEMO_LESSONS,
        isLoading: false
      })
    }
  },
  
  // Начать урок
  startLesson: async (lessonId) => {
    set({ isLoading: true })
    try {
      const response = await lessonsAPI.getQuestions(lessonId)
      set({
        currentLesson: lessonId,
        questions: response.data,
        currentQuestionIndex: 0,
        answers: {},
        isComplete: false,
        xpEarned: 0,
        isLoading: false
      })
      return response.data
    } catch (error) {
      console.error('Start lesson error:', error)
      set({ isLoading: false })
      return []
    }
  },
  
  // Следующий вопрос
  nextQuestion: () => {
    const { currentQuestionIndex, questions } = get()
    if (currentQuestionIndex < questions.length - 1) {
      set({ currentQuestionIndex: currentQuestionIndex + 1 })
    }
  },
  
  // Предыдущий вопрос
  prevQuestion: () => {
    const { currentQuestionIndex } = get()
    if (currentQuestionIndex > 0) {
      set({ currentQuestionIndex: currentQuestionIndex - 1 })
    }
  },
  
  // Записать ответ
  recordAnswer: (questionIndex, isCorrect) => {
    const { answers, xpEarned, questions } = get()
    const xp = isCorrect ? Math.floor(20 / questions.length) : 0
    set({
      answers: {
        ...answers,
        [questionIndex]: isCorrect
      },
      xpEarned: xpEarned + xp
    })
  },
  
  // Завершить урок (отправить на сервер)
  completeLesson: async () => {
    const { answers, questions, xpEarned, currentLesson } = get()
    const tg_id = useUserStore.getState().tg_id || 12345
    const correctCount = Object.values(answers).filter(a => a).length
    
    try {
      await userAPI.updateProgress(tg_id, currentLesson, {
        lesson_id: currentLesson,
        correct_answers: correctCount,
        total_questions: questions.length,
        xp_earned: xpEarned
      })
    } catch (error) {
      console.error('Complete lesson error:', error)
    }
    
    set({ isComplete: true })
    return { xpEarned, correctCount }
  },
  
  // Сбросить урок
  resetLesson: () => {
    set({
      currentLesson: null,
      questions: [],
      currentQuestionIndex: 0,
      answers: {},
      isComplete: false,
      xpEarned: 0
    })
  }
}))

// ============ Achievements Store ============
export const useAchievementsStore = create((set, get) => ({
  achievements: [],
  newUnlocked: null,
  
  // Загрузить достижения
  loadAchievements: async () => {
    const tg_id = useUserStore.getState().tg_id || 12345
    try {
      const response = await achievementsAPI.getAll(tg_id)
      set({ achievements: response.data })
    } catch (error) {
      console.error('Load achievements error:', error)
      // Демо-данные
      set({ achievements: DEMO_ACHIEVEMENTS })
    }
  },
  
  // Разблокировать достижение
  unlock: (achievement) => {
    const { achievements } = get()
    const existing = achievements.find(a => a.id === achievement.id)
    if (existing && !existing.unlocked) {
      achievement.unlocked = true
      set({
        achievements: achievements.map(a => 
          a.id === achievement.id ? { ...a, unlocked: true } : a
        ),
        newUnlocked: achievement
      })
    }
  },
  
  // Закрыть уведомление
  clearNewUnlocked: () => {
    set({ newUnlocked: null })
  }
}))

// ============ Leaderboard Store ============
export const useLeaderboardStore = create((set, get) => ({
  users: [],
  isLoading: false,
  
  // Загрузить лидерборд
  loadLeaderboard: async (limit = 10) => {
    set({ isLoading: true })
    try {
      const response = await leaderboardAPI.get(limit)
      set({ users: response.data, isLoading: false })
    } catch (error) {
      console.error('Load leaderboard error:', error)
      set({ users: DEMO_LEADERBOARD, isLoading: false })
    }
  }
}))

// ============ Daily Quests Store ============
export const useQuestsStore = create((set) => ({
  quests: [],
  
  // Загрузить задания
  loadQuests: async () => {
    const tg_id = useUserStore.getState().tg_id || 12345
    try {
      const response = await questsAPI.getDaily(tg_id)
      set({ quests: response.data })
    } catch (error) {
      console.error('Load quests error:', error)
    }
  },
  
  // Получить награду
  claimReward: async (questId) => {
    const tg_id = useUserStore.getState().tg_id || 12345
    try {
      const response = await questsAPI.claimReward(tg_id, questId)
      // Обновляем квесты
      set(state => ({
        quests: state.quests.map(q => 
          q.id === questId ? { ...q, completed: 2 } : q
        )
      }))
      return response.data
    } catch (error) {
      console.error('Claim reward error:', error)
      return null
    }
  }
}))

// ============ Demo Data ============
const DEMO_LESSONS = [
  { id: 1, title: 'Животные', category: 'animals', difficulty: 1, xp_reward: 15, order_num: 1 },
  { id: 2, title: 'Цвета', category: 'colors', difficulty: 1, xp_reward: 15, order_num: 2 },
  { id: 3, title: 'Еда', category: 'food', difficulty: 2, xp_reward: 20, order_num: 3 },
  { id: 4, title: 'Семья', category: 'family', difficulty: 2, xp_reward: 20, order_num: 4 },
  { id: 5, title: 'Время', category: 'time', difficulty: 3, xp_reward: 25, order_num: 5 },
]

const DEMO_ACHIEVEMENTS = [
  { id: 1, name: 'Первые шаги', description: 'Пройди первый урок', icon: '🎯', xp_reward: 50, unlocked: false },
  { id: 2, name: 'Любопытный', description: 'Пройди 5 уроков', icon: '📚', xp_reward: 100, unlocked: false },
  { id: 3, name: 'Неделю подряд', description: '7 дней подряд', icon: '🔥', xp_reward: 150, unlocked: false },
  { id: 4, name: 'Первый уровень', description: 'Достигни 2 уровня', icon: '⭐', xp_reward: 50, unlocked: true },
]

const DEMO_LEADERBOARD = [
  { tg_id: 1, first_name: 'Алиса', level: 12, xp: 2500, streak_days: 15 },
  { tg_id: 2, first_name: 'Борис', level: 10, xp: 2100, streak_days: 10 },
  { tg_id: 3, first_name: 'Вова', level: 8, xp: 1600, streak_days: 7 },
  { tg_id: 4, first_name: 'Галя', level: 7, xp: 1400, streak_days: 5 },
  { tg_id: 5, first_name: 'Дима', level: 5, xp: 900, streak_days: 3 },
]