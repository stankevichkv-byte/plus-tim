# 📋 Детальный план: Telegram Web App для PlusTim

## 🎯 Цель проекта
Создать полноценное веб-приложение внутри Telegram с нативным интерфейсом (как отдельное приложение) для изучения английского языка детьми 8-10 лет.

---

## 📁 Структура проекта

```
plus_tim/
├── bot/                       # Существующий Telegram-бот (aiogram 3.x)
│   ├── main.py
│   ├── handlers.py
│   ├── keyboards.py
│   ├── database.py
│   ├── config.py
│   ├── content.py
│   └── .env
│
├── backend/                   # FastAPI бэкенд (API для Web App)
│   ├── main.py               # Точка входа
│   ├── api/
│   │   ├── __init__.py
│   │   ├── telegram.py       # Аутентификация через Telegram
│   │   ├── users.py          # API пользователей
│   │   ├── lessons.py        # API уроков
│   │   ├── words.py          # API слов
│   │   ├── achievements.py   # API достижений
│   │   └── games.py          # API мини-игр
│   ├── models/
│   │   ├── __init__.py
│   │   ├── pydantic_models.py # Pydantic модели
│   │   └── database.py       # Работа с БД
│   └── requirements.txt
│
└── frontend/                  # React приложение
    ├── public/
    │   └── favicon.ico
    ├── src/
    │   ├── api/
    │   │   ├── client.js      # API клиент
    │   │   └── telegram.js    # Telegram WebApp SDK
    │   ├── components/
    │   │   ├── App.jsx        # Главное приложение
    │   │   ├── App.css
    │   │   ├── pages/
    │   │   │   ├── Home.jsx          # Главное меню
    │   │   │   ├── Home.css
    │   │   │   ├── Lesson.jsx        # Урок
    │   │   │   ├── Lesson.css
    │   │   │   ├── Profile.jsx      # Профиль
    │   │   │   ├── Profile.css
    │   │   │   ├── Achievements.jsx # Достижения
    │   │   │   ├── Achievements.css
    │   │   │   ├── Leaderboard.jsx  # Топ игроков
    │   │   │   └── Leaderboard.css
    │   │   ├── games/
    │   │   │   ├── QuizGame.jsx     # Угадай по картинке
    │   │   │   ├── QuizGame.css
    │   │   │   ├── MissingLetter.jsx # Пропавшая буква
    │   │   │   └── MissingLetter.css
    │   │   │   └── SpeedRound.jsx    # Скоростной раунд
    │   │   │   └── SpeedRound.css
    │   │   ├── ui/
    │   │   │   ├── Button.jsx
    │   │   │   ├── Button.css
    │   │   │   ├── Card.jsx
    │   │   │   ├── Card.css
    │   │   │   ├── ProgressBar.jsx
    │   │   │   ├── ProgressBar.css
    │   │   │   ├── LevelBadge.jsx
    │   │   │   └── LevelBadge.css
    │   │   │   ├── XPProgress.jsx
    │   │   │   └── XPProgress.css
    │   │   │   ├── AchievementCard.jsx
    │   │   │   └── AchievementCard.css
    │   │   │   └── StatsCard.jsx
    │   │   │   └── StatsCard.css
    │   │   └── shared/
    │   │       ├── Header.jsx
    │   │       ├── Header.css
    │   │       ├── Footer.jsx
    │   │       └── Footer.css
    │   ├── hooks/
    │   │   ├── useAuth.js      # Хук аутентификации
    │   │   ├── useUser.js      # Хук данных пользователя
    │   │   ├── useLesson.js    # Хук урока
    │   │   └── useAnimations.js # Хук анимаций
    │   ├── utils/
    │   │   ├── animations.js   # Функции анимаций
    │   │   ├── sounds.js       # Звуковые эффекты
    │   │   └── helpers.js      # Вспомогательные функции
    │   ├── styles/
    │   │   ├── theme.css       # Тема оформления
    │   │   └── variables.css   # CSS переменные
    │   ├── store/
    │   │   ├── index.js        # Глобальное состояние
    │   │   └── slices/
    │   │       ├── userSlice.js
    │   │       ├── lessonSlice.js
    │   │       └── gameSlice.js
    │   ├── App.jsx
    │   ├── main.jsx
    │   └── index.css
    ├── index.html
    ├── package.json
    ├── vite.config.js
    └── tailwind.config.js
```

---

## 🎨 Дизайн-система

### Цветовая палитра (детская, яркая)

```css
:root {
  /* Основные цвета */
  --primary: #6366F1;        /* Indigo */
  --primary-light: #818CF8;
  --primary-dark: #4F46E5;
  
  --secondary: #F59E0B;      /* Amber */
  --secondary-light: #FBBF24;
  --secondary-dark: #D97706;
  
  --success: #10B981;        /* Emerald */
  --success-light: #34D399;
  
  --warning: #F97316;        /* Orange */
  --error: #EF4444;          /* Red */
  
  /* Нейтральные */
  --bg-primary: #FFFFFF;
  --bg-secondary: #F3F4F6;
  --bg-card: #FFFFFF;
  
  --text-primary: #1F2937;
  --text-secondary: #6B7280;
  --text-muted: #9CA3AF;
  
  /* Градиенты */
  --gradient-primary: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
  --gradient-success: linear-gradient(135deg, #10B981 0%, #34D399 100%);
  --gradient-gold: linear-gradient(135deg, #F59E0B 0%, #FBBF24 100%);
  
  /* Тени */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
  
  /* Скругления */
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --radius-xl: 24px;
  --radius-full: 9999px;
  
  /* Анимации */
  --transition-fast: 150ms ease;
  --transition-normal: 300ms ease;
  --transition-slow: 500ms ease;
}
```

### Типографика

```css
:root {
  --font-primary: 'Nunito', -apple-system, BlinkMacSystemFont, sans-serif;
  
  --text-xs: 12px;
  --text-sm: 14px;
  --text-base: 16px;
  --text-lg: 18px;
  --text-xl: 20px;
  --text-2xl: 24px;
  --text-3xl: 30px;
  --text-4xl: 36px;
  
  --font-normal: 400;
  --font-medium: 600;
  --font-bold: 700;
}
```

---

## 📊 База данных (расширенная)

### Таблица `users` (обновлённая)
```sql
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    first_name TEXT,
    xp INTEGER DEFAULT 0,
    gems INTEGER DEFAULT 0,
    streak INTEGER DEFAULT 0,
    level INTEGER DEFAULT 1,
    lessons_completed INTEGER DEFAULT 0,
    words_learned INTEGER DEFAULT 0,
    last_activity DATE,
    daily_reward_claimed BOOLEAN DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Таблица `daily_rewards`
```sql
CREATE TABLE daily_rewards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    reward_day INTEGER,
    xp_reward INTEGER DEFAULT 0,
    gems_reward INTEGER DEFAULT 0,
    claimed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    UNIQUE(user_id, reward_day)
);
```

### Таблица `user_word_progress`
```sql
CREATE TABLE user_word_progress (
    user_id INTEGER,
    word_id INTEGER,
    correct_count INTEGER DEFAULT 0,
    wrong_count INTEGER DEFAULT 0,
    mastered BOOLEAN DEFAULT 0,
    last_practice DATE,
    next_review DATE,
    PRIMARY KEY (user_id, word_id)
);
```

---

## 🔌 API Endpoints

### Аутентификация
```
POST /api/telegram/auth    # Аутентификация через Telegram WebApp
GET  /api/telegram/init    # Получить init данные для WebApp
```

### Пользователи
```
GET  /api/users/me         # Получить текущего пользователя
PUT  /api/users/me         # Обновить профиль
GET  /api/users/{id}       # Получить пользователя по ID
GET  /api/users/leaderboard # Топ игроков
POST /api/users/daily-reward # Получить ежедневную награду
```

### Уроки
```
GET  /api/lessons          # Список уроков
GET  /api/lessons/{id}     # Урок по ID
POST /api/lessons/start    # Начать урок
POST /api/lessons/{id}/complete # Завершить урок
GET  /api/lessons/progress # Прогресс уроков
```

### Слова
```
GET  /api/words            # Список слов (с фильтрами)
GET  /api/words/{id}      # Слово по ID
GET  /api/words/categories # Категории слов
GET  /api/words/random    # Случайные слова
```

### Достижения
```
GET  /api/achievements     # Все достижения
GET  /api/achievements/mine # Мои достижения
POST /api/achievements/claim # Получить достижение
```

### Мини-игры
```
POST /api/games/quiz       # Ответ в викторине
POST /api/games/missing-letter # Ответ в "Пропавшая буква"
POST /api/games/speed-round # Ответ в скоростном раунде
GET  /api/games/stats      # Статистика игр
```

---

## 🎮 Компоненты React

### App.jsx (Роутинг)
```jsx
// Главный компонент с роутингом
function App() {
  return (
    <TelegramProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/lesson/:id" element={<Lesson />} />
          <Route path="/lesson/:id/start" element={<LessonStart />} />
          <Route path="/lesson/:id/discovery" element={<Discovery />} />
          <Route path="/lesson/:id/quiz" element={<QuizGame />} />
          <Route path="/lesson/:id/missing-letter" element={<MissingLetter />} />
          <Route path="/lesson/:id/speed" element={<SpeedRound />} />
          <Route path="/lesson/:id/complete" element={<LessonComplete />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/achievements" element={<Achievements />} />
          <Route path="/leaderboard" element={<Leaderboard />} />
          <Route path="/daily-reward" element={<DailyReward />} />
        </Routes>
      </Router>
    </TelegramProvider>
  );
}
```

### Home.jsx (Главное меню)
```jsx
function Home() {
  return (
    <div className="home">
      <Header user={user} />
      
      <WelcomeBanner 
        user={user} 
        streak={streak}
        onClaimDaily={claimDailyReward}
      />
      
      <LevelProgress level={level} xp={xp} nextLevelXP={nextLevelXP} />
      
      <QuickActions>
        <ActionCard
          icon="🎮"
          title="Урок"
          description="Изучай новые слова"
          onClick={() => navigate('/lesson')}
        />
        <ActionCard
          icon="⚡"
          title="Быстрая игра"
          onClick={() => navigate('/game/quick')}
        />
        <ActionCard
          icon="📚"
          title="Повторение"
          onClick={() => navigate('/review')}
        />
      </QuickActions>
      
      <StatsOverview stats={stats} />
      
      <RecentAchievements achievements={recentAchievements} />
      
      <NavigationBar active="home" />
    </div>
  );
}
```

### Lesson.jsx (Структура урока)
```jsx
function Lesson() {
  const [step, setStep] = useState('intro'); // intro, discovery, quiz, missing, speed, complete
  
  return (
    <div className="lesson">
      <LessonProgressBar current={step} total={5} />
      
      {step === 'intro' && <LessonIntro words={words} onStart={startLesson} />}
      {step === 'discovery' && <DiscoveryBlock word={currentWord} onComplete={nextWord} />}
      {step === 'quiz' && <QuizGame words={words} onComplete={nextBlock} />}
      {step === 'missing' && <MissingLetter words={words} onComplete={nextBlock} />}
      {step === 'speed' && <SpeedRound words={words} onComplete={finishLesson} />}
      {step === 'complete' && <LessonComplete results={results} onContinue={continueAction} />}
    </div>
  );
}
```

---

## 🎨 Анимации

### Framer Motion компоненты
```jsx
// Анимация появления карточки слова
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  exit={{ opacity: 0, y: -20 }}
  transition={{ type: "spring", bounce: 0.3 }}
>
  <WordCard word={word} />
</motion.div>

// Анимация правильного ответа
<motion.div
  initial={{ scale: 0.8, rotate: -10 }}
  animate={{ scale: 1.1, rotate: 0 }}
  className="correct-answer"
>
  🎉
</motion.div>

// Прогресс-бар с анимацией
<motion.div
  className="progress-fill"
  initial={{ width: 0 }}
  animate={{ width: `${progress}%` }}
  transition={{ duration: 0.5 }}
/>
```

### Confetti эффект при достижениях
```jsx
import Confetti from 'react-confetti';

function AchievementUnlock({ achievement, onComplete }) {
  return (
    <div className="achievement-unlock">
      <Confetti />
      <motion.div
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        className="achievement-popup"
      >
        <span className="emoji">{achievement.emoji}</span>
        <h2>{achievement.name}</h2>
        <p>+{achievement.xp} XP, +{achievement.gems} 💎</p>
        <Button onClick={onComplete}>Продолжить</Button>
      </motion.div>
    </div>
  );
}
```

---

## 🔐 Аутентификация Telegram WebApp

```javascript
// api/telegram.js
import TelegramWebApp from '@twa-dev/sdk';

export function verifyTelegramAuth(initData) {
  // Проверка подписи Telegram
  const hash = initData.hash;
  const dataCheckString = initData_data
    .split('\n')
    .filter(k => k[0] !== 'hash')
    .sort()
    .join('\n');
  
  // Верификация через WebApp API
  return TelegramWebApp.initDataUnsafe.hash;
}

export async function authenticateUser(initData) {
  const response = await api.post('/telegram/auth', {
    init_data: initData
  });
  
  if (response.success) {
    localStorage.setItem('token', response.token);
    return response.user;
  }
  
  throw new Error('Аутентификация не удалась');
}
```

---

## 📦 Зависимости

### Frontend
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "@twa-dev/sdk": "^6.9.0",
    "axios": "^1.6.0",
    "framer-motion": "^10.16.0",
    "react-confetti": "^6.1.0",
    "zustand": "^4.4.0",
    "clsx": "^2.0.0",
    "lucide-react": "^0.294.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.2.0",
    "vite": "^5.0.0",
    "tailwindcss": "^3.3.0",
    "autoprefixer": "^10.4.0"
  }
}
```

### Backend
```
fastapi==0.109.0
uvicorn[standard]==0.27.0
aiogram==3.4.0
aiosqlite==0.19.0
python-telegram-bot==20.7.0
python-dotenv==1.0.0
pydantic==2.5.0
websockets==12.0
```

---

## 🚀 Этапы реализации

### Этап 1: Инфраструктура (1-2 дня)
- [ ] Создать структуру папок
- [ ] Настроить React + Vite
- [ ] Установить зависимости
- [ ] Настроить TailwindCSS
- [ ] Создать FastAPI бэкенд
- [ ] Настроить CORS

### Этап 2: Telegram WebApp SDK (0.5 дня)
- [ ] Подключить @twa-dev/sdk
- [ ] Настроить инициализацию
- [ ] Создать провайдер контекста
- [ ] Обработать тему (светлая/тёмная)

### Этап 3: API бэкенд (2-3 дня)
- [ ] Создать Pydantic модели
- [ ] Реализовать аутентификацию Telegram
- [ ] Создать endpoints для пользователей
- [ ] Создать endpoints для уроков
- [ ] Создать endpoints для достижений
- [ ] Добавить CORS

### Этап 4: Главное меню (1-2 дня)
- [ ] Создать компонент Header
- [ ] Создать компонент WelcomeBanner
- [ ] Создать компонент LevelProgress
- [ ] Создать компонент QuickActions
- [ ] Создать компонент StatsOverview
- [ ] Создать компонент NavigationBar
- [ ] Сверстать Home.jsx

### Этап 5: Экран урока (2-3 дня)
- [ ] Создать компонент LessonProgressBar
- [ ] Создать компонент LessonIntro
- [ ] Создать компонент DiscoveryBlock
- [ ] Создать компонент WordCard
- [ ] Создать компонент AudioPlayer
- [ ] Сверстать Lesson.jsx

### Этап 6: Мини-игры (3-4 дня)
- [ ] QuizGame (викторина с картинками)
- [ ] MissingLetter (пропавшая буква)
- [ ] SpeedRound (скоростной раунд с таймером)
- [ ] Добавить анимации ответов
- [ ] Добавить звуковые эффекты

### Этап 7: Профиль (1-2 дня)
- [ ] Создать компонент ProfileHeader
- [ ] Создать компонент LevelBadge
- [ ] Создать компонент XPProgress
- [ ] Создать компонент StatsGrid
- [ ] Сверстать Profile.jsx

### Этап 8: Достижения (1 день)
- [ ] Создать компонент AchievementCard
- [ ] Создать компонент AchievementGrid
- [ ] Реализовать модалку нового достижения
- [ ] Добавить анимацию confetti
- [ ] Сверстать Achievements.jsx

### Этап 9: Интеграция с ботом (1-2 дня)
- [ ] Добавить кнопку "Открыть приложение" в бота
- [ ] Связать Web App с ботом через BOT_TOKEN
- [ ] Синхронизировать данные
- [ ] Тестирование

---

## 📈 Метрики и аналитика

```javascript
// Отслеживание событий
function trackEvent(eventName, params) {
  // Google Analytics / Telegram Analytics
  console.log('Track:', eventName, params);
}

// Использование
trackEvent('lesson_started', { category: 'animals', wordCount: 3 });
trackEvent('quiz_correct', { time: 2.5, streak: 5 });
trackEvent('achievement_unlocked', { achievement: 'streak_7' });
trackEvent('level_up', { oldLevel: 5, newLevel: 6 });
```

---

## 🧪 Тестирование

```javascript
// Jest тесты
describe('Lesson', () => {
  test('должен показать экран урока', () => {
    render(<Lesson words={sampleWords} />);
    expect(screen.getByText('Новый урок!')).toBeInTheDocument();
  });
  
  test('должен перейти к следующему слову', () => {
    render(<Discovery word={sampleWord} />);
    fireEvent.click(screen.getByText('Дальше'));
    expect(mockOnComplete).toHaveBeenCalled();
  });
});
```

---

## 📱 Адаптивность

```css
/* Mobile-first */
.container {
  max-width: 480px; /* Telegram Web App width */
  margin: 0 auto;
  padding: 16px;
}

/* Tablet */
@media (min-width: 768px) {
  .container {
    max-width: 600px;
  }
}

/* Desktop (если открыть в браузере) */
@media (min-width: 1024px) {
  .container {
    max-width: 480px; /* Сохраняем мобильный вид */
  }
}
```

---

## 🔄 CI/CD

```yaml
# GitHub Actions
name: Deploy Web App

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Install dependencies
        run: cd frontend && npm ci
        
      - name: Build
        run: npm run build
        
      - name: Deploy to Render
        run: echo "Deploying..."
```

---

## 📝 Чек-лист перед запуском

- [ ] Все API endpoints протестированы
- [ ] Аутентификация работает
- [ ] UI адаптирован под мобильные
- [ ] Анимации плавные
- [ ] Звуковые эффекты добавлены
- [ ] Confetti при достижениях
- [ ] Обработка ошибок
- [ ] Loading states
- [ ] Pull-to-refresh работает
- [ ] Свайп назад работает
- [ ] Тёмная тема Telegram учитывается

---

*Дата создания: 06.02.2026*
*Версия: 1.0*