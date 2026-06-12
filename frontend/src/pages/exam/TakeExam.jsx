import React, { useState, useEffect, useRef } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { API_BASE } from '../../config'
import './TakeExam.css'

export default function TakeExam() {
  const { sessionId } = useParams()
  const navigate = useNavigate()

  const [loading, setLoading] = useState(true)
  const [sessionData, setSessionData] = useState(null)
  const [questions, setQuestions] = useState([])
  const [currentIdx, setCurrentIdx] = useState(0)
  const [answers, setAnswers] = useState({}) // question_id -> option
  const [savingAnswers, setSavingAnswers] = useState({}) // question_id -> boolean
  const [timeLeft, setTimeLeft] = useState(0) // seconds
  const [error, setError] = useState('')
  const [showConfirmFinish, setShowConfirmFinish] = useState(false)
  const [finishing, setFinishing] = useState(false)

  const timerRef = useRef(null)
  // Ref keeps the interval callback pointing at the latest finish handler
  // (avoids the stale-closure bug where auto-submit used old state).
  const finishRef = useRef(() => {})
  const examCode = localStorage.getItem('exam_code') || ''

  useEffect(() => {
    fetchSession()
    return () => {
      if (timerRef.current) clearInterval(timerRef.current)
    }
  }, [sessionId])

  useEffect(() => {
    if (timeLeft > 0) {
      timerRef.current = setInterval(() => {
        setTimeLeft(prev => {
          if (prev <= 1) {
            clearInterval(timerRef.current)
            // Auto submit when time runs out
            finishRef.current(true)
            return 0
          }
          return prev - 1
        })
      }, 1000)
    }
    return () => {
      if (timerRef.current) clearInterval(timerRef.current)
    }
  }, [timeLeft > 0])

  const fetchSession = async () => {
    try {
      const res = await fetch(`${API_BASE}/exams/session/${sessionId}/?code=${encodeURIComponent(examCode)}`)
      const data = await res.json()

      if (res.ok) {
        const sess = data.session
        if (sess.status === 'completed') {
          navigate(`/exam/result/${sessionId}`)
          return
        }

        setSessionData(sess)
        setQuestions(sess.questions)
        setTimeLeft(data.remaining_seconds)

        // Parse pre-saved answers
        const saved = {}
        sess.answers.forEach(a => {
          saved[a.question] = a.selected_answer
        })
        setAnswers(saved)
      } else {
        setError(data.error || "Sessiya ma'lumotlarini yuklashda xatolik yuz berdi.")
      }
    } catch (e) {
      console.error(e)
      setError("Tarmoq xatoligi yuz berdi. Iltimos, sahifani yangilang.")
    } finally {
      setLoading(false)
    }
  }

  const handleOptionClick = async (questionId, option) => {
    // Optimistic UI update
    setAnswers(prev => ({ ...prev, [questionId]: option }))
    setSavingAnswers(prev => ({ ...prev, [questionId]: true }))

    try {
      const res = await fetch(`${API_BASE}/exams/answer/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          session_id: sessionId,
          question_id: questionId,
          selected_answer: option,
          unique_code: examCode
        })
      })

      if (!res.ok) {
        const err = await res.json()
        console.error("Failed to save answer", err)
      }
    } catch (e) {
      console.error(e)
    } finally {
      setSavingAnswers(prev => ({ ...prev, [questionId]: false }))
    }
  }

  const handleFinishExam = async (auto = false) => {
    if (finishing) return
    setFinishing(true)
    setShowConfirmFinish(false)

    try {
      const res = await fetch(`${API_BASE}/exams/finish/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ session_id: sessionId, unique_code: examCode })
      })

      if (res.ok) {
        navigate(`/exam/result/${sessionId}`)
      } else {
        alert("Natijani saqlashda xatolik yuz berdi.")
      }
    } catch (e) {
      console.error(e)
      alert("Xatolik yuz berdi, qayta urinib ko'ring.")
    } finally {
      setFinishing(false)
    }
  }

  // Keep the timer's auto-submit pointing at the freshest handler
  finishRef.current = handleFinishExam

  const formatTimer = (seconds) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
  }

  if (loading) {
    return (
      <div className="exam-loading-screen">
        <div className="spinner-big"></div>
        <p>Test yuklanmoqda. Iltimos, kuting...</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="exam-error-screen">
        <div className="error-card">
          <span>⚠️</span>
          <h3>Xatolik</h3>
          <p>{error}</p>
          <button onClick={() => navigate('/exam/login')}>Chiqish</button>
        </div>
      </div>
    )
  }

  const currentQuestion = questions[currentIdx]
  const totalQuestions = questions.length

  return (
    <div className="take-exam-page">
      {/* Top Navigation / Stats bar */}
      <header className="exam-header-bar">
        <div className="bar-left">
          <span className="subject-tag">{sessionData?.test_title}</span>
          <span className="student-name">{sessionData?.participant_name}</span>
        </div>
        <div className="bar-right">
          <div className="timer-wrapper">
            <span>⏱️ Qolgan vaqt:</span>
            <span className={`timer-digits ${timeLeft < 180 ? 'critical' : ''}`}>
              {formatTimer(timeLeft)}
            </span>
          </div>
          <button className="btn-finish-trigger" onClick={() => setShowConfirmFinish(true)}>
            Testni yakunlash
          </button>
        </div>
      </header>

      <div className="exam-main-container">
        {/* Sidebar Questions Nav */}
        <aside className="exam-sidebar-nav">
          <h3 className="nav-title">Savollar ({totalQuestions} ta)</h3>
          <div className="nav-grid">
            {questions.map((q, idx) => {
              const isCurrent = idx === currentIdx
              const isAnswered = !!answers[q.id]
              const isSaving = savingAnswers[q.id]

              return (
                <button
                  key={q.id}
                  className={`nav-num-btn ${isCurrent ? 'active' : ''} ${isAnswered ? 'answered' : ''} ${isSaving ? 'saving' : ''}`}
                  onClick={() => setCurrentIdx(idx)}
                >
                  {idx + 1}
                </button>
              )
            })}
          </div>
          <div className="nav-legend">
            <div><span className="dot dot-unanswered"></span> Belgilanmagan</div>
            <div><span className="dot dot-answered"></span> Belgilangan</div>
            <div><span className="dot dot-active"></span> Joriy savol</div>
          </div>
        </aside>

        {/* Question Panel */}
        <main className="exam-question-panel">
          {currentQuestion && (
            <div className="question-card-interactive">
              <div className="q-card-header">
                <span className="q-count-badge">Savol {currentIdx + 1} / {totalQuestions}</span>
                {savingAnswers[currentQuestion.id] && <span className="saving-indicator">Avtomatik saqlanmoqda...</span>}
              </div>

              <div className="q-card-body">
                <h2 className="question-text">{currentQuestion.question_text}</h2>
                
                {currentQuestion.question_image && (
                  <div className="question-image-box">
                    <img src={currentQuestion.question_image} alt="Savol rasmi" />
                  </div>
                )}

                <div className="options-interactive-list">
                  {(currentQuestion.options
                    ? currentQuestion.options
                    : ['A', 'B', 'C', 'D'].map(l => ({ key: l, text: currentQuestion[`option_${l.toLowerCase()}`] }))
                  ).map((opt, i) => {
                    const displayLetter = ['A', 'B', 'C', 'D'][i] || String(i + 1)
                    const isSelected = answers[currentQuestion.id] === opt.key

                    return (
                      <div
                        key={opt.key}
                        className={`option-card-interactive ${isSelected ? 'selected' : ''}`}
                        onClick={() => handleOptionClick(currentQuestion.id, opt.key)}
                      >
                        <div className="option-letter-badge">{displayLetter}</div>
                        <div className="option-text-content">{opt.text}</div>
                      </div>
                    )
                  })}
                </div>
              </div>

              <div className="q-card-footer">
                <button
                  className="btn-prev-q"
                  disabled={currentIdx === 0}
                  onClick={() => setCurrentIdx(prev => prev - 1)}
                >
                  ← Oldingi savol
                </button>
                {currentIdx < totalQuestions - 1 ? (
                  <button
                    className="btn-next-q"
                    onClick={() => setCurrentIdx(prev => prev + 1)}
                  >
                    Keyingi savol →
                  </button>
                ) : (
                  <button
                    className="btn-finish-q"
                    onClick={() => setShowConfirmFinish(true)}
                  >
                    Testni topshirish
                  </button>
                )}
              </div>
            </div>
          )}
        </main>
      </div>

      {/* Confirmation Modal */}
      {showConfirmFinish && (
        <div className="modal-backdrop-exam">
          <div className="modal-content-exam">
            <h3>Testni yakunlash</h3>
            <p>Rostdan ham testni topshirib yakunlamoqchimisiz? Topshirilgandan so'ng javoblarni o'zgartirib bo'lmaydi!</p>
            <div className="modal-action-btns">
              <button className="btn-modal-yes" onClick={() => handleFinishExam(false)} disabled={finishing}>
                {finishing ? 'Tugatilmoqda...' : 'Ha, yakunlash'}
              </button>
              <button className="btn-modal-no" onClick={() => setShowConfirmFinish(false)} disabled={finishing}>
                Yo'q, davom ettirish
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
