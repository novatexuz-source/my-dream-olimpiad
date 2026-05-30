import React, { useState, useEffect } from 'react'
import './Register.css'
import { API_BASE } from '../../config'

// Telegram WebApp SDK
const tg = window.Telegram?.WebApp

const SUBJECTS = ['Matematika', 'Ingliz tili', 'Rus tili']
const GRADES = Array.from({ length: 11 }, (_, i) => i + 1)
const PAYMENT_TYPES = [
  { value: 'click', label: 'Click', icon: '💳' },
  { value: 'payme', label: 'Payme', icon: '📱' },
  { value: 'cash', label: 'Naqd pul', icon: '💵' },
]

const STEPS = ['Shaxsiy', 'Ta\'lim', 'To\'lov', 'Tasdiqlash']

export default function Register() {
  const [step, setStep] = useState(1)
  const [loading, setLoading] = useState(false)
  const [success, setSuccess] = useState(false)

  const getPrice = () => {
    const num = Math.max(1, form.subjects.length)
    return 190000 + (num - 1) * 90000
  }
  const [error, setError] = useState('')

  const [form, setForm] = useState({
    id: '',
    first_name: '',
    last_name: '',
    phone: '+998',
    grade: '',
    subjects: [],
    payment_type: '',
  })

  // Phone formatter: +998-90-123-45-67
  const formatPhone = (raw) => {
    // Always start with +998
    let digits = raw.replace(/\D/g, '')
    if (!digits.startsWith('998')) digits = '998' + digits.replace(/^998/, '')
    // Limit to 12 digits (998 + 9 digits)
    digits = digits.slice(0, 12)
    // Format: +998-XX-XXX-XX-XX
    let result = '+998'
    if (digits.length > 3) result += '-' + digits.slice(3, 5)
    if (digits.length > 5) result += '-' + digits.slice(5, 8)
    if (digits.length > 8) result += '-' + digits.slice(8, 10)
    if (digits.length > 10) result += '-' + digits.slice(10, 12)
    return result
  }

  const handlePhoneChange = (e) => {
    const formatted = formatPhone(e.target.value)
    setForm(prev => ({ ...prev, phone: formatted }))
    setErrors(prev => ({ ...prev, phone: '' }))
  }

  const [errors, setErrors] = useState({})

  // Initialize Telegram WebApp and fetch data
  useEffect(() => {
    if (tg) {
      tg.ready()
      tg.expand()
      tg.setHeaderColor('#0b0a1f')
      tg.setBackgroundColor('#0b0a1f')

      const urlParams = new URLSearchParams(window.location.search);
      const action = urlParams.get('action');
      const id = urlParams.get('id');

      if (id) {
        fetch(`${API_BASE}/registration/get_by_id/?id=${id}`)
          .then(res => {
            if (res.ok) return res.json()
            throw new Error('Not found')
          })
          .then(data => {
            setForm({
              id: data.id,
              first_name: data.first_name || '',
              last_name: data.last_name || '',
              phone: data.phone || '+998',
              grade: data.grade || '',
              subjects: data.subjects || [],
              payment_type: data.payment_type || '',
            })
          })
          .catch(e => console.log('Error fetching data'))
      } else if (action === 'new') {
        // Leave form blank with no id (new profile)
        setForm({
          id: '',
          first_name: '',
          last_name: '',
          phone: '+998',
          grade: '',
          subjects: [],
          payment_type: '',
        })
      }
    }
  }, [])

  const update = (field, val) => {
    setForm(prev => ({ ...prev, [field]: val }))
    setErrors(prev => ({ ...prev, [field]: '' }))
  }

  const validateStep = () => {
    const newErrors = {}
    if (step === 1) {
      if (!form.first_name.trim()) newErrors.first_name = 'Ismingizni kiriting'
      if (!form.last_name.trim()) newErrors.last_name = 'Familiyangizni kiriting'
      const phoneDigits = form.phone.replace(/\D/g, '')
      if (phoneDigits.length < 12) newErrors.phone = 'Telefon raqamni to\'liq kiriting (+998-XX-XXX-XX-XX)'
    }
    if (step === 2) {
      if (!form.grade) newErrors.grade = 'Sinfingizni tanlang'
      if (form.subjects.length === 0) newErrors.subject = 'Kamida bitta fan tanlang'
    }
    if (step === 3) {
      if (!form.payment_type) newErrors.payment_type = 'To\'lov turini tanlang'
    }
    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const nextStep = () => {
    if (validateStep()) setStep(s => s + 1)
  }

  const prevStep = () => setStep(s => s - 1)

  const handleSubmit = async () => {
    setLoading(true)
    setError('')
    try {
      // Get Telegram user info if opened from Telegram
      const telegramId = tg?.initDataUnsafe?.user?.id
        ? `tg_${tg.initDataUnsafe.user.id}`
        : null

      const res = await fetch(`${API_BASE}/registration/register/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          id: form.id,
          full_name: `${form.last_name} ${form.first_name}`,
          phone: form.phone,
          grade: form.grade,
          subject: form.subjects.join(', '),
          payment_type: form.payment_type,
          telegram_id: telegramId,
        }),
      })
      const data = await res.json()
      if (res.ok) {
        setSuccess(true)
        // Don't auto-close - let user press the button
      } else {
        setError(data.error || 'Xatolik yuz berdi')
      }
    } catch (e) {
      setError('Server bilan bog\'lanishda xatolik. Qayta urinib ko\'ring.')
    } finally {
      setLoading(false)
    }
  }

  if (success) {
    return (
      <div className="reg-wrapper">
        <div className="reg-success-card">
          <div className="success-icon">🎉</div>
          <h2>Arizangiz qabul qilindi!</h2>
          <p>Hurmatli <strong>{form.last_name} {form.first_name}</strong>,</p>
          <p>Arizangiz muvaffaqiyatli yuborildi. Operatorlarimiz tekshirib,
            <strong> {form.phone}</strong> raqami orqali bog'lanadilar.</p>
          <div className="success-details">
            <div className="detail-row"><span>📚 Fan:</span><strong>{form.subjects.join(', ')}</strong></div>
            <div className="detail-row"><span>🏫 Sinf:</span><strong>{form.grade}-sinf</strong></div>
            <div className="detail-row"><span>💳 To'lov:</span><strong>{PAYMENT_TYPES.find(p => p.value === form.payment_type)?.label} ({getPrice().toLocaleString('ru-RU')} so'm)</strong></div>
          </div>
          <p className="warning-note">⚠️ Test kuni pasport yoki tug'ilganlik guvohnomangizni olib keling.</p>
          <button className="btn-back-to-bot" onClick={() => tg ? tg.close() : window.close()}>
            ← Botga qaytish
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="reg-wrapper">
      {/* Header */}
      <div className="reg-header">
        <div className="reg-logo">🏆</div>
        <h1>My Dream International Olimpiad</h1>
        <p>Ro'yxatdan o'tish</p>
      </div>

      {/* Progress bar */}
      <div className="reg-progress">
        {STEPS.map((label, i) => (
          <div key={i} className={`progress-step ${step > i + 1 ? 'done' : ''} ${step === i + 1 ? 'active' : ''}`}>
            <div className="step-circle">
              {step > i + 1 ? '✓' : i + 1}
            </div>
            <span>{label}</span>
          </div>
        ))}
        <div className="progress-line">
          <div className="progress-fill" style={{ width: `${((step - 1) / (STEPS.length - 1)) * 100}%` }} />
        </div>
      </div>

      {/* Card */}
      <div className="reg-card">

        {/* Step 1: Personal */}
        {step === 1 && (
          <div className="step-content">
            <h2 className="step-title">Shaxsiy ma'lumotlar</h2>
            <p className="step-subtitle">Ism va familiyangizni sertifikatdagidek to'g'ri kiriting.</p>
            <div className="form-row">
              <div className="form-group">
                <label>Ismingiz</label>
                <input
                  type="text"
                  placeholder="Abdurasul"
                  value={form.first_name}
                  onChange={e => update('first_name', e.target.value)}
                  className={errors.first_name ? 'error' : ''}
                />
                {errors.first_name && <span className="err-msg">{errors.first_name}</span>}
              </div>
              <div className="form-group">
                <label>Familiyangiz</label>
                <input
                  type="text"
                  placeholder="Sobirov"
                  value={form.last_name}
                  onChange={e => update('last_name', e.target.value)}
                  className={errors.last_name ? 'error' : ''}
                />
                {errors.last_name && <span className="err-msg">{errors.last_name}</span>}
              </div>
            </div>
            <div className="form-group">
              <label>Telefon raqam</label>
              <input
                type="tel"
                placeholder="+998-90-123-45-67"
                value={form.phone}
                onChange={handlePhoneChange}
                onFocus={e => { if (e.target.value === '') setForm(p => ({...p, phone: '+998'})) }}
                className={errors.phone ? 'error' : ''}
                inputMode="numeric"
                maxLength={17}
              />
              {errors.phone && <span className="err-msg">{errors.phone}</span>}
            </div>
          </div>
        )}

        {/* Step 2: Education */}
        {step === 2 && (
          <div className="step-content">
            <h2 className="step-title">Ta'lim ma'lumotlari</h2>
            <p className="step-subtitle">Sinfingizni va qatnashmoqchi bo'lgan fanlaringizni tanlang.</p>
            <div className="form-group">
              <label>Sinfingiz</label>
              <div className="grade-grid">
                {GRADES.map(g => (
                  <button
                    key={g}
                    className={`grade-btn ${form.grade === g ? 'selected' : ''}`}
                    onClick={() => update('grade', g)}
                  >
                    {g}-sinf
                  </button>
                ))}
              </div>
              {errors.grade && <span className="err-msg">{errors.grade}</span>}
            </div>
            <div className="form-group">
              <label>Olimpiada fanlari <span className="multi-hint">(bir nechta tanlash mumkin)</span></label>
              <div className="subject-list">
                {SUBJECTS.map(s => {
                  const selected = form.subjects.includes(s)
                  return (
                    <button
                      key={s}
                      className={`subject-btn ${selected ? 'selected' : ''}`}
                      onClick={() => {
                        setForm(prev => ({
                          ...prev,
                          subjects: selected
                            ? prev.subjects.filter(x => x !== s)
                            : [...prev.subjects, s]
                        }))
                        setErrors(prev => ({ ...prev, subject: '' }))
                      }}
                    >
                      <span>{s === 'Matematika' ? '🔢' : s === 'Ingliz tili' ? '🇬🇧' : '🇷🇺'} {s}</span>
                      {selected && <span className="check">✓</span>}
                    </button>
                  )
                })}
              </div>
              {form.subjects.length > 0 && (
                <div className="selected-subjects">
                  Tanlangan: <strong>{form.subjects.join(' · ')}</strong>
                </div>
              )}
              {errors.subject && <span className="err-msg">{errors.subject}</span>}
            </div>
          </div>
        )}

        {/* Step 3: Payment */}
        {step === 3 && (
          <div className="step-content">
            <h2 className="step-title">To'lov turi</h2>
            <p className="step-subtitle">Qulay to'lov usulini tanlang. To'lov tasdiqlangach faollashtiriladi.</p>
            <div className="price-badge">{getPrice().toLocaleString('ru-RU')} so'm</div>
            <div className="payment-list">
              {PAYMENT_TYPES.map(p => (
                <button
                  key={p.value}
                  className={`payment-btn ${form.payment_type === p.value ? 'selected' : ''}`}
                  onClick={() => update('payment_type', p.value)}
                >
                  <span className="pay-icon">{p.icon}</span>
                  <span>{p.label}</span>
                  {form.payment_type === p.value && <span className="check">✓</span>}
                </button>
              ))}
            </div>
            {errors.payment_type && <span className="err-msg">{errors.payment_type}</span>}
          </div>
        )}

        {/* Step 4: Confirm */}
        {step === 4 && (
          <div className="step-content">
            <h2 className="step-title">Ma'lumotlarni tasdiqlang</h2>
            <p className="step-subtitle">Yuborishdan oldin barcha ma'lumotlar to'g'riligiga ishonch hosil qiling.</p>
            <div className="confirm-notice">
              ⚠️ Bu ma'lumotlar sertifikatda xuddi shunday tartibda chiqadi. Diqqat bilan tekshiring!
            </div>
            <div className="confirm-list">
              <div className="confirm-row"><span>👤 Ism</span><strong>{form.first_name}</strong></div>
              <div className="confirm-row"><span>👤 Familiya</span><strong>{form.last_name}</strong></div>
              <div className="confirm-row"><span>📱 Telefon</span><strong>{form.phone}</strong></div>
              <div className="confirm-row"><span>🏫 Sinf</span><strong>{form.grade}-sinf</strong></div>
              <div className="confirm-row"><span>📚 Fan</span><strong>{form.subjects.join(', ')}</strong></div>
              <div className="confirm-row"><span>💳 To'lov</span><strong>{PAYMENT_TYPES.find(p => p.value === form.payment_type)?.label} ({getPrice().toLocaleString('ru-RU')} so'm)</strong></div>
            </div>
            {error && <div className="error-banner">{error}</div>}
          </div>
        )}

        {/* Buttons */}
        <div className="btn-row">
          {step > 1 && (
            <button className="btn-secondary" onClick={prevStep} disabled={loading}>
              ← Orqaga
            </button>
          )}
          {step < 4 ? (
            <button className="btn-primary" onClick={nextStep}>
              Davom etish →
            </button>
          ) : (
            <button className="btn-submit" onClick={handleSubmit} disabled={loading}>
              {loading ? <span className="spinner" /> : '🚀 Ariza yuborish'}
            </button>
          )}
        </div>
      </div>
    </div>
  )
}
