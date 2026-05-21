import React, { useState, useEffect, useCallback } from 'react'
import { Search, RefreshCw, Trophy, ChevronUp, ChevronDown } from 'lucide-react'
import { API_BASE } from '../../config'
import './Results.css'

const SUBJECT_OPTIONS = ['Barcha fanlar', 'Matematika', 'Ingliz tili', 'Rus tili']
const GRADE_OPTIONS = ['Barcha sinflar', ...Array.from({ length: 11 }, (_, i) => `${i + 1}`)]

export default function Results() {
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(true)
  const [totalCount, setTotalCount] = useState(0)

  const [search, setSearch] = useState('')
  const [subject, setSubject] = useState('Barcha fanlar')
  const [grade, setGrade] = useState('Barcha sinflar')
  const [sortKey, setSortKey] = useState('rank')
  const [sortDir, setSortDir] = useState('asc')

  const fetchResults = useCallback(async () => {
    setLoading(true)
    const token = localStorage.getItem('access_token')
    const params = new URLSearchParams()
    if (search) params.append('search', search)
    if (subject !== 'Barcha fanlar') params.append('subject', subject)
    if (grade !== 'Barcha sinflar') params.append('grade', grade)

    try {
      const res = await fetch(`${API_BASE}/results/?${params.toString()}`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      if (res.ok) {
        const data = await res.json()
        setResults(data.results || [])
        setTotalCount(data.count || 0)
      }
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }, [search, subject, grade])

  useEffect(() => {
    const timer = setTimeout(fetchResults, 400)
    return () => clearTimeout(timer)
  }, [fetchResults])

  const handleSort = (key) => {
    if (sortKey === key) {
      setSortDir(d => d === 'asc' ? 'desc' : 'asc')
    } else {
      setSortKey(key)
      setSortDir('asc')
    }
  }

  const sorted = [...results].sort((a, b) => {
    let valA = a[sortKey]
    let valB = b[sortKey]
    if (typeof valA === 'string') valA = valA.toLowerCase()
    if (typeof valB === 'string') valB = valB.toLowerCase()
    if (valA < valB) return sortDir === 'asc' ? -1 : 1
    if (valA > valB) return sortDir === 'asc' ? 1 : -1
    return 0
  })

  const SortIcon = ({ col }) => {
    if (sortKey !== col) return <span className="sort-icon muted">↕</span>
    return sortDir === 'asc'
      ? <ChevronUp size={13} className="sort-icon active" />
      : <ChevronDown size={13} className="sort-icon active" />
  }

  const getMedalClass = (rank) => {
    if (rank === 1) return 'medal gold'
    if (rank === 2) return 'medal silver'
    if (rank === 3) return 'medal bronze'
    return null
  }

  const getPercentColor = (pct) => {
    if (pct >= 80) return 'pct-high'
    if (pct >= 50) return 'pct-mid'
    return 'pct-low'
  }

  return (
    <div className="results-page">
      {/* Header */}
      <div className="results-header">
        <div className="results-header-left">
          <div className="results-icon-wrap">
            <Trophy size={26} color="#f59e0b" />
          </div>
          <div>
            <h1>Natijalar</h1>
            <p>Barcha imtihon natijalari reytingi</p>
          </div>
        </div>
        <button className="btn-refresh" onClick={fetchResults}>
          <RefreshCw size={15} />
          <span>Yangilash</span>
        </button>
      </div>

      {/* Filters */}
      <div className="results-filters">
        <div className="search-wrap">
          <Search size={16} className="search-ico" />
          <input
            placeholder="Ism bo'yicha qidiruv..."
            value={search}
            onChange={e => setSearch(e.target.value)}
          />
        </div>

        <select value={subject} onChange={e => setSubject(e.target.value)}>
          {SUBJECT_OPTIONS.map(s => <option key={s} value={s}>{s}</option>)}
        </select>

        <select value={grade} onChange={e => setGrade(e.target.value)}>
          {GRADE_OPTIONS.map(g => (
            <option key={g} value={g}>
              {g === 'Barcha sinflar' ? g : `${g}-sinf`}
            </option>
          ))}
        </select>
      </div>

      {/* Count info */}
      <div className="results-count">
        {loading ? 'Yuklanmoqda...' : `${totalCount} ta natija topildi`}
      </div>

      {/* Table */}
      <div className="results-table-wrap">
        {loading ? (
          <div className="results-loading">
            <div className="spinner" />
            <p>Natijalar yuklanmoqda...</p>
          </div>
        ) : sorted.length === 0 ? (
          <div className="results-empty">
            <Trophy size={48} color="#d1d5db" />
            <p>Hech qanday natija topilmadi</p>
          </div>
        ) : (
          <table className="results-table">
            <thead>
              <tr>
                <th onClick={() => handleSort('rank')} className="sortable">
                  # <SortIcon col="rank" />
                </th>
                <th onClick={() => handleSort('full_name')} className="sortable">
                  F.I.O <SortIcon col="full_name" />
                </th>
                <th onClick={() => handleSort('subject')} className="sortable">
                  Fan <SortIcon col="subject" />
                </th>
                <th onClick={() => handleSort('grade')} className="sortable">
                  Sinf <SortIcon col="grade" />
                </th>
                <th onClick={() => handleSort('correct_count')} className="sortable">
                  To'g'ri <SortIcon col="correct_count" />
                </th>
                <th onClick={() => handleSort('wrong_count')} className="sortable">
                  Noto'g'ri <SortIcon col="wrong_count" />
                </th>
                <th onClick={() => handleSort('percentage')} className="sortable">
                  Foiz <SortIcon col="percentage" />
                </th>
                <th onClick={() => handleSort('score')} className="sortable">
                  Ball <SortIcon col="score" />
                </th>
                <th>Sana</th>
              </tr>
            </thead>
            <tbody>
              {sorted.map((r) => (
                <tr key={r.id} className={r.rank <= 3 ? `top-row rank-${r.rank}` : ''}>
                  <td>
                    {getMedalClass(r.rank)
                      ? <span className={getMedalClass(r.rank)}>{r.rank}</span>
                      : <span className="rank-num">{r.rank}</span>
                    }
                  </td>
                  <td>
                    <div className="participant-cell">
                      <div className="participant-avatar">
                        {r.full_name ? r.full_name[0].toUpperCase() : '?'}
                      </div>
                      <div>
                        <div className="participant-name">{r.full_name}</div>
                        <div className="participant-phone">{r.phone}</div>
                      </div>
                    </div>
                  </td>
                  <td><span className="subject-badge">{r.subject}</span></td>
                  <td><span className="grade-badge">{r.grade}-sinf</span></td>
                  <td><span className="correct-count">{r.correct_count}</span></td>
                  <td><span className="wrong-count">{r.wrong_count}</span></td>
                  <td>
                    <div className="pct-wrap">
                      <div className="pct-bar">
                        <div
                          className={`pct-fill ${getPercentColor(r.percentage)}`}
                          style={{ width: `${r.percentage}%` }}
                        />
                      </div>
                      <span className={`pct-label ${getPercentColor(r.percentage)}`}>
                        {r.percentage}%
                      </span>
                    </div>
                  </td>
                  <td><span className="score-badge">{r.score}</span></td>
                  <td className="date-cell">
                    {r.finished_at
                      ? new Date(r.finished_at).toLocaleDateString('uz-UZ', {
                          year: 'numeric', month: '2-digit', day: '2-digit',
                          hour: '2-digit', minute: '2-digit'
                        })
                      : '—'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}
