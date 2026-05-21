import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import './ExamResult.css'

const API_BASE = 'http://localhost:8000/api'

export default function ExamResult() {
  const { sessionId } = useParams()
  const navigate = useNavigate()

  const [loading, setLoading] = useState(true)
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchResult()
  }, [sessionId])

  const fetchResult = async () => {
    try {
      const res = await fetch(`${API_BASE}/exams/result/${sessionId}/`)
      const data = await res.json()

      if (res.ok) {
        setResult(data)
      } else {
        setError(data.error || "Natijani yuklab bo'lmadi.")
      }
    } catch (e) {
      console.error(e)
      setError("Tarmoq xatoligi yuz berdi.")
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="result-loading-screen">
        <div className="spinner-big"></div>
        <p>Natijangiz hisoblanmoqda, iltimos kuting...</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="result-error-screen">
        <div className="error-card">
          <span>⚠️</span>
          <h3>Xatolik</h3>
          <p>{error}</p>
          <button onClick={() => navigate('/exam/login')}>Bosh sahifaga qaytish</button>
        </div>
      </div>
    )
  }

  const isPassed = result.percentage >= 50 // arbitrary threshold for UI presentation

  return (
    <div className="exam-result-container">
      <div className="exam-result-card">
        <div className="result-badge-top">
          {isPassed ? '🎉 Omad!' : '👍 Rahmat!'}
        </div>

        <h2 className="congrats-title">
          {isPassed ? "Tabriklaymiz!" : "Test yakunlandi!"}
        </h2>
        <p className="congrats-sub">
          Siz "My Dream International Olympiad" testini muvaffaqiyatli topshirdingiz.
        </p>

        <div className="score-circle-wrapper">
          <div className={`score-circle ${isPassed ? 'passed' : 'failed'}`}>
            <span className="score-percent">{Math.round(result.percentage)}%</span>
            <span className="score-lbl">Umumiy foiz</span>
          </div>
        </div>

        <div className="result-stats-table">
          <div className="stat-row">
            <span className="stat-label">👤 Ishtirokchi:</span>
            <span className="stat-value">{result.participant_name}</span>
          </div>
          <div className="stat-row">
            <span className="stat-label">📚 Test / Sinf:</span>
            <span className="stat-value">{result.subject_name} • {result.grade}-sinf</span>
          </div>
          <div className="stat-row">
            <span className="stat-label">🎯 To'g'ri javoblar:</span>
            <span className="stat-value correct">{result.correct_count} ta</span>
          </div>
          <div className="stat-row">
            <span className="stat-label">❌ Noto'g'ri javoblar:</span>
            <span className="stat-value wrong">{result.wrong_count} ta</span>
          </div>
          <div className="stat-row">
            <span className="stat-label">📋 Jami savollar:</span>
            <span className="stat-value">{result.total_questions} ta</span>
          </div>
        </div>

        <div className="final-notice">
          <p>📜 Yakuniy natijalar va g'oliblar ro'yxati barcha ishtirokchilar testni yakunlagandan so'ng e'lon qilinadi.</p>
        </div>

        <button className="btn-finish-go-home" onClick={() => navigate('/exam/login')}>
          Tizimdan chiqish
        </button>
      </div>
    </div>
  )
}
