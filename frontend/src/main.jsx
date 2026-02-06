import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'

// Инициализация Telegram WebApp
import TelegramWebApp from '@twa-dev/sdk'

// Пытаемся инициализировать WebApp
try {
  TelegramWebApp.ready()
  TelegramWebApp.expand()
  console.log('Telegram WebApp initialized')
} catch (e) {
  console.log('Running outside Telegram or WebApp not available')
}

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)