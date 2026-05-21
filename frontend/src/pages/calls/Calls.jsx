import React, { useState, useEffect, useCallback, useMemo } from 'react'
import {
  Phone, PhoneOff, PhoneIncoming, PhoneForwarded,
  Search, RefreshCw, X, User, GraduationCap, BookOpen,
  ChevronDown, ChevronUp, Copy, Check
} from 'lucide-react'
import './Calls.css'

const API_BASE = 'http://localhost:8000/api'

const CALL_STATUSES = {
  new:        { label: 'Yangi',       icon: Phone,            color: 'call-new',       emoji: '📞' },
  no_answer:  { label: "Ko'tarmadi",  icon: PhoneOff,         color: 'call-no-answer', emoji: '📵' },
  confirmed:  { label: 'Keladi',      icon: PhoneForwarded,   color: 'call-confirmed', emoji: '✅' },
  declined:   { label: 'Rad etildi',  icon: PhoneIncoming,    color: 'call-declined',  emoji: '❌' },
}

export default function Calls() {
  const [participants, setParticipants] = useState([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [activeTab, setActiveTab] = useState('new')
  const [updatingId, setUpdatingId] = useState(null)
  const [copiedPhone, setCopiedPhone] = useState(null)
  const [expandedId, setExpandedId] = useState(null)

  const fetchData = useCallback(async () => {
    setLoading(true)
    try {
      const res = await fetch(`${API_BASE}/registration/participants/`)
      const data = await res.json()
      const list = Array.isArray(data) ? data : (data.results || [])
      // Only show approved participants
      setParticipants(list.filter(p => p.verification_status === 'approved'))
    } catch (e) {
      console.error(e)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => { fetchData() }, [fetchData])

  const updateCallStatus = async (id, newStatus) => {
    setUpdatingId(id)
    try {
      const res = await fetch(`${API_BASE}/registration/participants/${id}/call-status/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ call_status: newStatus })
      })
      if (res.ok) {
        setParticipants(prev =>
          prev.map(p => p.id === id ? { ...p, call_status: newStatus } : p)
        )
      }
    } catch (e) {
      console.error(e)
    } finally {
      setUpdatingId(null)
    }
  }

  const handleCopyPhone = (phone, id) => {
    navigator.clipboard.writeText(phone)
    setCopiedPhone(id)
    setTimeout(() => setCopiedPhone(null), 2000)
  }

  // Filter and group
  const filtered = useMemo(() => {
    const q = search.toLowerCase()
    return participants.filter(p => {
      if (q && !p.full_name?.toLowerCase().includes(q) && !p.phone?.includes(q)) return false
      return (p.call_status || 'new') === activeTab
    })
  }, [participants, search, activeTab])

  // Stats
  const stats = useMemo(() => {
    const s = { new: 0, no_answer: 0, confirmed: 0, declined: 0 }
    participants.forEach(p => {
      const st = p.call_status || 'new'
      if (s[st] !== undefined) s[st]++
    })
    return s
  }, [participants])

  return (
    <div className="calls-page">
      {/* Header */}
      <div className="calls-header">
        <div className="calls-title-row">
          <div className="calls-title">
            <span className="calls-icon-wrap">📞</span>
            <div>
              <h1>Qo'ng'iroqlar</h1>
              <p>Tasdiqlangan ishtirokchilarga qo'ng'iroq qilish va natijalarni belgilash</p>
            </div>
          </div>
          <button className={`refresh-btn ${loading ? 'spinning' : ''}`} onClick={fetchData} disabled={loading}>
            <RefreshCw size={16} />
            <span>Yangilash</span>
          </button>
        </div>
      </div>

      {/* Tabs */}
      <div className="calls-tabs">
        {Object.entries(CALL_STATUSES).map(([key, val]) => {
          const IconComp = val.icon
          return (
            <button
              key={key}
              className={`call-tab ${val.color} ${activeTab === key ? 'active' : ''}`}
              onClick={() => setActiveTab(key)}
            >
              <IconComp size={16} />
              <span className="tab-label">{val.label}</span>
              <span className="tab-count">{stats[key]}</span>
            </button>
          )
        })}
      </div>

      {/* Search */}
      <div className="calls-search-row">
        <div className="search-box">
          <Search size={18} className="search-icon" />
          <input
            placeholder="Ism yoki telefon raqam bo'yicha qidiruv..."
            value={search}
            onChange={e => setSearch(e.target.value)}
          />
          {search && (
            <button className="clear-search" onClick={() => setSearch('')}>
              <X size={14} />
            </button>
          )}
        </div>
        <div className="results-count">
          {loading ? 'Yuklanmoqda...' : `${filtered.length} ta ishtirokchi`}
        </div>
      </div>

      {/* List */}
      <div className="calls-list">
        {loading ? (
          <div className="calls-loading">
            <div className="spinner-big"></div>
            <p>Yuklanmoqda...</p>
          </div>
        ) : filtered.length === 0 ? (
          <div className="calls-empty">
            <span className="empty-icon">{CALL_STATUSES[activeTab].emoji}</span>
            <h3>
              {activeTab === 'new' && "Yangi qo'ng'iroq qilinadigan ishtirokchi yo'q"}
              {activeTab === 'no_answer' && "Ko'tarmagan ishtirokchi yo'q"}
              {activeTab === 'confirmed' && "Kelishini tasdiqlagan ishtirokchi yo'q"}
              {activeTab === 'declined' && "Rad etgan ishtirokchi yo'q"}
            </h3>
          </div>
        ) : (
          filtered.map(p => {
            const isExpanded = expandedId === p.id
            const isCopied = copiedPhone === p.id
            const isUpdating = updatingId === p.id

            return (
              <div className={`call-card ${CALL_STATUSES[activeTab].color}`} key={p.id}>
                <div className="call-card-main" onClick={() => setExpandedId(isExpanded ? null : p.id)}>
                  <div className="call-avatar">
                    {p.full_name?.[0]?.toUpperCase() || '?'}
                  </div>

                  <div className="call-info">
                    <h4 className="call-name">{p.full_name}</h4>
                    <div className="call-meta-inline">
                      <span className="call-grade">{p.grade}-sinf</span>
                      <span className="call-subject">{p.subject}</span>
                    </div>
                  </div>

                  <div className="call-phone-area">
                    <a
                      href={`tel:${p.phone}`}
                      className="phone-link"
                      onClick={e => e.stopPropagation()}
                    >
                      <Phone size={14} />
                      {p.phone}
                    </a>
                    <button
                      className={`copy-phone-btn ${isCopied ? 'copied' : ''}`}
                      onClick={(e) => { e.stopPropagation(); handleCopyPhone(p.phone, p.id) }}
                      title="Raqamni nusxalash"
                    >
                      {isCopied ? <Check size={14} /> : <Copy size={14} />}
                    </button>
                  </div>

                  <div className="call-expand-icon">
                    {isExpanded ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
                  </div>
                </div>

                {isExpanded && (
                  <div className="call-card-expanded">
                    <div className="call-details-grid">
                      <div className="detail-item">
                        <User size={14} />
                        <span>F.I.O: <strong>{p.full_name}</strong></span>
                      </div>
                      <div className="detail-item">
                        <GraduationCap size={14} />
                        <span>Sinf: <strong>{p.grade}-sinf</strong></span>
                      </div>
                      <div className="detail-item">
                        <BookOpen size={14} />
                        <span>Fan: <strong>{p.subject}</strong></span>
                      </div>
                      <div className="detail-item">
                        <Phone size={14} />
                        <span>Telefon: <strong>{p.phone}</strong></span>
                      </div>
                      {p.unique_code && (
                        <div className="detail-item">
                          <span>🎟 Kod: <strong className="unique-code">{p.unique_code}</strong></span>
                        </div>
                      )}
                    </div>

                    <div className="call-actions">
                      <span className="actions-label">Natijani belgilang:</span>
                      <div className="action-buttons">
                        {activeTab !== 'confirmed' && (
                          <button
                            className="action-btn btn-confirmed"
                            onClick={() => updateCallStatus(p.id, 'confirmed')}
                            disabled={isUpdating}
                          >
                            <PhoneForwarded size={14} />
                            Keladi
                          </button>
                        )}
                        {activeTab !== 'no_answer' && (
                          <button
                            className="action-btn btn-no-answer"
                            onClick={() => updateCallStatus(p.id, 'no_answer')}
                            disabled={isUpdating}
                          >
                            <PhoneOff size={14} />
                            Ko'tarmadi
                          </button>
                        )}
                        {activeTab !== 'declined' && (
                          <button
                            className="action-btn btn-declined"
                            onClick={() => updateCallStatus(p.id, 'declined')}
                            disabled={isUpdating}
                          >
                            <X size={14} />
                            Rad etildi
                          </button>
                        )}
                        {activeTab !== 'new' && (
                          <button
                            className="action-btn btn-reset"
                            onClick={() => updateCallStatus(p.id, 'new')}
                            disabled={isUpdating}
                          >
                            <Phone size={14} />
                            Yangiga qaytarish
                          </button>
                        )}
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )
          })
        )}
      </div>
    </div>
  )
}
