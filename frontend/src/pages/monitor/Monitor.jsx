import React, { useState, useEffect, useCallback } from 'react'
import { API_BASE } from '../../config'
import './Monitor.css'

const SUBJECTS = ['Barcha fanlar', 'Matematika', 'Ingliz tili', 'Rus tili']
const GRADES = ['Barcha sinflar', ...Array.from({ length: 11 }, (_, i) => `${i + 1}`)]
const STATUS_TABS = [
  { key: '', label: 'Hammasi' },
  { key: 'entered', label: 'Kirganlar' },
  { key: 'not_entered', label: 'Kirmaganlar' },
]
const BADGE = {
  not_entered: { text: 'Kirmadi', cls: 'b-red' },
  started: { text: 'Kirdi', cls: 'b-green' },
  in_progress: { text: 'Ishlayapti', cls: 'b-blue' },
  completed: { text: 'Tugatdi', cls: 'b-gray' },
}

export default function Monitor() {
  const [rows, setRows] = useState([])
  const [summary, setSummary] = useState({ total: 0, entered_count: 0, not_entered_count: 0 })
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [grade, setGrade] = useState('Barcha sinflar')
  const [subject, setSubject] = useState('Barcha fanlar')
  const [status, setStatus] = useState('')
  const [updatedAt, setUpdatedAt] = useState(null)

  const fetchData = useCallback(async () => {
    const params = new URLSearchParams()
    if (search) params.append('search', search)
    if (grade !== 'Barcha sinflar') params.append('grade', grade)
    if (subject !== 'Barcha fanlar') params.append('subject', subject)
    if (status) params.append('status', status)
    try {
      const res = await fetch(`${API_BASE}/results/attendance/?${params.toString()}`)
      if (res.ok) {
        const data = await res.json()
        setRows(data.results || [])
        setSummary({
          total: data.total || 0,
          entered_count: data.entered_count || 0,
          not_entered_count: data.not_entered_count || 0,
        })
        setUpdatedAt(new Date())
      }
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }, [search, grade, subject, status])

  useEffect(() => {
    const t = setTimeout(fetchData, 350)
    return () => clearTimeout(t)
  }, [fetchData])

  useEffect(() => {
    const id = setInterval(fetchData, 20000)
    return () => clearInterval(id)
  }, [fetchData])

  const fmt = (s) =>
    s
      ? new Date(s).toLocaleString('uz-UZ', {
          day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit',
        })
      : '—'

  return (
    <div className="mon-wrap">
      <div className="mon-card">
        <div className="mon-head">
          <div>
            <h1>📊 Test Monitoringi</h1>
            <p>Kim testga kirdi va kim kirmadi</p>
          </div>
          <button className="mon-refresh" onClick={fetchData}>↻ Yangilash</button>
        </div>

        <div className="mon-stats">
          <div className="stat s-total">
            <span className="num">{summary.total}</span>
            <span className="lbl">Jami o'quvchi</span>
          </div>
          <div className="stat s-in">
            <span className="num">{summary.entered_count}</span>
            <span className="lbl">Kirdi</span>
          </div>
          <div className="stat s-out">
            <span className="num">{summary.not_entered_count}</span>
            <span className="lbl">Kirmadi</span>
          </div>
        </div>

        <div className="mon-filters">
          <input
            className="mon-search"
            placeholder="Ism bo'yicha qidiruv..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
          <select value={grade} onChange={(e) => setGrade(e.target.value)}>
            {GRADES.map((g) => (
              <option key={g} value={g}>{g === 'Barcha sinflar' ? g : `${g}-sinf`}</option>
            ))}
          </select>
          <select value={subject} onChange={(e) => setSubject(e.target.value)}>
            {SUBJECTS.map((s) => <option key={s} value={s}>{s}</option>)}
          </select>
          <div className="mon-tabs">
            {STATUS_TABS.map((s) => (
              <button
                key={s.key}
                className={`tab ${status === s.key ? 'active' : ''}`}
                onClick={() => setStatus(s.key)}
              >
                {s.label}
              </button>
            ))}
          </div>
        </div>

        <div className="mon-table-wrap">
          {loading ? (
            <div className="mon-empty">Yuklanmoqda...</div>
          ) : rows.length === 0 ? (
            <div className="mon-empty">Hech narsa topilmadi</div>
          ) : (
            <table className="mon-table">
              <thead>
                <tr>
                  <th>#</th>
                  <th>F.I.O</th>
                  <th>Sinf</th>
                  <th>Fan</th>
                  <th>Holat</th>
                  <th>Vaqt</th>
                </tr>
              </thead>
              <tbody>
                {rows.map((r, i) => {
                  const b = BADGE[r.status] || BADGE.not_entered
                  return (
                    <tr key={r.id}>
                      <td>{i + 1}</td>
                      <td className="name">{r.full_name}</td>
                      <td>{r.grade}-sinf</td>
                      <td>{r.subject}</td>
                      <td>
                        <span className={`badge ${b.cls}`}>{b.text}</span>
                        {r.status === 'completed' && r.percentage != null && (
                          <span className="pct">{r.percentage}%</span>
                        )}
                      </td>
                      <td className="time">
                        {r.status === 'completed' ? fmt(r.finished_at) : fmt(r.started_at)}
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          )}
        </div>

        {updatedAt && (
          <div className="mon-foot">
            Yangilangan: {updatedAt.toLocaleTimeString('uz-UZ')} • har 20 soniyada avtomatik yangilanadi
          </div>
        )}
      </div>
    </div>
  )
}
