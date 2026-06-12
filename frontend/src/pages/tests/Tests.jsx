import React, { useState, useEffect, useMemo } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  Trash2, ChevronDown, ChevronUp, Clock, HelpCircle,
  CalendarDays, X, Plus, Users, Sparkles, ArrowRight, History, Hourglass,
  Pencil, Save, AlertTriangle, CalendarPlus
} from 'lucide-react'
import { authFetch } from '../../config'
import './Tests.css'

const SUBJECTS_ORDER = ['Matematika', 'Ingliz tili', 'Rus tili']
const SUBJECT_LABELS = {
  'Matematika': 'Matematika',
  'Ingliz tili': 'Ingliz tili',
  'Rus tili': 'Rus tili',
}
const SUBJECT_ICONS = {
  'Matematika': '🔢',
  'Ingliz tili': '🇬🇧',
  'Rus tili': '🇷🇺',
}
const SUBJECT_COLORS = {
  'Matematika': 'subject-math',
  'Ingliz tili': 'subject-english',
  'Rus tili': 'subject-russian',
}
const GRADES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

const AVATAR_GRADIENTS = [
  'linear-gradient(135deg, #6366f1 0%, #a855f7 100%)',
  'linear-gradient(135deg, #ec4899 0%, #f43f5e 100%)',
  'linear-gradient(135deg, #0ea5e9 0%, #6366f1 100%)',
  'linear-gradient(135deg, #14b8a6 0%, #0ea5e9 100%)',
  'linear-gradient(135deg, #f59e0b 0%, #ef4444 100%)',
  'linear-gradient(135deg, #10b981 0%, #14b8a6 100%)',
  'linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%)',
  'linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%)',
]
const getAvatarGradient = (name) => {
  if (!name) return AVATAR_GRADIENTS[0]
  return AVATAR_GRADIENTS[(name.charCodeAt(0) || 0) % AVATAR_GRADIENTS.length]
}

export default function Tests() {
  const [tests, setTests] = useState([])
  const [participants, setParticipants] = useState([])
  const [subjects, setSubjects] = useState([])
  const [loading, setLoading] = useState(true)
  const [showPast, setShowPast] = useState(false)
  const [selectedTest, setSelectedTest] = useState(null)
  const [confirmDeleteId, setConfirmDeleteId] = useState(null)
  const [deleting, setDeleting] = useState(false)
  const [editDateOpen, setEditDateOpen] = useState(false)
  const [newDate, setNewDate] = useState('')
  const [newStartTime, setNewStartTime] = useState('')
  const [newEndTime, setNewEndTime] = useState('')
  const [rescheduling, setRescheduling] = useState(false)
  const [rescheduleError, setRescheduleError] = useState('')
  // "Assign date to undated (AI) tests" modal
  const [scheduleOpen, setScheduleOpen] = useState(false)
  const [schedDate, setSchedDate] = useState('')
  const [schedStart, setSchedStart] = useState('09:00:00')
  const [schedEnd, setSchedEnd] = useState('23:59:00')
  const [scheduling, setScheduling] = useState(false)
  const [scheduleError, setScheduleError] = useState('')
  const navigate = useNavigate()

  useEffect(() => {
    fetchAll()
  }, [])

  const fetchAll = async () => {
    setLoading(true)
    try {
      const [testsRes, partRes, subjectsRes] = await Promise.all([
        authFetch('/tests/list/'),
        authFetch('/registration/participants/'),
        authFetch('/tests/subjects/')
      ])
      const testsData = await testsRes.json()
      const partData = await partRes.json()
      const subjectsData = await subjectsRes.json()
      setTests(Array.isArray(testsData) ? testsData : [])
      setSubjects(Array.isArray(subjectsData) ? subjectsData : [])
      const partList = Array.isArray(partData) ? partData : (partData.results || [])
      setParticipants(partList.filter(p => p.verification_status === 'approved'))
    } catch (e) {
      console.error(e)
    } finally {
      setLoading(false)
    }
  }

  const openEditDate = (currentDateStr) => {
    setNewDate(currentDateStr)
    // Pre-fill start/end time from first test on this date (if any)
    const firstTest = upcomingGroup?.tests?.[0]
    if (firstTest?.start_datetime) {
      setNewStartTime(extractTimeHMS(firstTest.start_datetime))
    } else {
      setNewStartTime('')
    }
    if (firstTest?.end_datetime) {
      setNewEndTime(extractTimeHMS(firstTest.end_datetime))
    } else {
      setNewEndTime('')
    }
    setRescheduleError('')
    setEditDateOpen(true)
  }

  const handleReschedule = async () => {
    if (!newDate || !upcomingGroup) return
    setRescheduling(true)
    setRescheduleError('')
    try {
      const payload = {
        from_date: upcomingGroup.dateStr,
        to_date: newDate,
      }
      if (newStartTime) payload.start_time = newStartTime
      if (newEndTime) payload.end_time = newEndTime
      const res = await authFetch('/tests/list/reschedule/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
      if (res.ok) {
        setEditDateOpen(false)
        await fetchAll()
      } else {
        const err = await res.json()
        setRescheduleError(err.error || "Xatolik yuz berdi")
      }
    } catch (e) {
      console.error(e)
      setRescheduleError("Tarmoq xatosi")
    } finally {
      setRescheduling(false)
    }
  }

  const openScheduleUndated = () => {
    // Pre-fill with the existing upcoming date if there is one (so AI tests join it)
    setSchedDate(upcomingGroup?.dateStr || '')
    setSchedStart('09:00:00')
    setSchedEnd('23:59:00')
    setScheduleError('')
    setScheduleOpen(true)
  }

  const handleScheduleUndated = async () => {
    if (!schedDate) return
    setScheduling(true)
    setScheduleError('')
    try {
      const res = await authFetch('/tests/list/schedule-undated/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          to_date: schedDate,
          start_time: schedStart || undefined,
          end_time: schedEnd || undefined,
        })
      })
      if (res.ok) {
        setScheduleOpen(false)
        await fetchAll()
      } else {
        const err = await res.json()
        setScheduleError(err.error || "Xatolik yuz berdi")
      }
    } catch (e) {
      console.error(e)
      setScheduleError("Tarmoq xatosi")
    } finally {
      setScheduling(false)
    }
  }

  const handleDelete = async (id) => {
    setDeleting(true)
    try {
      const res = await authFetch(`/tests/list/${id}/`, { method: 'DELETE' })
      if (res.ok || res.status === 204) {
        setConfirmDeleteId(null)
        setSelectedTest(null)
        fetchAll()
      }
    } catch (e) {
      console.error(e)
    } finally {
      setDeleting(false)
    }
  }

  const subjectsById = useMemo(() => {
    const map = {}
    subjects.forEach(s => { map[s.name] = s.id })
    return map
  }, [subjects])

  const { upcomingGroup, pastGroups, pendingParticipants, hasUpcoming, undatedTests } = useMemo(() => {
    const today = new Date()
    today.setHours(0, 0, 0, 0)

    // Group tests by date
    const dateMap = {}
    tests.forEach(t => {
      const dateStr = t.start_datetime ? t.start_datetime.slice(0, 10) : 'unknown'
      if (!dateMap[dateStr]) dateMap[dateStr] = []
      dateMap[dateStr].push(t)
    })

    let upcoming = null
    const past = []

    Object.keys(dateMap).sort().forEach(dateStr => {
      if (dateStr === 'unknown') return
      const dateObj = new Date(dateStr + 'T00:00:00')
      const group = {
        dateStr,
        dateObj,
        tests: dateMap[dateStr],
        label: formatDateLabel(dateStr),
      }
      if (dateObj >= today) {
        if (!upcoming || dateObj < upcoming.dateObj) {
          upcoming = group
        }
      } else {
        past.push(group)
      }
    })
    past.sort((a, b) => b.dateObj - a.dateObj)

    // Attach participants to each date group
    const byDate = {}
    participants.forEach(p => {
      const d = p.target_test_date
      if (!d) return
      if (!byDate[d]) byDate[d] = []
      byDate[d].push(p)
    })

    if (upcoming) upcoming.participants = byDate[upcoming.dateStr] || []
    past.forEach(g => { g.participants = byDate[g.dateStr] || [] })

    const pending = participants.filter(p => !p.target_test_date)

    return {
      upcomingGroup: upcoming,
      pastGroups: past,
      pendingParticipants: pending,
      hasUpcoming: !!upcoming,
      undatedTests: dateMap['unknown'] || [],
    }
  }, [tests, participants])

  return (
    <div className="tests-page">
      {/* Header */}
      <div className="tests-header">
        <div className="tests-title-row">
          <div className="tests-title">
            <span className="tests-icon">
              <Sparkles size={26} strokeWidth={2.2} />
            </span>
            <div>
              <h1>Testlar bazasi</h1>
              <p>
                {tests.length} ta test · {participants.length} ta tasdiqlangan ishtirokchi
                {pendingParticipants.length > 0 && (
                  <> · <strong style={{ color: '#d97706' }}>{pendingParticipants.length}</strong> sana kutmoqda</>
                )}
              </p>
            </div>
          </div>
          <button
            className="btn-add-test"
            onClick={() => navigate('/tests/new')}
            title={hasUpcoming ? "Mavjud kelajakdagi olimpiada sanasi uchun yangi savollar qo'shish" : "Yangi olimpiada sanasini boshlash"}
          >
            <Plus size={18} />
            <span>{hasUpcoming ? "Test qo'shish" : "Yangi olimpiada"}</span>
          </button>
        </div>
      </div>

      {loading ? (
        <div className="tests-loading">
          <div className="spinner-big"></div>
          <p>Ma'lumotlar yuklanmoqda...</p>
        </div>
      ) : (
        <div className="tests-content">
          {/* Undated (AI-imported) tests — no start_datetime, so invisible until scheduled */}
          {undatedTests.length > 0 && (
            <div className="undated-block">
              <div className="undated-banner">
                <div className="undated-banner-left">
                  <div className="undated-icon">
                    <AlertTriangle size={24} strokeWidth={2.2} />
                  </div>
                  <div>
                    <h3>Sana belgilanmagan testlar</h3>
                    <p>
                      {undatedTests.length} ta test (AI orqali qo'shilgan) sanasi yo'qligi uchun ishtirokchilarga ko'rinmayapti.
                      Olimpiada sanasini belgilang — shunda ular faollashadi.
                    </p>
                  </div>
                </div>
                <button className="btn-schedule-undated" onClick={openScheduleUndated}>
                  <CalendarPlus size={17} />
                  <span>Sana belgilash</span>
                </button>
              </div>
              <DateGroupView
                group={{ tests: undatedTests }}
                isPast={false}
                onTestClick={setSelectedTest}
              />
            </div>
          )}

          {/* Pending participants pool — when no future date exists */}
          {pendingParticipants.length > 0 && !hasUpcoming && (
            <div className="pending-pool-card">
              <div className="pending-pool-header">
                <Hourglass size={20} strokeWidth={2.2} />
                <div>
                  <h3>Sana belgilangani kutilmoqda</h3>
                  <p>{pendingParticipants.length} ta ishtirokchi olimpiada sanasi belgilanishini kutmoqda — yangi sana qo'yganingizda avtomatik shu sanaga belgilanadi</p>
                </div>
              </div>
              <ParticipantsList participants={pendingParticipants} compact />
            </div>
          )}

          {/* Upcoming Olympiad — Main featured block */}
          {upcomingGroup ? (
            <div className="upcoming-block">
              <div className="upcoming-banner">
                <div className="banner-bg-decor" />
                <div className="banner-content">
                  <div className="banner-left">
                    <div className="banner-icon">
                      <CalendarDays size={28} strokeWidth={2.2} />
                    </div>
                    <div>
                      <span className="banner-eyebrow">
                        <Sparkles size={13} />
                        Kelajakdagi olimpiada
                      </span>
                      <h2 className="banner-date">
                        {upcomingGroup.label}
                        <button
                          className="banner-edit-btn"
                          onClick={() => openEditDate(upcomingGroup.dateStr)}
                          title="Olimpiada sanasini o'zgartirish"
                        >
                          <Pencil size={14} />
                        </button>
                      </h2>
                      <div className="banner-meta">
                        <span>{upcomingGroup.tests.length} ta test tayyor</span>
                        <span className="banner-dot">·</span>
                        <span><strong>{upcomingGroup.participants.length}</strong> ta ishtirokchi</span>
                      </div>
                    </div>
                  </div>
                  <div className="banner-countdown">
                    <CountdownPill targetDate={upcomingGroup.dateObj} />
                  </div>
                </div>
              </div>

              <DateGroupView
                group={upcomingGroup}
                isPast={false}
                onTestClick={setSelectedTest}
                onEmptyClick={(subjectName, grade) => {
                  const subjectId = subjectsById[subjectName]
                  const params = new URLSearchParams()
                  if (subjectId) params.set('subject', subjectId)
                  params.set('grade', String(grade))
                  params.set('date', upcomingGroup.dateStr)
                  navigate(`/tests/new?${params.toString()}`)
                }}
              />

              <ParticipantsSection
                title="Ushbu olimpiadaga yozilganlar"
                participants={upcomingGroup.participants}
                emptyText="Hozircha hech kim yozilmagan"
              />
            </div>
          ) : (
            <div className="no-upcoming-card">
              <CalendarDays size={48} strokeWidth={1.5} />
              <h3>Kelajakdagi olimpiada belgilanmagan</h3>
              <p>"Yangi olimpiada" tugmasini bosib, kelajakdagi sana uchun testlar qo'shing. Botda ro'yxatdan o'tgan barcha ishtirokchilar avtomatik shu sanaga belgilanadi.</p>
            </div>
          )}

          {/* Past Olympiads */}
          {pastGroups.length > 0 && (
            <div className="past-section">
              <button
                className={`past-toggle ${showPast ? 'open' : ''}`}
                onClick={() => setShowPast(!showPast)}
              >
                <div className="past-toggle-left">
                  <History size={20} strokeWidth={2.2} />
                  <span>O'tgan olimpiadalar ({pastGroups.length})</span>
                </div>
                {showPast ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
              </button>

              {showPast && (
                <div className="past-groups">
                  {pastGroups.map(group => (
                    <div className="past-event" key={group.dateStr}>
                      <div className="past-event-header">
                        <div className="past-event-icon">
                          <CalendarDays size={22} />
                        </div>
                        <div>
                          <h3>{group.label}</h3>
                          <p>{group.tests.length} ta test · {group.participants.length} ta qatnashgan</p>
                        </div>
                      </div>
                      <DateGroupView group={group} isPast={true} onTestClick={setSelectedTest} />
                      <ParticipantsSection
                        title="Qatnashganlar"
                        participants={group.participants}
                        emptyText="Bu sanaga biriktirilgan ishtirokchi yo'q"
                        compact
                      />
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {tests.length === 0 && !hasUpcoming && (
            <div className="tests-empty">
              <div className="empty-icon">📭</div>
              <h3>Hozircha testlar yo'q</h3>
              <p>Yangi olimpiada uchun testlar qo'shing</p>
            </div>
          )}
        </div>
      )}

      {/* Edit Date Modal */}
      {editDateOpen && upcomingGroup && (
        <div className="modal-overlay" onClick={() => !rescheduling && setEditDateOpen(false)}>
          <div className="reschedule-modal-card" onClick={e => e.stopPropagation()}>
            <button className="modal-close" onClick={() => !rescheduling && setEditDateOpen(false)}>
              <X size={20} />
            </button>
            <div className="reschedule-modal-icon">
              <CalendarDays size={28} />
            </div>
            <h3 className="reschedule-modal-title">Olimpiada sanasini o'zgartirish</h3>
            <p className="reschedule-modal-text">
              Joriy sana: <strong>{upcomingGroup.label}</strong>
            </p>
            <p className="reschedule-modal-hint">
              {upcomingGroup.tests.length} ta test va {upcomingGroup.participants.length} ta ishtirokchi yangi sanaga ko'chiriladi.
            </p>

            <div className="reschedule-input-group">
              <label>Yangi sana</label>
              <input
                type="date"
                value={newDate}
                onChange={e => { setNewDate(e.target.value); setRescheduleError('') }}
                min={new Date().toISOString().slice(0, 10)}
                disabled={rescheduling}
                autoFocus
              />
            </div>

            <div className="reschedule-time-row">
              <div className="reschedule-input-group">
                <label>⏱ Boshlanish vaqti</label>
                <input
                  type="time"
                  step="1"
                  value={newStartTime}
                  onChange={e => { setNewStartTime(e.target.value); setRescheduleError('') }}
                  disabled={rescheduling}
                />
              </div>
              <div className="reschedule-input-group">
                <label>🏁 Tugash vaqti</label>
                <input
                  type="time"
                  step="1"
                  value={newEndTime}
                  onChange={e => { setNewEndTime(e.target.value); setRescheduleError('') }}
                  disabled={rescheduling}
                />
              </div>
            </div>
            <p className="reschedule-time-hint">
              Vaqtlar bo'sh qoldirilsa, har bir testning eski vaqti saqlanadi
            </p>

            {rescheduleError && (
              <div className="reschedule-error">{rescheduleError}</div>
            )}

            <div className="reschedule-modal-actions">
              <button
                className="btn-cancel-resched"
                onClick={() => setEditDateOpen(false)}
                disabled={rescheduling}
              >
                Bekor qilish
              </button>
              <button
                className="btn-save-resched"
                onClick={handleReschedule}
                disabled={rescheduling || !newDate}
              >
                {rescheduling ? (
                  <>Ko'chirilmoqda...</>
                ) : (
                  <>
                    <Save size={15} />
                    Saqlash
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Schedule Undated Tests Modal */}
      {scheduleOpen && (
        <div className="modal-overlay" onClick={() => !scheduling && setScheduleOpen(false)}>
          <div className="reschedule-modal-card" onClick={e => e.stopPropagation()}>
            <button className="modal-close" onClick={() => !scheduling && setScheduleOpen(false)}>
              <X size={20} />
            </button>
            <div className="reschedule-modal-icon">
              <CalendarPlus size={28} />
            </div>
            <h3 className="reschedule-modal-title">Testlarga sana belgilash</h3>
            <p className="reschedule-modal-hint">
              {undatedTests.length} ta sanasiz test tanlangan sanaga biriktiriladi.
              O'tgan sana bo'lsa — faqat shu testlarni topshirganlar shu olimpiadaga ulanadi;
              yangi yozilganlar keyingi olimpiadani kutib turadi.
            </p>

            <div className="reschedule-input-group">
              <label>Olimpiada sanasi</label>
              <input
                type="date"
                value={schedDate}
                onChange={e => { setSchedDate(e.target.value); setScheduleError('') }}
                disabled={scheduling}
                autoFocus
              />
              <p className="sched-date-note">
                O'tgan sanani ham tanlash mumkin — bunda testlar "O'tgan olimpiadalar"ga o'tadi
                va topshirganlar "qatnashgan" bo'ladi.
              </p>
            </div>

            <div className="reschedule-time-row">
              <div className="reschedule-input-group">
                <label>⏱ Boshlanish vaqti</label>
                <input
                  type="time"
                  step="1"
                  value={schedStart}
                  onChange={e => { setSchedStart(e.target.value); setScheduleError('') }}
                  disabled={scheduling}
                />
              </div>
              <div className="reschedule-input-group">
                <label>🏁 Tugash vaqti</label>
                <input
                  type="time"
                  step="1"
                  value={schedEnd}
                  onChange={e => { setSchedEnd(e.target.value); setScheduleError('') }}
                  disabled={scheduling}
                />
              </div>
            </div>
            <p className="reschedule-time-hint">
              Ishtirokchilar shu vaqt oralig'ida test topshira oladi
            </p>

            {scheduleError && (
              <div className="reschedule-error">{scheduleError}</div>
            )}

            <div className="reschedule-modal-actions">
              <button
                className="btn-cancel-resched"
                onClick={() => setScheduleOpen(false)}
                disabled={scheduling}
              >
                Bekor qilish
              </button>
              <button
                className="btn-save-resched"
                onClick={handleScheduleUndated}
                disabled={scheduling || !schedDate}
              >
                {scheduling ? (
                  <>Belgilanmoqda...</>
                ) : (
                  <>
                    <CalendarPlus size={15} />
                    Sanani belgilash
                  </>
                )}
              </button>
            </div>
          </div>
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
                  {selectedTest.questions.map((q) => (
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
                      {deleting ? "O'chirilmoqda..." : "Ha, o'chirish"}
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

// ─── DateGroupView (renders the subjects × grades grid for one date) ───
function DateGroupView({ group, isPast, onTestClick, onEmptyClick }) {
  const testLookup = useMemo(() => {
    const lookup = {}
    group.tests.forEach(t => {
      const subj = t.subject_name
      if (!lookup[subj]) lookup[subj] = {}
      lookup[subj][t.grade] = t
    })
    return lookup
  }, [group.tests])

  return (
    <div className={`date-group ${isPast ? 'past' : 'upcoming'}`}>
      <div className="subjects-grid">
        {SUBJECTS_ORDER.map(subjectName => {
          const subjectTests = testLookup[subjectName] || {}

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
                  const canCreate = !test && !isPast && onEmptyClick
                  return (
                    <div
                      className={`grade-slot ${test ? 'has-test' : 'empty'} ${canCreate ? 'clickable-empty' : ''}`}
                      key={grade}
                      onClick={() => {
                        if (test) return onTestClick(test)
                        if (canCreate) onEmptyClick(subjectName, grade)
                      }}
                      title={
                        test
                          ? `${test.title} — ${test.questions?.length || 0} ta savol`
                          : canCreate
                            ? `${SUBJECT_LABELS[subjectName] || subjectName} · ${grade}-sinf uchun test qo'shish`
                            : `${grade}-sinf uchun test qo'shilmagan`
                      }
                    >
                      <span className="grade-num">{grade}-sinf</span>
                      {test ? (
                        <div className="grade-info">
                          <span className="grade-questions">{test.questions?.length || 0} savol</span>
                          <span className="grade-time">{test.duration_minutes}′</span>
                        </div>
                      ) : canCreate ? (
                        <span className="grade-add-mark">+</span>
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

// ─── Participants Section (with divider + list) ───
function ParticipantsSection({ title, participants, emptyText, compact = false }) {
  return (
    <div className="participants-section">
      <div className="participants-divider">
        <span className="divider-line" />
        <span className="divider-label">
          <Users size={14} />
          {title}
          {participants.length > 0 && <strong>({participants.length})</strong>}
        </span>
        <span className="divider-line" />
      </div>
      {participants.length === 0 ? (
        <div className="participants-empty">{emptyText}</div>
      ) : (
        <ParticipantsList participants={participants} compact={compact} />
      )}
    </div>
  )
}

function ParticipantsList({ participants, compact = false }) {
  return (
    <div className={`participants-grid ${compact ? 'compact' : ''}`}>
      {participants.map(p => (
        <div className="participant-card" key={p.id}>
          <div
            className="participant-avatar"
            style={{ background: getAvatarGradient(p.full_name) }}
          >
            {p.full_name?.[0]?.toUpperCase() || '?'}
          </div>
          <div className="participant-info">
            <span className="participant-name">{p.full_name}</span>
            <div className="participant-meta">
              <span className="p-meta-tag">{p.grade}-sinf</span>
              <span className="p-meta-subject">{p.subject}</span>
            </div>
            <span className="participant-phone">{p.phone}</span>
          </div>
          {p.unique_code && (
            <span className="participant-code">{p.unique_code}</span>
          )}
        </div>
      ))}
    </div>
  )
}

// ─── Countdown ───
function CountdownPill({ targetDate }) {
  const diff = Math.ceil((targetDate - new Date()) / (1000 * 60 * 60 * 24))
  if (diff <= 0) return <span className="countdown-pill today">Bugun!</span>
  if (diff === 1) return <span className="countdown-pill soon">Ertaga</span>
  return (
    <span className="countdown-pill">
      <strong>{diff}</strong> kun qoldi
      <ArrowRight size={14} />
    </span>
  )
}

// ─── Helpers ───
function formatDateLabel(dateStr) {
  const months = [
    'yanvar', 'fevral', 'mart', 'aprel', 'may', 'iyun',
    'iyul', 'avgust', 'sentabr', 'oktabr', 'noyabr', 'dekabr'
  ]
  const d = new Date(dateStr + 'T00:00:00')
  return `${d.getDate()}-${months[d.getMonth()]}, ${d.getFullYear()}-yil`
}

function extractTimeHMS(isoString) {
  if (!isoString) return ''
  const d = new Date(isoString)
  const hh = String(d.getHours()).padStart(2, '0')
  const mm = String(d.getMinutes()).padStart(2, '0')
  const ss = String(d.getSeconds()).padStart(2, '0')
  return `${hh}:${mm}:${ss}`
}

function formatDt(dt) {
  if (!dt) return '—'
  return new Date(dt).toLocaleString('uz-UZ', {
    day: '2-digit', month: '2-digit', year: 'numeric',
    hour: '2-digit', minute: '2-digit'
  })
}
