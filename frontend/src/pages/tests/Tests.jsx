import React, { useState, useEffect, useMemo } from 'react'
import { useNavigate } from 'react-router-dom'
import { Trash2, ChevronDown, ChevronUp, Clock, HelpCircle, CalendarDays, X, Plus } from 'lucide-react'
import { API_BASE } from '../../config'
import './Tests.css'

const SUBJECTS_ORDER = ['Matematika', 'Ingliz-tili', 'Rus-tili']
const SUBJECT_LABELS = {
  'Matematika': 'Matematika',
  'Ingliz-tili': 'Ingliz tili',
  'Rus-tili': 'Rus tili',
}
const SUBJECT_ICONS = {
  'Matematika': '🔢',
  'Ingliz-tili': '🇬🇧',
  'Rus-tili': '🇷🇺',
}
const SUBJECT_COLORS = {
  'Matematika': 'subject-math',
  'Ingliz-tili': 'subject-english',
  'Rus-tili': 'subject-russian',
}
const GRADES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

export default function Tests() {
  const [tests, setTests] = useState([])
  const [loading, setLoading] = useState(true)
  const [showPast, setShowPast] = useState(false)
  const [selectedTest, setSelectedTest] = useState(null)
  const [confirmDeleteId, setConfirmDeleteId] = useState(null)
  const [deleting, setDeleting] = useState(false)
  const navigate = useNavigate()

  useEffect(() => {
    fetchTests()
  }, [])

  const fetchTests = async () => {
    setLoading(true)
    try {
      const res = await fetch(`${API_BASE}/tests/list/`)
      const data = await res.json()
      setTests(Array.isArray(data) ? data : [])
    } catch (e) {
      console.error(e)
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (id) => {
    setDeleting(true)
    try {
      const res = await fetch(`${API_BASE}/tests/list/${id}/`, { method: 'DELETE' })
      if (res.ok || res.status === 204) {
        setConfirmDeleteId(null)
        setSelectedTest(null)
        fetchTests()
      }
    } catch (e) {
      console.error(e)
    } finally {
      setDeleting(false)
    }
  }

  // Group tests by date
  const { upcomingGroups, pastGroups, stats } = useMemo(() => {
    const today = new Date()
    today.setHours(0, 0, 0, 0)

    // Group by date string (YYYY-MM-DD)
    const dateMap = {}
    tests.forEach(t => {
      const dateStr = t.start_datetime ? t.start_datetime.slice(0, 10) : 'unknown'
      if (!dateMap[dateStr]) dateMap[dateStr] = []
      dateMap[dateStr].push(t)
    })

    const upcoming = []
    const past = []

    Object.keys(dateMap).sort().reverse().forEach(dateStr => {
      const dateObj = new Date(dateStr + 'T00:00:00')
      const group = {
        dateStr,
        dateObj,
        tests: dateMap[dateStr],
        label: formatDateLabel(dateStr),
      }
      if (dateObj >= today) {
        upcoming.push(group)
      } else {
        past.push(group)
      }
    })

    // Sort upcoming ascending (closest first), past descending (most recent first)
    upcoming.sort((a, b) => a.dateObj - b.dateObj)
    past.sort((a, b) => b.dateObj - a.dateObj)

    return {
      upcomingGroups: upcoming,
      pastGroups: past,
      stats: {
        total: tests.length,
        upcomingDates: upcoming.length,
        pastDates: past.length,
      }
    }
  }, [tests])

  return (
    <div className="tests-page">
      {/* Header */}
      <div className="tests-header">
        <div className="tests-title-row">
          <div className="tests-title">
            <span className="tests-icon">📝</span>
            <div>
              <h1>Testlar bazasi</h1>
              <p>
                {stats.total} ta test • {stats.upcomingDates + stats.pastDates} ta olimpiada sanasi
              </p>
            </div>
          </div>
          <button className="btn-add-test" onClick={() => navigate('/tests/new')}>
            <Plus size={18} />
            <span>Yangi test qo'shish</span>
          </button>
        </div>
      </div>

      {loading ? (
        <div className="tests-loading">
          <div className="spinner-big"></div>
          <p>Testlar yuklanmoqda...</p>
        </div>
      ) : tests.length === 0 ? (
        <div className="tests-empty">
          <div className="empty-icon">📭</div>
          <h3>Hozircha testlar yo'q</h3>
          <p>Yangi test qo'shish tugmasini bosing</p>
        </div>
      ) : (
        <div className="tests-content">
          {/* Upcoming Olympiads */}
          {upcomingGroups.length > 0 && (
            <div className="tests-section">
              <div className="section-label upcoming-label">
                <CalendarDays size={18} />
                <span>Kelayotgan olimpiadalar ({upcomingGroups.length})</span>
              </div>
              {upcomingGroups.map(group => (
                <DateGroup
                  key={group.dateStr}
                  group={group}
                  isPast={false}
                  onTestClick={setSelectedTest}
                />
              ))}
            </div>
          )}

          {/* Past Olympiads */}
          {pastGroups.length > 0 && (
            <div className="tests-section past-section">
              <button
                className={`section-toggle ${showPast ? 'open' : ''}`}
                onClick={() => setShowPast(!showPast)}
              >
                <div className="section-label past-label">
                  <CalendarDays size={18} />
                  <span>O'tgan olimpiadalar ({pastGroups.length})</span>
                </div>
                {showPast ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
              </button>

              {showPast && (
                <div className="past-groups-container">
                  {pastGroups.map(group => (
                    <DateGroup
                      key={group.dateStr}
                      group={group}
                      isPast={true}
                      onTestClick={setSelectedTest}
                    />
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      )}

      {/* Test Detail Modal */}
      {selectedTest && (
        <div className="modal-overlay" onClick={() => { setSelectedTest(null); setConfirmDeleteId(null) }}>
          <div className="modal-card" onClick={e => e.stopPropagation()}>
            <button className="modal-close" onClick={() => { setSelectedTest(null); setConfirmDeleteId(null) }}>
              <X size={20} />
            </button>

            <div className="modal-test-header">
              <span className={`modal-subject-badge ${SUBJECT_COLORS[selectedTest.subject_name]}`}>
                {SUBJECT_ICONS[selectedTest.subject_name]} {SUBJECT_LABELS[selectedTest.subject_name] || selectedTest.subject_name}
              </span>
              <span className="modal-grade-badge">{selectedTest.grade}-sinf</span>
            </div>

            <h2 className="modal-test-title">{selectedTest.title}</h2>

            <div className="modal-test-details">
              <div className="modal-detail-item">
                <Clock size={16} />
                <span>Davomiyligi: <strong>{selectedTest.duration_minutes} daqiqa</strong></span>
              </div>
              <div className="modal-detail-item">
                <HelpCircle size={16} />
                <span>Savollar soni: <strong>{selectedTest.questions?.length || 0} ta</strong></span>
              </div>
              <div className="modal-detail-item">
                <CalendarDays size={16} />
                <span>Boshlanish: <strong>{formatDt(selectedTest.start_datetime)}</strong></span>
              </div>
              <div className="modal-detail-item">
                <CalendarDays size={16} />
                <span>Tugash: <strong>{formatDt(selectedTest.end_datetime)}</strong></span>
              </div>
            </div>

            {selectedTest.questions && selectedTest.questions.length > 0 && (
              <div className="modal-questions-preview">
                <h4>Savollar ({selectedTest.questions.length} ta)</h4>
                <div className="questions-mini-list">
                  {selectedTest.questions.map((q, i) => (
                    <div className="question-mini" key={q.id}>
                      <span className="q-mini-num">{q.order_number}.</span>
                      <span className="q-mini-text">{q.question_text}</span>
                      <span className="q-mini-answer">✓ {q.correct_answer}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            <div className="modal-actions">
              {confirmDeleteId === selectedTest.id ? (
                <div className="confirm-delete-modal">
                  <span>Rostdan bu testni o'chirasizmi?</span>
                  <div className="confirm-btns">
                    <button className="btn-confirm-yes" onClick={() => handleDelete(selectedTest.id)} disabled={deleting}>
                      {deleting ? 'O\'chirilmoqda...' : 'Ha, o\'chirish'}
                    </button>
                    <button className="btn-confirm-no" onClick={() => setConfirmDeleteId(null)}>Yo'q</button>
                  </div>
                </div>
              ) : (
                <button className="btn-delete-modal" onClick={() => setConfirmDeleteId(selectedTest.id)}>
                  <Trash2 size={16} />
                  O'chirish
                </button>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

// ─── DateGroup Component ───────────────────────────────────────────

function DateGroup({ group, isPast, onTestClick }) {
  // Build a lookup: subject_name -> grade -> test
  const testLookup = useMemo(() => {
    const lookup = {}
    group.tests.forEach(t => {
      const subj = t.subject_name
      if (!lookup[subj]) lookup[subj] = {}
      lookup[subj][t.grade] = t
    })
    return lookup
  }, [group.tests])

  // Count tests per subject
  const subjectCounts = SUBJECTS_ORDER.map(s => ({
    name: s,
    count: testLookup[s] ? Object.keys(testLookup[s]).length : 0
  }))

  return (
    <div className={`date-group ${isPast ? 'past' : 'upcoming'}`}>
      <div className="date-group-header">
        <div className="date-label-container">
          <span className="date-emoji">📅</span>
          <div>
            <h3 className="date-heading">{group.label}</h3>
            <p className="date-summary">
              {group.tests.length} ta test •{' '}
              {subjectCounts.filter(s => s.count > 0).map(s =>
                `${SUBJECT_LABELS[s.name] || s.name}: ${s.count}`
              ).join(' • ')}
            </p>
          </div>
        </div>
      </div>

      <div className="subjects-grid">
        {SUBJECTS_ORDER.map(subjectName => {
          const subjectTests = testLookup[subjectName] || {}
          const hasAny = Object.keys(subjectTests).length > 0

          return (
            <div className={`subject-column ${SUBJECT_COLORS[subjectName]}`} key={subjectName}>
              <div className="subject-column-header">
                <span className="subject-icon">{SUBJECT_ICONS[subjectName]}</span>
                <span className="subject-name">{SUBJECT_LABELS[subjectName] || subjectName}</span>
                <span className="subject-count">
                  {Object.keys(subjectTests).length}/11
                </span>
              </div>

              <div className="grades-list">
                {GRADES.map(grade => {
                  const test = subjectTests[grade]
                  return (
                    <div
                      className={`grade-slot ${test ? 'has-test' : 'empty'}`}
                      key={grade}
                      onClick={() => test && onTestClick(test)}
                      title={test ? `${test.title} — ${test.questions?.length || 0} ta savol` : `${grade}-sinf uchun test qo'shilmagan`}
                    >
                      <span className="grade-num">{grade}-sinf</span>
                      {test ? (
                        <div className="grade-info">
                          <span className="grade-questions">{test.questions?.length || 0} savol</span>
                          <span className="grade-time">{test.duration_minutes}′</span>
                        </div>
                      ) : (
                        <span className="grade-empty-mark">—</span>
                      )}
                    </div>
                  )
                })}
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}

// ─── Helper Functions ──────────────────────────────────────────────

function formatDateLabel(dateStr) {
  const months = [
    'yanvar', 'fevral', 'mart', 'aprel', 'may', 'iyun',
    'iyul', 'avgust', 'sentabr', 'oktabr', 'noyabr', 'dekabr'
  ]
  const d = new Date(dateStr + 'T00:00:00')
  return `${d.getDate()}-${months[d.getMonth()]}, ${d.getFullYear()}-yil`
}

function formatDt(dt) {
  if (!dt) return '—'
  return new Date(dt).toLocaleString('uz-UZ', {
    day: '2-digit', month: '2-digit', year: 'numeric',
    hour: '2-digit', minute: '2-digit'
  })
}
