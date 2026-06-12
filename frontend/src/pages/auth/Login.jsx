import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import logoImg from '../../assets/logo.jpg'
import { API_BASE } from '../../config'
import './Login.css'

export default function Login() {
  const [phone, setPhone] = useState('+998')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const handlePhoneChange = (e) => {
    const inputVal = e.target.value
    
    // Extract only digits from the input
    let digits = inputVal.replace(/\D/g, '')
    
    // Ensure it starts with 998.
    if (!digits.startsWith('998')) {
      if ('998'.startsWith(digits)) {
        digits = '998'
      } else {
        digits = '998' + digits
      }
    }
    
    // limit to 12 digits (998 + 9 digits)
    digits = digits.slice(0, 12)
    
    // Build formatted string (+998-90-123-45-67)
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
    
    setPhone(formatted)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    const rawPhone = phone.replace(/-/g, '')
    if (rawPhone.length < 13 || !password) {
      setError("Iltimos barcha maydonlarni to'ldiring")
      return
    }

    setLoading(true)
    setError('')

    try {
      const res = await fetch(`${API_BASE}/token/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: rawPhone, password })
      })

      const data = await res.json()

      if (res.ok) {
        localStorage.setItem('access_token', data.access)
        localStorage.setItem('refresh_token', data.refresh)
        navigate('/admin/dashboard')
      } else {
        setError("Telefon raqam yoki parol noto'g'ri")
      }
    } catch (err) {
      setError("Server bilan ulanishda xatolik yuz berdi")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login-page">
      <div className="login-card">
        <div className="login-header">
          <img src={logoImg} alt="Logo" className="login-logo-img" />
          <h1>Tizimga kirish</h1>
          <p>My Dream International Olimpiad</p>
        </div>

        {error && <div className="login-error">{error}</div>}

        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label>Telefon raqam</label>
            <input
              type="text"
              value={phone}
              onChange={handlePhoneChange}
              placeholder="+998-90-123-45-67"
              required
            />
          </div>

          <div className="form-group">
            <label>Parol</label>
            <input
              type="password"
              value={password}
              onChange={e => setPassword(e.target.value)}
              placeholder="••••••••"
              required
            />
          </div>

          <button type="submit" className="btn-login" disabled={loading}>
            {loading ? 'Tekshirilmoqda...' : 'Kirish'}
          </button>
        </form>
      </div>
    </div>
  )
}
