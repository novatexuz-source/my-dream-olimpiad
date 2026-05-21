import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { API_BASE } from '../../config'
import './ExamLogin.css'

export default function ExamLogin() {
  const [code, setCode] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [participantInfo, setParticipantInfo] = useState(null)
  const [tests, setTests] = useState([])
  
  const navigate = useNavigate()

  const handleCodeChange = (e) => {
    const val = e.target.value.replace(/\D/g, '') // only digits
    if (val.length <= 6) {
      setCode(val)
      setError('')
    }
  }

  const handleLogin = async (e) => {
    e.preventDefault()
    if (code.length !== 6) {
      setError("Unikal kod 6 ta raqamdan iborat bo'lishi kerak!")
      return
    }

    setLoading(true)
    setError('')

    try {
      const res = await fetch(`${API_BASE}/exams/login/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ unique_code: code })
      })

      const data = await res.json()

      if (res.ok) {
        setParticipantInfo(data.participant)
        setTests(data.tests)
      } else {
        setError(data.error || "Tizimga kirishda xatolik yuz berdi.")
      }
    } catch (err) {
      console.error(err)
      setError("Tarmoq xatoligi yuz berdi. Server ishlayotganini tekshiring.")
    } finally {
      setLoading(false)
    }
  }

  const handleStartExam = async (testId) => {
    if (!participantInfo) return
    setLoading(true)
    setError('')

    try {
      const res = await fetch(`${API_BASE}/exams/start/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          participant_id: participantInfo.id,
          test_id: testId
        })
      })

      const data = await res.json()

      if (res.ok) {
        // Navigate to the test interface
        navigate(`/exam/take/${data.id}`)
      } else {
        setError(data.error || "Testni boshlab bo'lmadi.")
      }
    } catch (err) {
      console.error(err)
      setError("Xatolik yuz berdi, qaytadan urinib ko'ring.")
    } finally {
      setLoading(false)
    }
  }

  const formatTime = (timeStr) => {
    if (!timeStr) return ''
    return new Date(timeStr).toLocaleString('uz-UZ', {
      day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit'
    })
  }

  return (
    <div className="exam-login-container">
      <div className="exam-login-card">
        <div className="exam-logo">
          <span>✨</span>
          <h2>My Dream Olympiad</h2>
          <p>O'quvchilar uchun test portali</p>
        </div>

        {!participantInfo ? (
          <form className="code-form" onSubmit={handleLogin}>
            <div className="form-group">
              <label htmlFor="unique-code">Unikal kodingizni kiriting</label>
              <input
                id="unique-code"
                type="text"
                value={code}
                onChange={handleCodeChange}
                placeholder="000000"
                maxLength={6}
                autoFocus
                disabled={loading}
              />
              <p className="helper-text">Telegram bot orqali yuborilgan 6 xonali unikal raqam</p>
            </div>

            {error && <div className="error-message">⚠️ {error}</div>}

            <button type="submit" className="btn-submit-code" disabled={loading}>
              {loading ? 'Tekshirilmoqda...' : 'Kirish →'}
            </button>
          </form>
        ) : (
          <div className="tests-portal">
            <div className="portal-header">
              <h3>Xush kelibsiz, <span className="p-name">{participantInfo.full_name}</span>!</h3>
              <p className="p-meta">{participantInfo.grade}-sinf • Kod: {participantInfo.unique_code}</p>
            </div>

            <h4 className="section-title">Sizga ajratilgan olimpiada testlari:</h4>
            
            {tests.length === 0 ? (
              <div className="no-tests">
                <span className="no-tests-icon">📭</span>
                <p>Hozirda siz uchun faol testlar topilmadi.</p>
              </div>
            ) : (
              <div className="exam-list">
                {tests.map(t => (
                  <div className={`exam-item-card ${t.status}`} key={t.id}>
                    <div className="exam-item-header">
                      <span className="exam-subject">{t.subject_name}</span>
                      <span className={`exam-badge ${t.status}`}>
                        {t.status === 'in_progress' && '🚀 Davom etmoqda'}
                        {t.status === 'completed' && '✅ Topshirilgan'}
                        {t.status === 'expired' && '⌛ Muddati tugagan'}
                        {t.status === 'waiting_start' && '📅 Boshlanishi kutilmoqda'}
                        {t.status === 'available' && '✍️ Boshlashga tayyor'}
                      </span>
                    </div>

                    <h4 className="exam-title">{t.title}</h4>
                    
                    <div className="exam-details">
                      <div><span>⏱</span> Vaqti: {t.duration_minutes} daqiqa</div>
                      <div><span>📋</span> Savollar: {t.questions_count} ta</div>
                      {t.start_datetime && (
                        <div className="exam-time-window">
                          <span>📅</span> {formatTime(t.start_datetime)} - {formatTime(t.end_datetime)}
                        </div>
                      )}
                    </div>

                    <div className="exam-action-row">
                      {t.status === 'available' && (
                        <button className="btn-start-exam" onClick={() => handleStartExam(t.id)} disabled={loading}>
                          Testni boshlash
                        </button>
                      )}
                      {t.status === 'in_progress' && (
                        <button className="btn-resume-exam" onClick={() => handleStartExam(t.id)} disabled={loading}>
                          Davom ettirish
                        </button>
                      )}
                      {t.status === 'completed' && (
                        <span className="msg-info">Test yakunlangan</span>
                      )}
                      {t.status === 'expired' && (
                        <span className="msg-expired">Muddati o'tgan</span>
                      )}
                      {t.status === 'waiting_start' && (
                        <span className="msg-waiting">Boshlanishini kuting</span>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}

            {error && <div className="error-message">⚠️ {error}</div>}

            <button className="btn-back-code" onClick={() => { setParticipantInfo(null); setCode(''); }}>
              ← Boshqa kod kiritish
            </button>
          </div>
        )}
      </div>
    </div>
  )
}
