import React, { useState, useEffect } from 'react'
import { API_BASE } from '../../config'
import './Profile.css'

export default function Profile() {
  const [firstName, setFirstName] = useState('')
  const [lastName, setLastName] = useState('')
  const [phone, setPhone] = useState('+998')
  const [password, setPassword] = useState('')
  
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [message, setMessage] = useState({ type: '', text: '' })

  useEffect(() => {
    fetchProfile()
  }, [])

  const formatPhoneNumber = (digits) => {
    let formatted = '+998'
    if (digits.length > 3) {
      formatted += '-' + digits.slice(3, 5)
    }
    if (digits.length > 5) {
      formatted += '-' + digits.slice(5, 8)
    }
    if (digits.length > 8) {
      formatted += '-' + digits.slice(8, 10)
    }
    if (digits.length > 10) {
      formatted += '-' + digits.slice(10, 12)
    }
    return formatted
  }

  const fetchProfile = async () => {
    setLoading(true)
    setMessage({ type: '', text: '' })
    const token = localStorage.getItem('access_token')
    try {
      const res = await fetch(`${API_BASE}/users/profile/`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      if (res.ok) {
        const data = await res.json()
        setFirstName(data.first_name || '')
        setLastName(data.last_name || '')
        
        const rawPhone = data.username || ''
        const digits = rawPhone.replace(/\D/g, '')
        setPhone(formatPhoneNumber(digits))
      } else {
        setMessage({ type: 'error', text: 'Profil ma\'lumotlarini yuklab bo\'lmadi' })
      }
    } catch (err) {
      setMessage({ type: 'error', text: 'Server bilan ulanishda xatolik yuz berdi' })
    } finally {
      setLoading(false)
    }
  }

  const handlePhoneChange = (e) => {
    const inputVal = e.target.value
    let digits = inputVal.replace(/\D/g, '')
    
    if (!digits.startsWith('998')) {
      if ('998'.startsWith(digits)) {
        digits = '998'
      } else {
        digits = '998' + digits
      }
    }
    digits = digits.slice(0, 12)
    setPhone(formatPhoneNumber(digits))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setSaving(true)
    setMessage({ type: '', text: '' })

    const token = localStorage.getItem('access_token')
    const rawPhone = phone.replace(/-/g, '')

    if (rawPhone.length < 12) {
      setMessage({ type: 'error', text: 'Telefon raqam noto\'g\'ri kiritilgan' })
      setSaving(false)
      return
    }

    const payload = {
      first_name: firstName,
      last_name: lastName,
      username: rawPhone
    }

    if (password.trim()) {
      payload.password = password
    }

    try {
      const res = await fetch(`${API_BASE}/users/profile/`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(payload)
      })

      if (res.ok) {
        setMessage({ type: 'success', text: 'Profil muvaffaqiyatli saqlandi!' })
        setPassword('') // Clear password field after save
        window.dispatchEvent(new Event('profileUpdated'))
      } else {
        const errorData = await res.json()
        if (errorData.username) {
          setMessage({ type: 'error', text: 'Ushbu telefon raqam band!' })
        } else {
          setMessage({ type: 'error', text: 'Xatolik yuz berdi, iltimos qaytadan urinib ko\'ring' })
        }
      }
    } catch (err) {
      setMessage({ type: 'error', text: 'Serverga ulanib bo\'lmadi' })
    } finally {
      setSaving(false)
    }
  }

  if (loading) {
    return (
      <div className="profile-loading">
        <div className="loading-spinner"></div>
        <p>Yuklanmoqda...</p>
      </div>
    )
  }

  return (
    <div className="profile-page">
      <div className="profile-header">
        <div className="profile-header-content">
          <div className="profile-avatar-large">
            {firstName ? firstName[0].toUpperCase() : 'A'}
          </div>
          <div>
            <h1>Profil Sozlamalari</h1>
            <p>Shaxsiy ma'lumotlaringizni va parolingizni boshqaring</p>
          </div>
        </div>
      </div>

      <div className="profile-content">
        <form onSubmit={handleSubmit} className="profile-form-card">
          {message.text && (
            <div className={`profile-alert ${message.type === 'success' ? 'alert-success' : 'alert-error'}`}>
              {message.text}
            </div>
          )}

          <div className="profile-form-row">
            <div className="form-group-profile">
              <label>Ism</label>
              <input
                type="text"
                value={firstName}
                onChange={e => setFirstName(e.target.value)}
                placeholder="Ismingizni kiriting"
                required
              />
            </div>

            <div className="form-group-profile">
              <label>Familya</label>
              <input
                type="text"
                value={lastName}
                onChange={e => setLastName(e.target.value)}
                placeholder="Familyangizni kiriting"
                required
              />
            </div>
          </div>

          <div className="form-group-profile">
            <label>Telefon raqam (Login)</label>
            <input
              type="text"
              value={phone}
              onChange={handlePhoneChange}
              placeholder="+998-90-123-45-67"
              required
            />
          </div>

          <div className="form-group-profile">
            <label>Yangi Parol (ixtiyoriy)</label>
            <input
              type="password"
              value={password}
              onChange={e => setPassword(e.target.value)}
              placeholder="O'zgartirmoqchi bo'lsangiz yangi parol kiriting"
            />
          </div>

          <div className="profile-form-actions">
            <button type="submit" className="btn-save-profile" disabled={saving}>
              {saving ? 'Saqlanmoqda...' : 'Saqlash'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
