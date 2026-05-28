import React, { useState, useEffect, useCallback, useMemo } from 'react'
import {
  Phone, PhoneOff, PhoneIncoming, PhoneForwarded,
  Search, RefreshCw, X, GraduationCap, BookOpen,
  ChevronDown, ChevronUp, Copy, Check, Users, MessageCircle,
  CalendarDays, Hourglass, Sparkles, Trash2, AlertTriangle
} from 'lucide-react'
import './Calls.css'
import { API_BASE } from '../../config'

const CALL_STATUSES = {
  new:        { label: 'Yangi',       icon: Phone,            color: 'call-new',       emoji: '📞' },
  no_answer:  { label: "Ko'tarmadi",  icon: PhoneOff,         color: 'call-no-answer', emoji: '📵' },
  confirmed:  { label: 'Keladi',      icon: PhoneForwarded,   color: 'call-confirmed', emoji: '✅' },
  declined:   { label: 'Rad etildi',  icon: PhoneIncoming,    color: 'call-declined',  emoji: '❌' },
}

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

const formatPhone = (phone) => {
  if (!phone) return ''
  const digits = phone.replace(/\D/g, '')
  if (digits.length === 12 && digits.startsWith('998')) {
    return `+${digits.slice(0, 3)} ${digits.slice(3, 5)} ${digits.slice(5, 8)} ${digits.slice(8, 10)} ${digits.slice(10, 12)}`
  }
  return phone
}

const formatDateLabel = (dateStr) => {
  if (!dateStr) return 'Sana belgilanmagan'
  const months = [
    'yanvar', 'fevral', 'mart', 'aprel', 'may', 'iyun',
    'iyul', 'avgust', 'sentabr', 'oktabr', 'noyabr', 'dekabr'
  ]
  const d = new Date(dateStr + 'T00:00:00')
  return `${d.getDate()}-${months[d.getMonth()]}`
}

const formatDateFullLabel = (dateStr) => {
  if (!dateStr) return 'Sana belgilanmagan'
  const months = [
    'yanvar', 'fevral', 'mart', 'aprel', 'may', 'iyun',
    'iyul', 'avgust', 'sentabr', 'oktabr', 'noyabr', 'dekabr'
  ]
  const d = new Date(dateStr + 'T00:00:00')
  return `${d.getDate()}-${months[d.getMonth()]}, ${d.getFullYear()}-yil`
}

export default function Calls() {
  const [participants, setParticipants] = useState([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [activeTab, setActiveTab] = useState('new')
  const [activeDate, setActiveDate] = useState('upcoming')
  const [updatingId, setUpdatingId] = useState(null)
  const [copiedPhone, setCopiedPhone] = useState(null)
  const [expandedPhone, setExpandedPhone] = useState(null)
  const [deleteConfirm, setDeleteConfirm] = useState(null) // { ids: [], names: [], phone, mode: 'one'|'group' }
  const [deleting, setDeleting] = useState(false)

  const fetchData = useCallback(async () => {
    setLoading(true)
    try {
      const res = await fetch(`${API_BASE}/registration/participants/`)
      const data = await res.json()
      const list = Array.isArray(data) ? data : (data.results || [])
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

  const updateGroupCallStatus = async (group, newStatus) => {
    const ids = group.members.map(m => m.id)
    setUpdatingId(group.phone)
    try {
      await Promise.all(ids.map(id =>
        fetch(`${API_BASE}/registration/participants/${id}/call-status/`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ call_status: newStatus })
        })
      ))
      setParticipants(prev =>
        prev.map(p => ids.includes(p.id) ? { ...p, call_status: newStatus } : p)
      )
    } catch (e) {
      console.error(e)
    } finally {
      setUpdatingId(null)
    }
  }

  const handleCopyPhone = (phone, key) => {
    navigator.clipboard.writeText(phone)
    setCopiedPhone(key)
    setTimeout(() => setCopiedPhone(null), 2000)
  }

  const askDeleteOne = (member) => {
    setDeleteConfirm({
      ids: [member.id],
      names: [member.full_name],
      phone: member.phone,
      mode: 'one',
    })
  }

  const askDeleteGroup = (group) => {
    setDeleteConfirm({
      ids: group.members.map(m => m.id),
      names: group.members.map(m => m.full_name),
      phone: group.phone,
      mode: 'group',
    })
  }

  const confirmDelete = async () => {
    if (!deleteConfirm) return
    setDeleting(true)
    try {
      await Promise.all(deleteConfirm.ids.map(id =>
        fetch(`${API_BASE}/registration/participants/${id}/`, { method: 'DELETE' })
      ))
      setParticipants(prev => prev.filter(p => !deleteConfirm.ids.includes(p.id)))
      setDeleteConfirm(null)
    } catch (e) {
      console.error(e)
      alert("O'chirishda xatolik yuz berdi")
    } finally {
      setDeleting(false)
    }
  }

  // Build date list: collect distinct target_test_date values, split into upcoming/past/pending
  const dateBuckets = useMemo(() => {
    const today = new Date()
    today.setHours(0, 0, 0, 0)
    const dateMap = new Map() // dateStr -> count
    let pendingCount = 0
    participants.forEach(p => {
      if (!p.target_test_date) {
        pendingCount++
      } else {
        dateMap.set(p.target_test_date, (dateMap.get(p.target_test_date) || 0) + 1)
      }
    })
    const upcoming = []
    const past = []
    Array.from(dateMap.entries()).forEach(([dateStr, count]) => {
      const d = new Date(dateStr + 'T00:00:00')
      const item = { dateStr, count, dateObj: d }
      if (d >= today) upcoming.push(item)
      else past.push(item)
    })
    upcoming.sort((a, b) => a.dateObj - b.dateObj)
    past.sort((a, b) => b.dateObj - a.dateObj)
    const upcomingDate = upcoming[0]?.dateStr || null
    return { upcoming, past, pendingCount, upcomingDate }
  }, [participants])

  // Auto-switch activeDate when data first loads or selected date no longer exists
  useEffect(() => {
    if (loading) return
    if (activeDate === 'upcoming' || activeDate === 'all' || activeDate === 'pending') return
    // Check if the activeDate still exists in upcoming or past
    const stillExists = [...dateBuckets.upcoming, ...dateBuckets.past].some(d => d.dateStr === activeDate)
    if (!stillExists) {
      setActiveDate(dateBuckets.upcomingDate ? 'upcoming' : (dateBuckets.pendingCount > 0 ? 'pending' : 'all'))
    }
  }, [loading, activeDate, dateBuckets])

  // Filter participants by selected date BEFORE grouping by phone
  const dateFilteredParticipants = useMemo(() => {
    if (activeDate === 'all') return participants
    if (activeDate === 'pending') return participants.filter(p => !p.target_test_date)
    if (activeDate === 'upcoming') {
      const upcomingDate = dateBuckets.upcomingDate
      if (!upcomingDate) return []
      return participants.filter(p => p.target_test_date === upcomingDate)
    }
    return participants.filter(p => p.target_test_date === activeDate)
  }, [participants, activeDate, dateBuckets])

  // Group participants (date-filtered) by phone
  const phoneGroups = useMemo(() => {
    const map = new Map()
    dateFilteredParticipants.forEach(p => {
      const key = p.phone || 'unknown'
      if (!map.has(key)) map.set(key, [])
      map.get(key).push(p)
    })
    return Array.from(map.entries()).map(([phone, members]) => {
      const statuses = new Set(members.map(m => m.call_status || 'new'))
      const groupStatus = statuses.size === 1 ? [...statuses][0] : 'mixed'
      return { phone, members, groupStatus, statuses: [...statuses] }
    })
  }, [dateFilteredParticipants])

  // Filter by tab + search
  const filteredGroups = useMemo(() => {
    const q = search.toLowerCase().trim()
    return phoneGroups.filter(g => {
      // Tab filter: include group if ANY member matches the active tab
      const hasInTab = g.members.some(m => (m.call_status || 'new') === activeTab)
      if (!hasInTab) return false

      if (!q) return true
      if (g.phone?.toLowerCase().includes(q)) return true
      return g.members.some(m => m.full_name?.toLowerCase().includes(q))
    })
  }, [phoneGroups, search, activeTab])

  // Per-tab stats (within current date filter — count groups that have at least one member with that status)
  const stats = useMemo(() => {
    const s = { new: 0, no_answer: 0, confirmed: 0, declined: 0 }
    phoneGroups.forEach(g => {
      const seenStatuses = new Set()
      g.members.forEach(m => seenStatuses.add(m.call_status || 'new'))
      seenStatuses.forEach(st => {
        if (s[st] !== undefined) s[st]++
      })
    })
    return s
  }, [phoneGroups])

  // Stats for total people, multi-person phones (within current date filter)
  const totalStats = useMemo(() => {
    const sharedPhones = phoneGroups.filter(g => g.members.length > 1).length
    return {
      totalGroups: phoneGroups.length,
      totalPeople: dateFilteredParticipants.length,
      sharedPhones,
    }
  }, [phoneGroups, dateFilteredParticipants])

  return (
    <div className="calls-page">
      {/* Header */}
      <div className="calls-header">
        <div className="calls-title-row">
          <div className="calls-title">
            <span className="calls-icon-wrap">
              <Phone size={26} strokeWidth={2.2} />
            </span>
            <div>
              <h1>Qo'ng'iroqlar</h1>
              <p>
                {activeDate === 'all' ? 'Barcha sanalardagi' :
                 activeDate === 'pending' ? 'Sana belgilanmagan' :
                 activeDate === 'upcoming' && dateBuckets.upcomingDate ? `${formatDateFullLabel(dateBuckets.upcomingDate)} olimpiadasi` :
                 activeDate ? `${formatDateFullLabel(activeDate)} olimpiadasi` : ''}
                {' · '}
                {totalStats.totalPeople} ta ishtirokchi · {totalStats.totalGroups} ta telefon
                {totalStats.sharedPhones > 0 && (
                  <> · <strong>{totalStats.sharedPhones}</strong> ta umumiy raqam</>
                )}
              </p>
            </div>
          </div>
          <button className={`refresh-btn ${loading ? 'spinning' : ''}`} onClick={fetchData} disabled={loading}>
            <RefreshCw size={16} />
            <span>Yangilash</span>
          </button>
        </div>
      </div>

      {/* Date Filter Chips */}
      <div className="calls-date-bar">
        <div className="date-bar-label">
          <CalendarDays size={14} />
          <span>Olimpiada sanasi:</span>
        </div>
        <div className="date-chips">
          {dateBuckets.upcomingDate && (
            <button
              className={`date-chip date-chip-upcoming ${activeDate === 'upcoming' ? 'active' : ''}`}
              onClick={() => setActiveDate('upcoming')}
              title={formatDateFullLabel(dateBuckets.upcomingDate)}
            >
              <Sparkles size={13} />
              <span>Kelajakdagi · {formatDateLabel(dateBuckets.upcomingDate)}</span>
              <span className="chip-count">
                {participants.filter(p => p.target_test_date === dateBuckets.upcomingDate).length}
              </span>
            </button>
          )}

          {dateBuckets.past.map(d => (
            <button
              key={d.dateStr}
              className={`date-chip date-chip-past ${activeDate === d.dateStr ? 'active' : ''}`}
              onClick={() => setActiveDate(d.dateStr)}
              title={formatDateFullLabel(d.dateStr)}
            >
              <CalendarDays size={13} />
              <span>{formatDateLabel(d.dateStr)}</span>
              <span className="chip-count">{d.count}</span>
            </button>
          ))}

          {dateBuckets.pendingCount > 0 && (
            <button
              className={`date-chip date-chip-pending ${activeDate === 'pending' ? 'active' : ''}`}
              onClick={() => setActiveDate('pending')}
              title="Olimpiada sanasi hali belgilanmagan ishtirokchilar"
            >
              <Hourglass size={13} />
              <span>Sana kutmoqda</span>
              <span className="chip-count">{dateBuckets.pendingCount}</span>
            </button>
          )}

          <button
            className={`date-chip date-chip-all ${activeDate === 'all' ? 'active' : ''}`}
            onClick={() => setActiveDate('all')}
          >
            <Users size={13} />
            <span>Barchasi</span>
            <span className="chip-count">{participants.length}</span>
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
          {loading ? 'Yuklanmoqda...' : `${filteredGroups.length} ta raqam`}
        </div>
      </div>

      {/* Delete Confirmation Modal */}
      {deleteConfirm && (
        <div className="delete-modal-overlay" onClick={() => !deleting && setDeleteConfirm(null)}>
          <div className="delete-modal-card" onClick={e => e.stopPropagation()}>
            <div className="delete-modal-icon">
              <AlertTriangle size={28} />
            </div>
            <h3 className="delete-modal-title">
              {deleteConfirm.mode === 'group'
                ? `${deleteConfirm.ids.length} ta lidni butunlay o'chirilsinmi?`
                : "Lidni butunlay o'chirilsinmi?"}
            </h3>
            <p className="delete-modal-text">
              Bu amalni qaytarib bo'lmaydi. Quyidagi {deleteConfirm.mode === 'group' ? "ishtirokchilar" : "ishtirokchi"} bazadan butunlay o'chiriladi:
            </p>
            <div className="delete-modal-names">
              {deleteConfirm.names.map((n, i) => (
                <span key={i} className="delete-name-chip">{n}</span>
              ))}
            </div>
            <div className="delete-modal-phone">
              <Phone size={14} />
              <strong>{formatPhone(deleteConfirm.phone)}</strong>
            </div>
            <div className="delete-modal-actions">
              <button
                className="btn-cancel-delete"
                onClick={() => setDeleteConfirm(null)}
                disabled={deleting}
              >
                Bekor qilish
              </button>
              <button
                className="btn-confirm-delete"
                onClick={confirmDelete}
                disabled={deleting}
              >
                {deleting ? (
                  <>O'chirilmoqda...</>
                ) : (
                  <>
                    <Trash2 size={15} />
                    Ha, o'chirish
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Groups List */}
      <div className="calls-list">
        {loading ? (
          <div className="calls-loading">
            <div className="spinner-big"></div>
            <p>Yuklanmoqda...</p>
          </div>
        ) : filteredGroups.length === 0 ? (
          <div className="calls-empty">
            <span className="empty-icon">{CALL_STATUSES[activeTab].emoji}</span>
            <h3>
              {activeTab === 'new' && "Yangi qo'ng'iroq qilinadigan raqam yo'q"}
              {activeTab === 'no_answer' && "Ko'tarmagan raqam yo'q"}
              {activeTab === 'confirmed' && "Kelishini tasdiqlagan raqam yo'q"}
              {activeTab === 'declined' && "Rad etgan raqam yo'q"}
            </h3>
            {activeDate !== 'all' && (
              <p style={{ marginTop: '8px', fontSize: '0.85rem', color: '#94a3b8' }}>
                Tanlangan sana bo'yicha. Boshqa sanani tanlang yoki "Barchasi"ni bosing.
              </p>
            )}
          </div>
        ) : (
          filteredGroups.map(group => {
            const isExpanded = expandedPhone === group.phone
            const isPhoneCopied = copiedPhone === group.phone
            const isUpdating = updatingId === group.phone
            const isMulti = group.members.length > 1
            const tgIds = group.members
              .map(m => m.telegram_id)
              .filter(t => t && t.startsWith('tg_'))
              .map(t => t.replace('tg_', ''))
            const tgId = tgIds[0]

            return (
              <div className={`phone-group-card ${isMulti ? 'multi' : ''} ${CALL_STATUSES[activeTab].color}`} key={group.phone}>
                {/* PHONE HEADER — primary action area */}
                <div className="phone-header">
                  <div className="phone-header-left">
                    <div className="phone-icon-circle">
                      <Phone size={22} strokeWidth={2.4} />
                    </div>
                    <div className="phone-info">
                      <a
                        href={`tel:${group.phone}`}
                        className="phone-number-big"
                        onClick={e => e.stopPropagation()}
                      >
                        {formatPhone(group.phone)}
                      </a>
                      <div className="phone-sub-info">
                        {isMulti ? (
                          <span className="people-count-badge">
                            <Users size={13} />
                            <strong>{group.members.length}</strong> ta ishtirokchi
                          </span>
                        ) : (
                          <span className="people-count-badge solo">
                            <Users size={13} />
                            1 ta ishtirokchi
                          </span>
                        )}
                      </div>
                    </div>
                  </div>

                  <div className="phone-header-actions">
                    <a
                      href={`tel:${group.phone}`}
                      className="phone-action-btn primary-call"
                      title="Qo'ng'iroq qilish"
                    >
                      <Phone size={16} />
                      <span>Qo'ng'iroq</span>
                    </a>
                    {tgId && (
                      <a
                        href={`tg://user?id=${tgId}`}
                        className="phone-action-btn telegram-action"
                        title="Telegramda yozish"
                      >
                        <MessageCircle size={16} />
                      </a>
                    )}
                    <button
                      className={`phone-action-btn copy-action ${isPhoneCopied ? 'copied' : ''}`}
                      onClick={() => handleCopyPhone(group.phone, group.phone)}
                      title="Raqamni nusxalash"
                    >
                      {isPhoneCopied ? <Check size={16} /> : <Copy size={16} />}
                    </button>
                    <button
                      className="phone-action-btn expand-action"
                      onClick={() => setExpandedPhone(isExpanded ? null : group.phone)}
                      title={isExpanded ? "Yopish" : "Ochish"}
                    >
                      {isExpanded ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
                    </button>
                  </div>
                </div>

                {/* MEMBERS LIST (compact preview) */}
                <div className="members-preview">
                  {group.members.map(m => {
                    const memberStatus = m.call_status || 'new'
                    const statusObj = CALL_STATUSES[memberStatus]
                    return (
                      <div
                        key={m.id}
                        className={`member-chip status-${memberStatus}`}
                        onClick={() => setExpandedPhone(isExpanded ? null : group.phone)}
                        title={`${m.full_name} — ${statusObj?.label}`}
                      >
                        <div
                          className="member-chip-avatar"
                          style={{ background: getAvatarGradient(m.full_name) }}
                        >
                          {m.full_name?.[0]?.toUpperCase() || '?'}
                        </div>
                        <div className="member-chip-info">
                          <span className="member-chip-name">{m.full_name}</span>
                          <span className="member-chip-meta">
                            {m.grade}-sinf · {m.subject}
                          </span>
                        </div>
                        <span className={`member-chip-status ${statusObj?.color}`}>
                          {statusObj?.emoji}
                        </span>
                      </div>
                    )
                  })}
                </div>

                {/* GROUP-LEVEL QUICK ACTIONS (visible always for multi-member) */}
                {isMulti && (
                  <div className="group-quick-actions">
                    <span className="group-actions-label">
                      Barchasiga birdaniga belgilash:
                    </span>
                    <div className="group-actions-row">
                      <button
                        className="group-btn group-btn-confirmed"
                        onClick={() => updateGroupCallStatus(group, 'confirmed')}
                        disabled={isUpdating}
                      >
                        <PhoneForwarded size={14} />
                        Keladi
                      </button>
                      <button
                        className="group-btn group-btn-no-answer"
                        onClick={() => updateGroupCallStatus(group, 'no_answer')}
                        disabled={isUpdating}
                      >
                        <PhoneOff size={14} />
                        Ko'tarmadi
                      </button>
                      <button
                        className="group-btn group-btn-declined"
                        onClick={() => updateGroupCallStatus(group, 'declined')}
                        disabled={isUpdating}
                      >
                        <X size={14} />
                        Rad etildi
                      </button>
                      <button
                        className="group-btn group-btn-delete"
                        onClick={() => askDeleteGroup(group)}
                        disabled={isUpdating}
                        title="Barcha lidlarni o'chirish"
                      >
                        <Trash2 size={14} />
                        Hammasini o'chirish
                      </button>
                    </div>
                  </div>
                )}

                {/* EXPANDED MEMBER DETAILS */}
                {isExpanded && (
                  <div className="members-detailed">
                    {group.members.map(m => {
                      const memberStatus = m.call_status || 'new'
                      const isMemberUpdating = updatingId === m.id
                      return (
                        <div className={`member-detailed status-${memberStatus}`} key={m.id}>
                          <div className="member-detailed-header">
                            <div
                              className="member-detailed-avatar"
                              style={{ background: getAvatarGradient(m.full_name) }}
                            >
                              {m.full_name?.[0]?.toUpperCase() || '?'}
                            </div>
                            <div className="member-detailed-info">
                              <h4>{m.full_name}</h4>
                              <div className="member-tags">
                                <span className="meta-tag">
                                  <GraduationCap size={12} />
                                  {m.grade}-sinf
                                </span>
                                <span className="meta-tag">
                                  <BookOpen size={12} />
                                  {m.subject}
                                </span>
                                {m.unique_code && (
                                  <span className="meta-tag code-tag">
                                    🎟 {m.unique_code}
                                  </span>
                                )}
                              </div>
                            </div>
                            <span className={`member-status-pill ${CALL_STATUSES[memberStatus].color}`}>
                              {CALL_STATUSES[memberStatus].emoji} {CALL_STATUSES[memberStatus].label}
                            </span>
                          </div>

                          <div className="member-action-row">
                            <span className="actions-label">Holatni o'zgartirish:</span>
                            <div className="action-buttons">
                              {memberStatus !== 'confirmed' && (
                                <button
                                  className="action-btn btn-confirmed"
                                  onClick={() => updateCallStatus(m.id, 'confirmed')}
                                  disabled={isMemberUpdating}
                                >
                                  <PhoneForwarded size={13} />
                                  Keladi
                                </button>
                              )}
                              {memberStatus !== 'no_answer' && (
                                <button
                                  className="action-btn btn-no-answer"
                                  onClick={() => updateCallStatus(m.id, 'no_answer')}
                                  disabled={isMemberUpdating}
                                >
                                  <PhoneOff size={13} />
                                  Ko'tarmadi
                                </button>
                              )}
                              {memberStatus !== 'declined' && (
                                <button
                                  className="action-btn btn-declined"
                                  onClick={() => updateCallStatus(m.id, 'declined')}
                                  disabled={isMemberUpdating}
                                >
                                  <X size={13} />
                                  Rad etildi
                                </button>
                              )}
                              {memberStatus !== 'new' && (
                                <button
                                  className="action-btn btn-reset"
                                  onClick={() => updateCallStatus(m.id, 'new')}
                                  disabled={isMemberUpdating}
                                >
                                  <Phone size={13} />
                                  Qaytarish
                                </button>
                              )}
                              <button
                                className="action-btn btn-delete-lead"
                                onClick={() => askDeleteOne(m)}
                                disabled={isMemberUpdating}
                                title="Lidni butunlay o'chirish"
                              >
                                <Trash2 size={13} />
                                O'chirish
                              </button>
                            </div>
                          </div>
                        </div>
                      )
                    })}
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
