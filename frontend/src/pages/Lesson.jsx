import React, { useState, useEffect, useRef } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import { useLessonStore, useUserStore } from '../store'
import { vibrate } from '../api/telegram'

// API URL - настройте для вашего окружения
const API_URL = import.meta.env.VITE_API_URL || ''

// Компонент: AudioButton с TTS озвучкой
function AudioButton({ word }) {
  const [loading, setLoading] = useState(false)
  const audioRef = useRef(null)
  
  const playAudio = async () => {
    if (!word) return
    
    vibrate('impact')
    setLoading(true)
    
    try {
      // Сначала пробуем API TTS
      if (API_URL) {
        const response = await fetch(`${API_URL}/api/tts/${word}`)
        if (response.ok) {
          const blob = await response.blob()
          const url = URL.createObjectURL(blob)
          const audio = new Audio(url)
          audio.play()
          audio.onended = () => {
            setLoading(false)
            URL.revokeObjectURL(url)
          }
          audio.onerror = () => {
            // fallback на browser TTS
            playBrowserTTS()
          }
          return
        }
      }
      // Fallback на browser TTS
      playBrowserTTS()
    } catch (error) {
      console.error('TTS error:', error)
      playBrowserTTS()
    }
  }
  
  const playBrowserTTS = () => {
    const utterance = new SpeechSynthesisUtterance(word)
    utterance.lang = 'en-US'
    utterance.rate = 0.9
    speechSynthesis.speak(utterance)
    setLoading(false)
  }
  
  return (
    <button
      onClick={playAudio}
      disabled={loading || !word}
      className={`w-full bg-gradient-to-r from-primary to-primary-light text-white font-bold py-3 rounded-xl flex items-center justify-center gap-2 transition-all ${
        loading ? 'opacity-50 cursor-not-allowed' : 'active:scale-95'
      }`}
    >
      {loading ? (
        <>
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
            className="w-5 h-5 border-2 border-white border-t-transparent rounded-full"
          />
          <span>Загрузка...</span>
        </>
      ) : (
        <>
          <span>🔊</span>
          <span>Послушать произношение</span>
        </>
      )}
    </button>
  )
}

// Шаги урока
const LESSON_STEPS = {
  INTRO: 'intro',
  DISCOVERY: 'discovery',
  QUIZ: 'quiz',
  MISSING_LETTER: 'missing_letter',
  SPEED_ROUND: 'speed',
  COMPLETE: 'complete'
}

// Демо-слова для разных категорий
const DEMO_WORDS = {
  animals: [
    { id: 1, word: 'cat', translation: 'кот', emoji: '🐱', transcription: '[kæt]', example: 'The cat is sleeping.' },
    { id: 2, word: 'dog', translation: 'собака', emoji: '🐶', transcription: '[dɒg]', example: 'The dog is running.' },
    { id: 3, word: 'bird', translation: 'птица', emoji: '🐦', transcription: '[bɜːrd]', example: 'The bird is flying.' },
  ],
  food: [
    { id: 101, word: 'apple', translation: 'яблоко', emoji: '🍎', transcription: '[ˈæpl]', example: 'I eat an apple.' },
    { id: 102, word: 'banana', translation: 'банан', emoji: '🍌', transcription: '[bəˈnɑːnə]', example: 'Bananas are yellow.' },
    { id: 103, word: 'bread', translation: 'хлеб', emoji: '🍞', transcription: '[bred]', example: 'I eat bread for breakfast.' },
  ],
  colors: [
    { id: 201, word: 'red', translation: 'красный', emoji: '🔴', transcription: '[red]', example: 'An apple is red.' },
    { id: 202, word: 'blue', translation: 'синий', emoji: '🔵', transcription: '[bluː]', example: 'The sky is blue.' },
    { id: 203, word: 'green', translation: 'зелёный', emoji: '🟢', transcription: '[griːn]', example: 'Grass is green.' },
  ],
  numbers: [
    { id: 301, word: 'one', translation: 'один', emoji: '1️⃣', transcription: '[wʌn]', example: 'I have one apple.' },
    { id: 302, word: 'two', translation: 'два', emoji: '2️⃣', transcription: '[tuː]', example: 'I have two dogs.' },
    { id: 303, word: 'three', translation: 'три', emoji: '3️⃣', transcription: '[θriː]', example: 'Three cats are sleeping.' },
  ],
  family: [
    { id: 401, word: 'mother', translation: 'мама', emoji: '👩', transcription: '[ˈmʌðər]', example: 'My mother cooks dinner.' },
    { id: 402, word: 'father', translation: 'папа', emoji: '👨', transcription: '[ˈfɑːðər]', example: 'My father plays football.' },
    { id: 403, word: 'sister', translation: 'сестра', emoji: '👧', transcription: '[ˈsɪstər]', example: 'My sister reads books.' },
  ],
}

function Lesson() {
  const { category } = useParams()
  const navigate = useNavigate()
  const { addXP, updateUser } = useUserStore()
  
  const [currentStep, setCurrentStep] = useState(LESSON_STEPS.INTRO)
  const [currentWordIndex, setCurrentWordIndex] = useState(0)
  const [words, setWords] = useState([])
  const [answers, setAnswers] = useState({})
  const [xpEarned, setXpEarned] = useState(0)
  const [showResult, setShowResult] = useState(null) // 'correct' | 'wrong' | null
  
  // Инициализация урока
  useEffect(() => {
    const lessonWords = DEMO_WORDS[category] || DEMO_WORDS.animals
    setWords(lessonWords)
  }, [category])
  
  const currentWord = words[currentWordIndex]
  const progress = ((currentWordIndex) / words.length) * 100
  
  const startLesson = () => {
    vibrate('impact')
    setCurrentStep(LESSON_STEPS.DISCOVERY)
    setCurrentWordIndex(0)
    setAnswers({})
    setXpEarned(0)
  }
  
  // Переход к следующему слову/этапу
  const advanceProgress = () => {
    vibrate('impact')
    const nextIndex = currentWordIndex + 1
    
    // Если Discovery - переходим к следующему слову или к Quiz
    if (currentStep === LESSON_STEPS.DISCOVERY) {
      if (nextIndex < words.length) {
        setCurrentWordIndex(nextIndex)
      } else {
        setCurrentStep(LESSON_STEPS.QUIZ)
        setCurrentWordIndex(0)
      }
    }
    // Если Quiz - переходим к следующему вопросу или к Missing Letter
    else if (currentStep === LESSON_STEPS.QUIZ) {
      if (nextIndex < words.length) {
        setCurrentWordIndex(nextIndex)
      } else {
        setCurrentStep(LESSON_STEPS.MISSING_LETTER)
        setCurrentWordIndex(0)
      }
    }
    // Если Missing Letter - переходим к следующему или к Speed Round
    else if (currentStep === LESSON_STEPS.MISSING_LETTER) {
      if (nextIndex < words.length) {
        setCurrentWordIndex(nextIndex)
      } else {
        setCurrentStep(LESSON_STEPS.SPEED_ROUND)
        setCurrentWordIndex(0)
      }
    }
    // Если Speed Round - переходим к следующему или к Complete
    else if (currentStep === LESSON_STEPS.SPEED_ROUND) {
      if (nextIndex < words.length) {
        setCurrentWordIndex(nextIndex)
      } else {
        setCurrentStep(LESSON_STEPS.COMPLETE)
      }
    }
  }
  
  const nextWord = () => {
    vibrate('impact')
    advanceProgress()
  }
  
  const handleAnswer = (isCorrect) => {
    vibrate(isCorrect ? 'success' : 'error')
    setShowResult(isCorrect ? 'correct' : 'wrong')
    
    if (isCorrect) {
      const xp = 10
      setXpEarned(prev => prev + xp)
      setAnswers(prev => ({ ...prev, [currentWord?.id]: true }))
      updateUser({ xp: (useUserStore.getState().user?.xp || 0) + xp })
    } else {
      setAnswers(prev => ({ ...prev, [currentWord?.id]: false }))
    }
    
    setTimeout(() => {
      setShowResult(null)
      nextWord()
    }, 1000)
  }
  
  // Компонент: Intro
  const IntroStep = () => (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      className="flex flex-col items-center justify-center min-h-screen px-4"
    >
      <div className="bg-white/90 backdrop-blur rounded-3xl p-8 shadow-2xl max-w-sm w-full text-center">
        <motion.div
          animate={{ rotate: [0, 10, -10, 0] }}
          transition={{ duration: 2, repeat: Infinity }}
          className="text-6xl mb-6"
        >
          📚
        </motion.div>
        
        <h1 className="text-2xl font-bold text-gray-800 mb-2">
          Урок: {category}
        </h1>
        <p className="text-gray-500 mb-6">
          Тебе предстоит выучить {words.length} новых слов!
        </p>
        
        <div className="flex justify-center gap-4 mb-6">
          <div className="bg-primary/10 rounded-xl p-3">
            <div className="text-2xl">📖</div>
            <div className="text-xs text-gray-500">Изучаем</div>
          </div>
          <div className="bg-success/10 rounded-xl p-3">
            <div className="text-2xl">🎯</div>
            <div className="text-xs text-gray-500">Проверяем</div>
          </div>
          <div className="bg-secondary/10 rounded-xl p-3">
            <div className="text-2xl">⚡</div>
            <div className="text-xs text-gray-500">Закрепляем</div>
          </div>
        </div>
        
        <button
          onClick={startLesson}
          className="w-full bg-gradient-to-r from-primary to-primary-light text-white font-bold py-4 rounded-xl shadow-lg active:scale-95 transition-transform"
        >
          Начать урок! 🚀
        </button>
      </div>
    </motion.div>
  )
  
  // Компонент: Discovery (Изучение слова)
  const DiscoveryStep = () => (
    <motion.div
      initial={{ opacity: 0, x: 50 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -50 }}
      className="min-h-screen px-4 py-6"
    >
      {/* Progress Bar */}
      <div className="mb-6">
        <div className="flex justify-between text-white text-sm mb-2">
          <span>Слово {currentWordIndex + 1} из {words.length}</span>
          <span>{Math.round(progress)}%</span>
        </div>
        <div className="h-2 bg-white/30 rounded-full overflow-hidden">
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${progress}%` }}
            className="h-full bg-white rounded-full"
          />
        </div>
      </div>
      
      {/* Word Card */}
      <div className="bg-white/90 backdrop-blur rounded-3xl p-6 shadow-xl">
        <div className="text-center mb-6">
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ type: "spring", bounce: 0.5 }}
            className="text-8xl mb-4"
          >
            {currentWord?.emoji}
          </motion.div>
          
          <motion.h2
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-3xl font-bold text-gray-800 mb-2"
          >
            {currentWord?.word}
          </motion.h2>
          
          <p className="text-gray-500 mb-4">
            {currentWord?.transcription}
          </p>
          
          <div className="bg-gray-100 rounded-xl p-4 mb-4">
            <p className="text-gray-700">
              <span className="font-bold">🇷🇺</span> {currentWord?.translation}
            </p>
          </div>
          
          <div className="bg-primary/10 rounded-xl p-4">
            <p className="text-gray-700 italic">
              "{currentWord?.example}"
            </p>
          </div>
        </div>
        
        {/* Audio Button with TTS */}
        <AudioButton word={currentWord?.word} />
      </div>
      
      {/* Next Button */}
      <button
        onClick={nextWord}
        className="w-full mt-4 bg-white/20 backdrop-blur text-white font-bold py-4 rounded-xl border-2 border-white/30"
      >
        Дальше →
      </button>
    </motion.div>
  )
  
  // Компонент: Quiz
  const QuizStep = () => {
    const correctWord = words[currentWordIndex]
    const wrongWords = words.filter((_, i) => i !== currentWordIndex).slice(0, 2)
    const options = [...wrongWords.map(w => w.word), correctWord.word].sort(() => Math.random() - 0.5)
    
    return (
      <motion.div
        initial={{ opacity: 0, x: 50 }}
        animate={{ opacity: 1, x: 0 }}
        exit={{ opacity: 0, x: -50 }}
        className="min-h-screen px-4 py-6"
      >
        {/* Quiz Header */}
        <div className="text-center text-white mb-6">
          <div className="text-2xl mb-2">🎯</div>
          <h2 className="text-xl font-bold">Угадай по картинке!</h2>
          <p className="text-sm opacity-80">Вопрос {currentWordIndex + 1} из {words.length}</p>
        </div>
        
        {/* Word Image */}
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          className="bg-white/90 backdrop-blur rounded-3xl p-8 shadow-xl text-center mb-6"
        >
          <div className="text-8xl mb-4">{correctWord?.emoji}</div>
          <p className="text-gray-500">Выбери правильный ответ:</p>
        </motion.div>
        
        {/* Options */}
        <div className="space-y-3">
          {options.map((option, index) => (
            <motion.button
              key={option}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
              onClick={() => handleAnswer(option === correctWord?.word)}
              className="w-full bg-white/90 backdrop-blur rounded-xl p-4 shadow-lg text-lg font-bold text-gray-800 active:scale-95 transition-transform"
            >
              {option}
            </motion.button>
          ))}
        </div>
      </motion.div>
    )
  }
  
  // Компонент: Missing Letter
  const MissingLetterStep = () => {
    const word = words[currentWordIndex]
    if (!word) return null
    
    // Создаём слово с пропущенной буквой
    const missingIndex = Math.floor(Math.random() * word.word.length)
    const correctLetter = word.word[missingIndex]
    const maskedWord = word.word.substring(0, missingIndex) + '___' + word.word.substring(missingIndex + 1)
    
    // Варианты букв
    const allLetters = 'abcdefghijklmnopqrstuvwxyz'.split('')
    const wrongLetters = allLetters.filter(l => l !== correctLetter).sort(() => Math.random() - 0.5).slice(0, 3)
    const letterOptions = [...wrongLetters, correctLetter].sort(() => Math.random() - 0.5)
    
    const handleLetterClick = (letter) => {
      handleAnswer(letter === correctLetter)
    }
    
    return (
      <motion.div
        initial={{ opacity: 0, x: 50 }}
        animate={{ opacity: 1, x: 0 }}
        exit={{ opacity: 0, x: -50 }}
        className="min-h-screen px-4 py-6"
      >
        {/* Header */}
        <div className="text-center text-white mb-6">
          <div className="text-2xl mb-2">✏️</div>
          <h2 className="text-xl font-bold">Пропущенная буква!</h2>
          <p className="text-sm opacity-80">Вопрос {currentWordIndex + 1} из {words.length}</p>
        </div>
        
        {/* Word Card */}
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          className="bg-white/90 backdrop-blur rounded-3xl p-8 shadow-xl text-center mb-6"
        >
          <div className="text-6xl mb-4">{word.emoji}</div>
          <div className="text-3xl font-bold text-gray-800 mb-2">{maskedWord}</div>
          <p className="text-gray-500">{word.translation}</p>
        </motion.div>
        
        {/* Letter Options */}
        <div className="grid grid-cols-4 gap-3">
          {letterOptions.map((letter, index) => (
            <motion.button
              key={letter}
              initial={{ opacity: 0, scale: 0 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: index * 0.1 }}
              onClick={() => handleLetterClick(letter)}
              className="bg-white/90 backdrop-blur rounded-xl p-4 shadow-lg text-2xl font-bold text-gray-800 active:scale-95 transition-transform hover:bg-white"
            >
              {letter.toUpperCase()}
            </motion.button>
          ))}
        </div>
      </motion.div>
    )
  }
  
  // Компонент: Speed Round
  const SpeedRoundStep = () => {
    const correctWord = words[currentWordIndex]
    if (!correctWord) return null
    
    const wrongWords = words.filter((_, i) => i !== currentWordIndex).slice(0, 2)
    const options = [...wrongWords.map(w => w.word), correctWord.word].sort(() => Math.random() - 0.5)
    const [timeLeft, setTimeLeft] = useState(5)
    
    useEffect(() => {
      if (currentStep !== LESSON_STEPS.SPEED_ROUND) return
      
      const timer = setInterval(() => {
        setTimeLeft(prev => {
          if (prev <= 1) {
            clearInterval(timer)
            handleAnswer(false) // Таймер истёк - неправильный ответ
            return 0
          }
          return prev - 1
        })
      }, 1000)
      
      return () => clearInterval(timer)
    }, [currentStep])
    
    return (
      <motion.div
        initial={{ opacity: 0, x: 50 }}
        animate={{ opacity: 1, x: 0 }}
        exit={{ opacity: 0, x: -50 }}
        className="min-h-screen px-4 py-6"
      >
        {/* Timer */}
        <div className="flex justify-center mb-6">
          <motion.div
            animate={{ scale: timeLeft <= 2 ? [1, 1.2, 1] : 1 }}
            transition={{ repeat: Infinity, duration: 0.5 }}
            className={`text-4xl font-bold ${
              timeLeft <= 2 ? 'text-red-500' : 'text-white'
            }`}
          >
            ⏱️ {timeLeft}c
          </motion.div>
        </div>
        
        {/* Header */}
        <div className="text-center text-white mb-6">
          <div className="text-2xl mb-2">⚡</div>
          <h2 className="text-xl font-bold">Скоростной раунд!</h2>
          <p className="text-sm opacity-80">Вопрос {currentWordIndex + 1} из {words.length}</p>
        </div>
        
        {/* Word Card */}
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          className="bg-white/90 backdrop-blur rounded-3xl p-8 shadow-xl text-center mb-6"
        >
          <div className="text-8xl mb-4">{correctWord?.emoji}</div>
          <p className="text-gray-500">Быстрее!</p>
        </motion.div>
        
        {/* Options */}
        <div className="space-y-3">
          {options.map((option, index) => (
            <motion.button
              key={option}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
              onClick={() => handleAnswer(option === correctWord?.word)}
              className="w-full bg-gradient-to-r from-orange-400 to-red-500 text-white rounded-xl p-4 shadow-lg text-lg font-bold active:scale-95 transition-transform"
            >
              {option}
            </motion.button>
          ))}
        </div>
      </motion.div>
    )
  }
  
  // Компонент: Complete
  const CompleteStep = () => {
    const correctCount = Object.values(answers).filter(Boolean).length
    const totalWords = words.length
    const accuracy = Math.round((correctCount / totalWords) * 100)
    
    return (
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        className="min-h-screen px-4 py-6 flex flex-col items-center justify-center"
      >
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
          className="absolute top-10 right-10 text-6xl opacity-20"
        >
          ⭐
        </motion.div>
        
        <div className="bg-white/90 backdrop-blur rounded-3xl p-8 shadow-2xl max-w-sm w-full text-center">
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ type: "spring", bounce: 0.5 }}
            className="text-6xl mb-6"
          >
            🏆
          </motion.div>
          
          <h1 className="text-2xl font-bold text-gray-800 mb-2">
            Урок завершён!
          </h1>
          
          <div className="grid grid-cols-2 gap-4 my-6">
            <div className="bg-primary/10 rounded-xl p-4">
              <div className="text-3xl font-bold text-primary">{xpEarned}</div>
              <div className="text-sm text-gray-500">⭐ Звёзд</div>
            </div>
            <div className="bg-success/10 rounded-xl p-4">
              <div className="text-3xl font-bold text-success">{accuracy}%</div>
              <div className="text-sm text-gray-500">Точность</div>
            </div>
          </div>
          
          <div className="bg-yellow-100 rounded-xl p-4 mb-6">
            <div className="text-lg">💪 Молодец!</div>
            <div className="text-sm text-gray-500">Ты выучил {totalWords} новых слов!</div>
          </div>
          
          <div className="space-y-3">
            <button
              onClick={() => {
                vibrate('success')
                navigate('/')
              }}
              className="w-full bg-gradient-to-r from-primary to-primary-light text-white font-bold py-4 rounded-xl shadow-lg"
            >
              В главное меню
            </button>
            <button
              onClick={() => {
                vibrate('impact')
                setCurrentStep(LESSON_STEPS.INTRO)
                startLesson()
              }}
              className="w-full bg-white text-primary font-bold py-4 rounded-xl border-2 border-primary"
            >
              Повторить урок
            </button>
          </div>
        </div>
      </motion.div>
    )
  }
  
  // Result overlay
  const ResultOverlay = () => (
    <AnimatePresence>
      {showResult && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
        >
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            exit={{ scale: 0 }}
            className={`w-32 h-32 rounded-full flex items-center justify-center ${
              showResult === 'correct' ? 'bg-success' : 'bg-error'
            }`}
          >
            <span className="text-6xl">
              {showResult === 'correct' ? '🎉' : '🤔'}
            </span>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  )
  
  return (
    <div className="bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 min-h-screen">
      <ResultOverlay />
      
      <AnimatePresence mode="wait">
        {currentStep === LESSON_STEPS.INTRO && (
          <div key="intro">
            <IntroStep />
          </div>
        )}
        
        {currentStep === LESSON_STEPS.DISCOVERY && (
          <motion.div
            key="discovery"
            initial={{ opacity: 0, x: 100 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -100 }}
          >
            <DiscoveryStep />
          </motion.div>
        )}
        
        {currentStep === LESSON_STEPS.QUIZ && (
          <motion.div
            key="quiz"
            initial={{ opacity: 0, x: 100 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -100 }}
          >
            <QuizStep />
          </motion.div>
        )}
        
        {currentStep === LESSON_STEPS.MISSING_LETTER && (
          <motion.div
            key="missing_letter"
            initial={{ opacity: 0, x: 100 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -100 }}
          >
            <MissingLetterStep />
          </motion.div>
        )}
        
        {currentStep === LESSON_STEPS.SPEED_ROUND && (
          <motion.div
            key="speed_round"
            initial={{ opacity: 0, x: 100 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -100 }}
          >
            <SpeedRoundStep />
          </motion.div>
        )}
        
        {currentStep === LESSON_STEPS.COMPLETE && (
          <motion.div
            key="complete"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
          >
            <CompleteStep />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

export default Lesson