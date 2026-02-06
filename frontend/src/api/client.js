import axios from 'axios'

// Конфигурация API (localhost для разработки)
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Создаём axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Interceptor для обработки ошибок
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message)
    return Promise.reject(error)
  }
)

// ============ API endpoints ============

// Пользователи
export const userAPI = {
  // Создать/получить пользователя ( tg_id передаётся в body)
  createOrGet: (tg_id, username, first_name) => 
    api.post('/api/users/', { tg_id, username, first_name }),
  
  // Получить пользователя по tg_id
  getByTgId: (tg_id) => api.get(`/api/users/${tg_id}`),
  
  // Обновить прогресс
  updateProgress: (tg_id, lessonId, result) => 
    api.post(`/api/quiz/${lessonId}/complete`, result, {
      params: { tg_id }
    })
}

// Уроки
export const lessonsAPI = {
  getAll: (category) => 
    api.get('/api/lessons/', { params: { category } }),
  
  getById: (id) => api.get(`/api/lessons/${id}`),
  
  getQuestions: (lessonId) => 
    api.get(`/api/lessons/${lessonId}/questions`),
  
  // Получить категории
  getCategories: () => 
    api.get('/api/lessons/').then(res => {
      const categories = [...new Set(res.data.map(l => l.category))]
      return categories
    })
}

// Достижения
export const achievementsAPI = {
  getAll: (tg_id) => api.get('/api/achievements/', { params: { tg_id } })
}

// Лидерборд
export const leaderboardAPI = {
  get: (limit = 10) => api.get('/api/leaderboard/', { params: { limit } })
}

// Ежедневные задания
export const questsAPI = {
  getDaily: (tg_id) => api.get(`/api/daily-quests/${tg_id}`),
  claimReward: (tg_id, questId) => 
    api.post(`/api/daily-quests/${tg_id}/${questId}/claim`)
}

// Telegram Auth (для production)
export const telegramAPI = {
  auth: (initData) => api.post('/api/telegram/auth', { init_data: initData })
}

export default api