import React, { useState, useEffect, useCallback } from 'react'
import {
  Search,
  Copy,
  Check,
  RefreshCw,
  X,
  AlertTriangle,
  User,
  Calendar,
  CreditCard,
  Tag,
  BookOpen,
  GraduationCap,
  ArrowUpDown,
  Filter,
  Users,
  Clock,
  CheckCircle2,
  XCircle,
  TrendingUp
} from 'lucide-react'
import { authFetch } from '../../config'
import './Leads.css'

const STATUS_MAP = {
  pending:  { label: 'Kutilmoqda', color: 'status-pending', emoji: '⏳' },
  approved: { label: 'Tasdiqlangan', color: 'status-approved', emoji: '✅' },
  rejected: { label: 'Rad etilgan', color: 'status-rejected', emoji: '❌' },
}

const PAYMENT_LABELS = { click: 'Click', payme: 'Payme', cash: 'Naqd pul' }

const PRESET_REASONS = [
  "To'lov cheki yuborilmagan yoki yaroqsiz",
  "Hujjat rasmi xira, o'qib bo'lmaydi",
  "F.I.O. pasport/guvohnomaga mos kelmaydi",
  "Tanlangan sinf yoki fan noto'g'ri kiritilgan",
  "To'lov summasi noto'g'ri yoki yetarli emas"
]

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
  const code = name.charCodeAt(0) || 0
  return AVATAR_GRADIENTS[code % AVATAR_GRADIENTS.length]
}

export default function Leads({ defaultStatus = 'all' }) {
  const [participants, setParticipants] = useState([])
  const [loading, setLoading] = useState(true)
  const [actionLoading, setActionLoading] = useState(false)
  const [search, setSearch] = useState('')
  const [filterStatus, setFilterStatus] = useState(defaultStatus)
  const [filterSubject, setFilterSubject] = useState('all')
  const [filterGrade, setFilterGrade] = useState('all')
  const [sortBy, setSortBy] = useState('newest')
  const [selected, setSelected] = useState(null)
  const [stats, setStats] = useState({ total: 0, approved: 0, pending: 0, rejected: 0 })

  const [showRejectDialog, setShowRejectDialog] = useState(false)
  const [rejectingId, setRejectingId] = useState(null)
  const [rejectReason, setRejectReason] = useState('')

  const [copiedId, setCopiedId] = useState(null)


  const fetchData = useCallback(async () => {
    setLoading(true)
    try {
      const res = await authFetch('/registration/participants/')
      const data = await res.json()
      const list = Array.isArray(data) ? data : (data.results || [])
      setParticipants(list)
      setStats({
        total: list.length,
        approved: list.filter(p => p.verification_status === 'approved').length,
        pending:  list.filter(p => p.verification_status === 'pending').length,
        rejected: list.filter(p => p.verification_status === 'rejected').length,
      })
    } catch (e) {
      console.error(e)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    fetchData()
  }, [fetchData])

  useEffect(() => {
    setFilterStatus(defaultStatus)
  }, [defaultStatus])

  const filtered = participants
    .filter(p => {
      const q = search.toLowerCase()
      if (q && !p.full_name?.toLowerCase().includes(q) && !p.phone?.includes(q)) return false
      if (filterStatus !== 'all' && p.verification_status !== filterStatus) return false
      if (filterSubject !== 'all' && !p.subject?.includes(filterSubject)) return false
      if (filterGrade !== 'all' && String(p.grade) !== String(filterGrade)) return false
      return true
    })
    .sort((a, b) => {
      if (sortBy === 'newest') return new Date(b.registered_at) - new Date(a.registered_at)
      if (sortBy === 'oldest') return new Date(a.registered_at) - new Date(b.registered_at)
      if (sortBy === 'name') return a.full_name?.localeCompare(b.full_name)
      return 0
    })

  const allSubjects = [...new Set(participants.flatMap(p => p.subject?.split(', ') || []))]
  const allGrades = [...new Set(participants.map(p => p.grade).filter(Boolean))].sort((a, b) => Number(a) - Number(b))

  const handleApprove = async (id) => {
    setActionLoading(true)
    try {
      const res = await authFetch(`/registration/participants/${id}/approve/`, { method: 'POST' })
      if (res.ok) {
        await fetchData()
        setSelected(null)
      }
    } catch (e) {
      console.error(e)
    } finally {
      setActionLoading(false)
    }
  }

  const handleRejectClick = (id, e) => {
    if (e) e.stopPropagation()
    setRejectingId(id)
    setRejectReason('')
    setShowRejectDialog(true)
  }

  const handleRejectConfirm = async () => {
    if (!rejectReason.trim()) return
    setActionLoading(true)
    try {
      const res = await authFetch(`/registration/participants/${rejectingId}/reject/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ reason: rejectReason })
      })
      if (res.ok) {
        await fetchData()
        setShowRejectDialog(false)
        setRejectingId(null)
        setRejectReason('')
        setSelected(null)
      }
    } catch (e) {
      console.error(e)
    } finally {
      setActionLoading(false)
    }
  }

  const handleCopy = (code, id, e) => {
    if (e) e.stopPropagation()
    navigator.clipboard.writeText(code)
    setCopiedId(id)
    setTimeout(() => setCopiedId(null), 2000)
  }

  const formatDate = (d) => {
    if (!d) return '—'
    return new Date(d).toLocaleDateString('uz-UZ', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const resetFilters = () => {
    setSearch('')
    setFilterSubject('all')
    setFilterGrade('all')
    setSortBy('newest')
    setFilterStatus(defaultStatus)
  }

  const hasActiveFilters = search || filterSubject !== 'all' || filterGrade !== 'all' || filterStatus !== defaultStatus

  const pageTitle = defaultStatus === 'rejected' ? 'Rad etilgan arizalar' :
                    defaultStatus === 'approved' ? 'Tasdiqlangan arizalar' :
                    defaultStatus === 'pending' ? 'Kutilayotgan arizalar' :
                    "Arizalar ro'yxati"

  const pageSubtitle = "Olimpiada ishtirokchilarini boshqarish va verification paneli"

  return (
    <div className="leads-page">
      {/* Hero Header Card */}
      <div className="leads-hero">
        <div className="hero-bg-decor" />
        <div className="hero-bg-decor hero-bg-decor-2" />

        <div className="leads-title-row">
          <div className="leads-title">
            <span className="leads-icon">
              {defaultStatus === 'rejected' ? <XCircle size={28} strokeWidth={2.2} /> :
               defaultStatus === 'approved' ? <CheckCircle2 size={28} strokeWidth={2.2} /> :
               defaultStatus === 'pending' ? <Clock size={28} strokeWidth={2.2} /> :
               <Users size={28} strokeWidth={2.2} />}
            </span>
            <div>
              <h1>{pageTitle}</h1>
              <p>{pageSubtitle}</p>
            </div>
          </div>
          <button className={`refresh-btn ${loading ? 'spinning' : ''}`} onClick={fetchData} disabled={loading}>
            <RefreshCw size={16} />
            <span>Yangilash</span>
          </button>
        </div>

      </div>

      {/* Toolbar: Filters */}
      <div className="leads-toolbar">
        <div className="filters-row">
          <div className="search-box">
            <Search size={18} className="search-icon" />
            <input
              placeholder="Ism yoki telefon raqam bo'yicha qidiruv..."
              value={search}
              onChange={e => setSearch(e.target.value)}
            />
            {search && <button className="clear-search" onClick={() => setSearch('')}><X size={14} /></button>}
          </div>

          <div className="select-wrapper">
            <Filter size={14} className="select-icon" />
            <select value={filterSubject} onChange={e => setFilterSubject(e.target.value)}>
              <option value="all">Barcha fanlar</option>
              {allSubjects.map(s => <option key={s} value={s}>{s}</option>)}
            </select>
          </div>

          <div className="select-wrapper">
            <GraduationCap size={14} className="select-icon" />
            <select value={filterGrade} onChange={e => setFilterGrade(e.target.value)}>
              <option value="all">Barcha sinflar</option>
              {allGrades.map(g => <option key={g} value={g}>{g}-sinf</option>)}
            </select>
          </div>

          <div className="select-wrapper">
            <ArrowUpDown size={14} className="select-icon" />
            <select value={sortBy} onChange={e => setSortBy(e.target.value)}>
              <option value="newest">Yangi → Eski</option>
              <option value="oldest">Eski → Yangi</option>
              <option value="name">Alifbo bo'yicha</option>
            </select>
          </div>

          {hasActiveFilters && (
            <button className="reset-btn" onClick={resetFilters}>
              <X size={14} />
              Tozalash
            </button>
          )}
        </div>

        <div className="results-count-row">
          <div className="results-count">
            <TrendingUp size={14} />
            {loading ? 'Yuklanmoqda...' : <span><strong>{filtered.length}</strong> ta ariza topildi</span>}
          </div>
        </div>
      </div>

      {/* Table */}
      <div className="leads-table-wrap">
        {loading ? (
          <div className="leads-loading">
            <div className="spinner-big" />
            <p>Ma'lumotlar yuklanmoqda...</p>
          </div>
        ) : filtered.length === 0 ? (
          <div className="leads-empty">
            <div className="empty-icon">📭</div>
            <p>Qidiruv shartlariga mos keladigan arizalar topilmadi</p>
            {hasActiveFilters && (
              <button className="reset-btn" style={{marginTop: '16px'}} onClick={resetFilters}>
                Barcha filterlarni bekor qilish
              </button>
            )}
          </div>
        ) : (
          <table className="leads-table">
            <thead>
              <tr>
                <th>#</th>
                <th>Ishtirokchi F.I.O</th>
                <th>Telefon</th>
                <th style={{textAlign:'center'}}>Sinf</th>
                <th>Fanlar</th>
                <th style={{textAlign:'center'}}>To'lov turi</th>
                <th>To'lov Summasi</th>
                <th>Status</th>
                <th>Ro'yxatdan o'tgan sana</th>
                <th style={{textAlign:'right'}}>Amallar</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((p, i) => {
                const s = STATUS_MAP[p.verification_status] || STATUS_MAP.pending
                const subjectsCount = p.subject ? p.subject.split(',').length : 1
                const amount = 190000 + (subjectsCount - 1) * 90000
                const isCopied = copiedId === p.id

                return (
                  <tr key={p.id} className="table-row" onClick={() => setSelected(p)}>
                    <td className="td-num">{i + 1}</td>
                    <td className="td-name">
                      <div
                        className="name-avatar-gradient"
                        style={{ background: getAvatarGradient(p.full_name) }}
                      >
                        {p.full_name?.[0]?.toUpperCase() || '?'}
                      </div>
                      <span className="fullname-text">{p.full_name}</span>
                    </td>
                    <td className="td-phone">{p.phone}</td>
                    <td className="td-center">
                      <span className={`grade-badge grade-${p.grade}`}>
                        {p.grade}-sinf
                      </span>
                    </td>
                    <td className="td-subject">
                      <div className="subject-tags-container">
                        {p.subject?.split(', ').map(s => (
                          <span key={s} className="subject-tag">{s}</span>
                        ))}
                      </div>
                    </td>
                    <td className="td-center">
                      <span className={`payment-badge payment-${p.payment_type}`}>
                        {PAYMENT_LABELS[p.payment_type] || p.payment_type}
                      </span>
                    </td>
                    <td className="td-amount">
                      {Number(amount).toLocaleString('ru-RU')} so'm
                    </td>
                    <td>
                      <span className={`status-pill ${s.color}`}>
                        <span className="status-dot" />
                        {s.label}
                      </span>
                    </td>
                    <td className="td-date">{formatDate(p.registered_at)}</td>
                    <td className="td-actions" onClick={e => e.stopPropagation()}>
                      {p.verification_status === 'pending' && (
                        <div className="action-buttons">
                          <button
                            className="btn-approve"
                            onClick={() => handleApprove(p.id)}
                            disabled={actionLoading}
                            title="Arizani tasdiqlash"
                          >
                            Tasdiqlash
                          </button>
                          <button
                            className="btn-reject"
                            onClick={(e) => handleRejectClick(p.id, e)}
                            disabled={actionLoading}
                            title="Arizani rad etish"
                          >
                            Rad etish
                          </button>
                        </div>
                      )}
                      {p.verification_status === 'approved' && (
                        <div className="copy-code-container">
                          <span className="code-badge" onClick={(e) => handleCopy(p.unique_code, p.id, e)}>
                            <code>{p.unique_code}</code>
                            {isCopied ? <Check size={14} className="copy-success" /> : <Copy size={14} />}
                            {isCopied && <span className="copy-tooltip">Nusxalandi!</span>}
                          </span>
                        </div>
                      )}
                      {p.verification_status === 'rejected' && (
                        <span className="rejected-badge" title={p.rejection_reason}>
                          Rad etilgan
                        </span>
                      )}
                    </td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        )}
      </div>

      {/* Detail Modal */}
      {selected && (
        <div className="modal-overlay animate-fade-in" onClick={() => setSelected(null)}>
          <div className="modal-card animate-slide-up" onClick={e => e.stopPropagation()}>
            <button className="modal-close" onClick={() => setSelected(null)}><X size={20} /></button>

            <div className="modal-header-section">
              <div
                className="modal-avatar-gradient"
                style={{ background: getAvatarGradient(selected.full_name) }}
              >
                {selected.full_name?.[0]?.toUpperCase()}
              </div>
              <h2>{selected.full_name}</h2>
              <div className={`status-pill ${STATUS_MAP[selected.verification_status]?.color} modal-status-badge`}>
                <span className="status-dot" />
                {STATUS_MAP[selected.verification_status]?.label}
              </div>
            </div>

            <div className="modal-split-layout">
              <div className="modal-info-column">
                <h3 className="section-title">Ishtirokchi ma'lumotlari</h3>
                <div className="modal-details">
                  <div className="detail-row">
                    <span className="detail-label"><User size={14} /> F.I.O</span>
                    <strong className="detail-value">{selected.full_name}</strong>
                  </div>
                  <div className="detail-row">
                    <span className="detail-label">📱 Telefon</span>
                    <strong className="detail-value">{selected.phone}</strong>
                  </div>
                  <div className="detail-row">
                    <span className="detail-label"><GraduationCap size={14} /> Sinf</span>
                    <strong className="detail-value">{selected.grade}-sinf</strong>
                  </div>
                  <div className="detail-row">
                    <span className="detail-label"><BookOpen size={14} /> Fanlar</span>
                    <strong className="detail-value">{selected.subject}</strong>
                  </div>
                  <div className="detail-row">
                    <span className="detail-label"><CreditCard size={14} /> To'lov turi</span>
                    <strong className="detail-value">{PAYMENT_LABELS[selected.payment_type]}</strong>
                  </div>
                  <div className="detail-row">
                    <span className="detail-label"><Tag size={14} /> Jami Summa</span>
                    <strong className="detail-value highlighted-price">
                      {Number(190000 + ((selected.subject ? selected.subject.split(',').length : 1) - 1) * 90000).toLocaleString('ru-RU')} so'm
                    </strong>
                  </div>
                  <div className="detail-row">
                    <span className="detail-label"><Calendar size={14} /> Sana</span>
                    <strong className="detail-value">{formatDate(selected.registered_at)}</strong>
                  </div>
                  {selected.unique_code && (
                    <div className="detail-row code-row">
                      <span className="detail-label">🎟 Kod</span>
                      <strong className="detail-value unique-code-wrapper" onClick={(e) => handleCopy(selected.unique_code, selected.id, e)}>
                        <span className="unique-code">{selected.unique_code}</span>
                        {copiedId === selected.id ? <Check size={16} style={{color: '#10b981'}} /> : <Copy size={16} />}
                        {copiedId === selected.id && <span className="copy-tooltip-modal">Nusxalandi!</span>}
                      </strong>
                    </div>
                  )}
                  {selected.rejection_reason && (
                    <div className="detail-row rejection-row">
                      <span className="detail-label"><AlertTriangle size={14} /> Rad etilish sababi</span>
                      <strong className="detail-value error-text">{selected.rejection_reason}</strong>
                    </div>
                  )}
                </div>
              </div>

            </div>

            {selected.verification_status === 'pending' && (
              <div className="modal-actions-grid">
                <button
                  className="btn-approve-big"
                  onClick={() => handleApprove(selected.id)}
                  disabled={actionLoading}
                >
                  {actionLoading ? 'Tasdiqlanmoqda...' : "✅ Arizani tasdiqlash"}
                </button>
                <button
                  className="btn-reject-big"
                  onClick={() => handleRejectClick(selected.id)}
                  disabled={actionLoading}
                >
                  ❌ Rad etish
                </button>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Rejection Dialog Sub-Modal */}
      {showRejectDialog && (
        <div className="rejection-dialog-overlay" onClick={() => setShowRejectDialog(false)}>
          <div className="rejection-dialog-card animate-scale-up" onClick={e => e.stopPropagation()}>
            <div className="rejection-dialog-header">
              <AlertTriangle size={24} className="warn-icon" />
              <h3>Arizani rad etish sababi</h3>
            </div>

            <p className="rejection-dialog-intro">Iltimos, arizani rad etish sababini tanlang yoki o'zingiz yozing:</p>

            <div className="preset-reasons-list">
              {PRESET_REASONS.map(reason => (
                <button
                  key={reason}
                  type="button"
                  className={`preset-reason-btn ${rejectReason === reason ? 'selected' : ''}`}
                  onClick={() => setRejectReason(reason)}
                >
                  {reason}
                </button>
              ))}
            </div>

            <textarea
              className="rejection-textarea"
              placeholder="Batafsil sababini kiriting..."
              rows={3}
              value={rejectReason}
              onChange={e => setRejectReason(e.target.value)}
            />

            <div className="rejection-dialog-actions">
              <button
                className="btn-dialog-cancel"
                onClick={() => setShowRejectDialog(false)}
                disabled={actionLoading}
              >
                Bekor qilish
              </button>
              <button
                className="btn-dialog-confirm"
                onClick={handleRejectConfirm}
                disabled={actionLoading || !rejectReason.trim()}
              >
                {actionLoading ? 'Rad etilmoqda...' : 'Rad etishni tasdiqlash'}
              </button>
            </div>
          </div>
        </div>
      )}

    </div>
  )
}
