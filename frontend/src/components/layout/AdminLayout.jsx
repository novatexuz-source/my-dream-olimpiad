import React, { useState, useEffect } from 'react'
import { Outlet, NavLink, Link, useNavigate } from 'react-router-dom'
import logoImg from '../../assets/logo.jpg'
import { API_BASE } from '../../config'
import './AdminLayout.css'

export default function AdminLayout() {
  const navigate = useNavigate()
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [user, setUser] = useState(null)

  useEffect(() => {
    const fetchUser = () => {
      const token = localStorage.getItem('access_token')
      if (token) {
        fetch(`${API_BASE}/users/profile/`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })
        .then(res => res.json())
        .then(data => {
          if (data && data.first_name) {
            setUser(data)
          }
        })
        .catch(() => {})
      }
    }

    fetchUser()
    window.addEventListener('profileUpdated', fetchUser)
    return () => {
      window.removeEventListener('profileUpdated', fetchUser)
    }
  }, [])

  const handleLogout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    navigate('/login')
  }

  return (
    <div className="admin-layout">
      {/* Sidebar Overlay for Mobile */}
      {sidebarOpen && <div className="sidebar-overlay" onClick={() => setSidebarOpen(false)} />}

      {/* Sidebar */}
      <aside className={`sidebar ${sidebarOpen ? 'open' : ''}`}>
        <div className="sidebar-logo">
          <img src={logoImg} alt="Logo" className="sidebar-logo-img" />
          <span>My Dream Olympiad</span>
        </div>

        <nav className="sidebar-nav">
          <NavLink to="/admin/dashboard" className="nav-item" onClick={() => setSidebarOpen(false)}>
            <span className="nav-icon">📊</span>
            Boshqaruv paneli
          </NavLink>
          <div style={{ margin: '12px 0', borderBottom: '1px solid #f3f4f6' }}></div>
          <NavLink to="/leads" className="nav-item" onClick={() => setSidebarOpen(false)}>
            <span className="nav-icon">📋</span>
            Lidlar (Barchasi)
          </NavLink>
          <NavLink to="/pending" className="nav-item" onClick={() => setSidebarOpen(false)}>
            <span className="nav-icon">⏳</span>
            Kutilmoqda
          </NavLink>
          <NavLink to="/approved" className="nav-item" onClick={() => setSidebarOpen(false)}>
            <span className="nav-icon">✅</span>
            Tasdiqlangan
          </NavLink>
          <NavLink to="/rejected" className="nav-item" onClick={() => setSidebarOpen(false)}>
            <span className="nav-icon">❌</span>
            Rad etilgan
          </NavLink>
          <div style={{ margin: '12px 0', borderBottom: '1px solid #f3f4f6' }}></div>
          <NavLink to="/operators" className="nav-item" onClick={() => setSidebarOpen(false)}>
            <span className="nav-icon">🎧</span>
            Operatorlar
          </NavLink>
          <NavLink to="/calls" className="nav-item" onClick={() => setSidebarOpen(false)}>
            <span className="nav-icon">📞</span>
            Qo'ng'iroqlar
          </NavLink>
          <NavLink to="/results" className="nav-item" onClick={() => setSidebarOpen(false)}>
            <span className="nav-icon">🏆</span>
            Natijalar
          </NavLink>
          <NavLink to="/tests" className="nav-item" onClick={() => setSidebarOpen(false)}>
            <span className="nav-icon">📝</span>
            Testlar bazasi
          </NavLink>
          <NavLink to="/profile" className="nav-item" onClick={() => setSidebarOpen(false)}>
            <span className="nav-icon">👤</span>
            Profil
          </NavLink>
        </nav>
      </aside>

      {/* Main Content Area */}
      <div className="main-wrapper">
        {/* Header */}
        <header className="admin-header">
          <div className="header-left">
            <button className="menu-btn" onClick={() => setSidebarOpen(!sidebarOpen)}>
              ☰
            </button>
            <h2 className="page-title">Admin Panel</h2>
          </div>
          
          <div className="header-right">
            <Link to="/profile" className="admin-profile" style={{ textDecoration: 'none' }}>
              <div className="admin-avatar">
                {user && user.first_name ? user.first_name[0].toUpperCase() : 'A'}
              </div>
              <span className="admin-name">
                {user && user.first_name ? `${user.first_name} ${user.last_name || ''}` : 'Admin'}
              </span>
            </Link>
            <button className="btn-logout" onClick={handleLogout}>
              Chiqish
            </button>
          </div>
        </header>

        {/* Page Content */}
        <main className="admin-content">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
