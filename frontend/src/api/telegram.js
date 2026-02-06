// Telegram WebApp SDK helper
import TelegramWebApp from '@twa-dev/sdk'

// Инициализация и проверка окружения
export function isTelegramWebApp() {
  return typeof window !== 'undefined' && TelegramWebApp.isInitialized
}

// Получить init данные
export function getInitData() {
  if (isTelegramWebApp()) {
    return TelegramWebApp.initData || ''
  }
  return ''
}

// Получить данные пользователя
export function getUserData() {
  if (isTelegramWebApp() && TelegramWebApp.initDataUnsafe?.user) {
    return TelegramWebApp.initDataUnsafe.user
  }
  return null
}

// Получить чат ID
export function getChatId() {
  if (isTelegramWebApp()) {
    return TelegramWebApp.initDataUnsafe?.chat?.id || 
           TelegramWebApp.initDataUnsafe?.user?.id
  }
  return null
}

// Показать главную кнопку
export function showMainButton(text, onClick) {
  if (isTelegramWebApp()) {
    TelegramWebApp.MainButton.text = text
    TelegramWebApp.MainButton.onClick = onClick
    TelegramWebApp.MainButton.show()
  }
}

// Скрыть главную кнопку
export function hideMainButton() {
  if (isTelegramWebApp()) {
    TelegramWebApp.MainButton.hide()
  }
}

// Показать кнопку "Назад"
export function showBackButton(onClick) {
  if (isTelegramWebApp()) {
    TelegramWebApp.BackButton.onClick = onClick
    TelegramWebApp.BackButton.show()
  }
}

// Скрыть кнопку "Назад"
export function hideBackButton() {
  if (isTelegramWebApp()) {
    TelegramWebApp.BackButton.hide()
  }
}

// Изменить тему
export function setTheme(theme) {
  if (isTelegramWebApp()) {
    TelegramWebApp.setHeaderColor(theme)
    TelegramWebApp.setBackgroundColor(theme)
  }
}

// Vibration
export function vibrate(type = 'light') {
  if (isTelegramWebApp() && TelegramWebApp.HapticFeedback) {
    switch (type) {
      case 'success':
        TelegramWebApp.HapticFeedback.notificationOccurred('success')
        break
      case 'error':
        TelegramWebApp.HapticFeedback.notificationOccurred('error')
        break
      case 'warning':
        TelegramWebApp.HapticFeedback.notificationOccurred('warning')
        break
      case 'impact':
        TelegramWebApp.HapticFeedback.impactOccurred('medium')
        break
      default:
        TelegramWebApp.HapticFeedback.impactOccurred('light')
    }
  }
}

// Скопировать текст
export function copyText(text) {
  if (isTelegramWebApp()) {
    TelegramWebApp.readTextFromClipboard(text)
  }
  navigator.clipboard.writeText(text)
}

// Открыть ссылку
export function openLink(url) {
  if (isTelegramWebApp()) {
    TelegramWebApp.openLink(url)
  } else {
    window.open(url, '_blank')
  }
}

// Закрыть WebApp
export function closeWebApp() {
  if (isTelegramWebApp()) {
    TelegramWebApp.close()
  }
}

// Получить цветовую схему
export function getColorScheme() {
  if (isTelegramWebApp()) {
    return TelegramWebApp.colorScheme || 'light'
  }
  return 'light'
}

// Настроить WebApp при загрузке
export function initWebApp(options = {}) {
  if (isTelegramWebApp()) {
    TelegramWebApp.ready()
    TelegramWebApp.expand()
    
    if (options.hideDefaultBack) {
      TelegramWebApp.BackButton.onClick(() => {
        window.history.back()
      })
    }
    
    // Обработка изменения темы
    if (options.onThemeChange) {
      TelegramWebApp.onEvent('themeChanged', options.onThemeChange)
    }
  }
}

export default {
  isTelegramWebApp,
  getInitData,
  getUserData,
  getChatId,
  showMainButton,
  hideMainButton,
  showBackButton,
  hideBackButton,
  setTheme,
  vibrate,
  copyText,
  openLink,
  closeWebApp,
  getColorScheme,
  initWebApp
}