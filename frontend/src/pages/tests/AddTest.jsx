import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { API_BASE } from '../../config'
import './AddTest.css'

export default function AddTest() {
  const navigate = useNavigate()
  const [subjects, setSubjects] = useState([])
  const [allTests, setAllTests] = useState([])
  
  const [testData, setTestData] = useState({
    subject: '',
    grade: 1,
    duration_minutes: 60,
    start_datetime: '',
    end_datetime: '',
    is_active: true
  })

  // Returns current datetime in datetime-local format (YYYY-MM-DDTHH:mm)
  const getNow = () => {
    const now = new Date()
    now.setMinutes(now.getMinutes() - now.getTimezoneOffset())
    return now.toISOString().slice(0, 16)
  }

  const [questions, setQuestions] = useState([
    {
      id: Date.now(),
      order_number: 1,
      question_text: '',
      option_a: '',
      option_b: '',
      option_c: '',
      option_d: '',
      correct_answer: 'A'
    }
  ])

  const [saving, setSaving] = useState(false)

  useEffect(() => {
    // Load subjects
    fetch(`${API_BASE}/tests/subjects/`)
      .then(res => res.json())
      .then(data => {
        setSubjects(data)
        if (data.length > 0) setTestData(prev => ({ ...prev, subject: data[0].id }))
      })
      .catch(err => console.error(err))

    // Load all existing tests to compute taken grades
    fetch(`${API_BASE}/tests/list/`)
      .then(res => res.json())
      .then(data => setAllTests(data))
      .catch(err => console.error(err))
  }, [])

  // Returns grades already taken for selected subject + selected date
  const getTakenGrades = () => {
    if (!testData.subject || !testData.start_datetime) return []
    const selectedDate = testData.start_datetime.slice(0, 10) // YYYY-MM-DD
    return allTests
      .filter(t => {
        const tDate = t.start_datetime ? t.start_datetime.slice(0, 10) : null
        return String(t.subject) === String(testData.subject) && tDate === selectedDate
      })
      .map(t => Number(t.grade))
  }

  const takenGrades = getTakenGrades()
  const availableGrades = [1,2,3,4,5,6,7,8,9,10,11].filter(n => !takenGrades.includes(n))

  const handleTestChange = (e) => {
    const { name, value, type, checked } = e.target
    setTestData(prev => {
      const updated = { ...prev, [name]: type === 'checkbox' ? checked : value }
      // If start changes, clear end if end is before new start
      if (name === 'start_datetime' && prev.end_datetime && value >= prev.end_datetime) {
        updated.end_datetime = ''
      }
      // When subject or date changes, reset grade to first available
      if (name === 'subject' || name === 'start_datetime') {
        const selDate = name === 'start_datetime' ? value.slice(0, 10) : prev.start_datetime.slice(0, 10)
        const selSubject = name === 'subject' ? value : prev.subject
        const taken = allTests
          .filter(t => {
            const tDate = t.start_datetime ? t.start_datetime.slice(0, 10) : null
            return String(t.subject) === String(selSubject) && tDate === selDate
          })
          .map(t => Number(t.grade))
        const available = [1,2,3,4,5,6,7,8,9,10,11].filter(n => !taken.includes(n))
        if (available.length > 0 && taken.includes(Number(prev.grade))) {
          updated.grade = available[0]
        }
      }
      return updated
    })
  }

  const handleQuestionChange = (id, field, value) => {
    setQuestions(prev => prev.map(q => {
      if (q.id === id) {
        return { ...q, [field]: value }
      }
      return q
    }))
  }

  const addQuestion = () => {
    setQuestions(prev => [
      ...prev,
      {
        id: Date.now(),
        order_number: prev.length + 1,
        question_text: '',
        option_a: '',
        option_b: '',
        option_c: '',
        option_d: '',
        correct_answer: 'A'
      }
    ])
  }

  const removeQuestion = (id) => {
    if (questions.length === 1) return
    setQuestions(prev => {
      const filtered = prev.filter(q => q.id !== id)
      return filtered.map((q, idx) => ({ ...q, order_number: idx + 1 }))
    })
  }

  const handleSave = async () => {
    if (!testData.subject) {
      alert("Iltimos, fanni tanlang.")
      return
    }
    if (!testData.start_datetime) {
      alert("Iltimos, testning boshlanish vaqtini kiriting.")
      return
    }
    if (!testData.end_datetime) {
      alert("Iltimos, testning tugash vaqtini kiriting.")
      return
    }
    if (testData.end_datetime <= testData.start_datetime) {
      alert("Tugash vaqti boshlanish vaqtidan keyin bo'lishi kerak!")
      return
    }

    // Basic validation
    for (let q of questions) {
      if (!q.question_text || !q.option_a || !q.option_b || !q.option_c || !q.option_d) {
        alert(`${q.order_number}-savolda barcha maydonlarni to'ldiring!`)
        return
      }
    }

    setSaving(true)
    
    // Clean up IDs for backend creation
    const questionsToSave = questions.map(q => {
      const { id, ...rest } = q
      return rest
    })

    // Auto-generate title: SubjectName + Grade + Date
    const subjectName = subjects.find(s => s.id === testData.subject)?.name || 'Test'
    const dateStr = new Date(testData.start_datetime).toLocaleDateString('uz-UZ', { day: '2-digit', month: '2-digit', year: 'numeric' })
    const autoTitle = `${subjectName} ${testData.grade}-sinf (${dateStr})`

    const payload = {
      ...testData,
      title: autoTitle,
      passing_percentage: 0,
      start_datetime: testData.start_datetime || null,
      end_datetime: testData.end_datetime || null,
      questions: questionsToSave
    }

    try {
      const res = await fetch(`${API_BASE}/tests/list/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      })

      if (res.ok) {
        navigate('/tests')
      } else {
        const err = await res.json()
        // Show human-readable error from backend
        const msg = typeof err === 'string' ? err
          : Array.isArray(err) ? err[0]
          : err.non_field_errors ? err.non_field_errors[0]
          : Object.values(err).flat()[0] || 'Xatolik yuz berdi'
        alert(msg)
      }
    } catch (e) {
      console.error(e)
      alert("Xatolik yuz berdi")
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="add-test-page">
      <div className="add-test-header">
        <button className="btn-back" onClick={() => navigate('/tests')}>← Orqaga</button>
        <div className="title-section">
          <h1>Yangi test yaratish</h1>
          <p>Test sozlamalari va savollarni kiriting</p>
        </div>
        <button className="btn-save" onClick={handleSave} disabled={saving}>
          {saving ? 'Saqlanmoqda...' : '💾 Testni saqlash'}
        </button>
      </div>

      <div className="test-builder-container">
        {/* Test Settings Sidebar */}
        <div className="test-settings-panel">
          <h3>⚙️ Test Sozlamalari</h3>
          
          <div className="form-group">
            <label>Fan nomi</label>
            <select name="subject" value={testData.subject} onChange={handleTestChange}>
              <option value="" disabled>Fanni tanlang</option>
              {subjects.map(s => <option key={s.id} value={s.id}>{s.name}</option>)}
            </select>
          </div>

          <div className="form-group">
            <label>Sinf</label>
            {takenGrades.length > 0 && testData.start_datetime && (
              <div className="grade-warning">
                ⚠️ {takenGrades.map(g => `${g}-sinf`).join(', ')} — bu sana uchun band
              </div>
            )}
            {availableGrades.length === 0 ? (
              <div className="grade-full">
                🚫 Shu fandan shu kuni barcha sinflar uchun test mavjud!
              </div>
            ) : (
              <select name="grade" value={testData.grade} onChange={handleTestChange}>
                {availableGrades.map(n => <option key={n} value={n}>{n}-sinf</option>)}
              </select>
            )}
          </div>

          <div className="form-group-row">
            <div className="form-group">
              <label>Vaqt (daqiqa)</label>
              <input type="number" name="duration_minutes" value={testData.duration_minutes} onChange={handleTestChange} min="10" />
            </div>
          </div>

          <div className="form-group datetime-section">
            <label>📅 Boshlanish vaqti</label>
            <input 
              type="datetime-local" 
              name="start_datetime" 
              value={testData.start_datetime} 
              min={getNow()}
              onChange={handleTestChange} 
            />
          </div>

          <div className="form-group">
            <label>🏁 Tugash vaqti</label>
            <input 
              type="datetime-local" 
              name="end_datetime" 
              value={testData.end_datetime} 
              min={testData.start_datetime || getNow()}
              onChange={handleTestChange} 
              disabled={!testData.start_datetime}
            />
          </div>
          
          <div className="form-group checkbox-group">
            <label className="checkbox-label">
              <input type="checkbox" name="is_active" checked={testData.is_active} onChange={handleTestChange} />
              <span>Test aktiv holatda (darhol ishga tushadi)</span>
            </label>
          </div>
        </div>

        {/* Questions Builder */}
        <div className="questions-panel">
          <div className="questions-header">
            <h3>📝 Savollar ro'yxati ({questions.length})</h3>
            <button className="btn-add-q" onClick={addQuestion}>+ Yangi savol</button>
          </div>

          <div className="questions-list">
            {questions.map((q, index) => (
              <div className="question-card" key={q.id}>
                <div className="q-header">
                  <span className="q-number">{q.order_number}-savol</span>
                  {questions.length > 1 && (
                    <button className="btn-remove-q" onClick={() => removeQuestion(q.id)}>🗑 O'chirish</button>
                  )}
                </div>

                <div className="q-body">
                  <textarea 
                    className="q-text"
                    placeholder="Savol matnini kiriting..."
                    value={q.question_text}
                    onChange={(e) => handleQuestionChange(q.id, 'question_text', e.target.value)}
                  />

                  <div className="options-grid">
                    {['A', 'B', 'C', 'D'].map(opt => (
                      <div className={`option-row ${q.correct_answer === opt ? 'is-correct' : ''}`} key={opt}>
                        <div className="radio-wrapper" onClick={() => handleQuestionChange(q.id, 'correct_answer', opt)}>
                          <div className={`custom-radio ${q.correct_answer === opt ? 'checked' : ''}`}></div>
                          <span>{opt}</span>
                        </div>
                        <input 
                          type="text" 
                          placeholder={`${opt} varianti...`} 
                          value={q[`option_${opt.toLowerCase()}`]}
                          onChange={(e) => handleQuestionChange(q.id, `option_${opt.toLowerCase()}`, e.target.value)}
                        />
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
