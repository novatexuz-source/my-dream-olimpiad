import React from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { Dashboard } from './pages/admin/Dashboard'
import Register from './pages/register/Register'
import Leads from './pages/leads/Leads'
import Login from './pages/auth/Login'
import AdminLayout from './components/layout/AdminLayout'
import Tests from './pages/tests/Tests'
import AddTest from './pages/tests/AddTest'
import ExamLogin from './pages/exam/ExamLogin'
import TakeExam from './pages/exam/TakeExam'
import ExamResult from './pages/exam/ExamResult'
import Calls from './pages/calls/Calls'
import Profile from './pages/profile/Profile'
import Results from './pages/results/Results'
import Monitor from './pages/monitor/Monitor'
import Operators from './pages/operators/Operators'

const PrivateRoute = ({ children }) => {
  const token = localStorage.getItem('access_token')
  if (!token) {
    return <Navigate to="/login" replace />
  }
  return children
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public Routes */}
        <Route path="/" element={<Register />} />
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route path="/monitor" element={<Monitor />} />


        {/* Student Exam Routes */}
        <Route path="/exam/login" element={<ExamLogin />} />
        <Route path="/exam/take/:sessionId" element={<TakeExam />} />
        <Route path="/exam/result/:sessionId" element={<ExamResult />} />
        
        {/* Protected Admin Routes inside Layout */}
        <Route path="/" element={
          <PrivateRoute>
            <AdminLayout />
          </PrivateRoute>
        }>
          <Route path="leads" element={<Leads defaultStatus="all" />} />
          <Route path="pending" element={<Leads defaultStatus="pending" />} />
          <Route path="approved" element={<Leads defaultStatus="approved" />} />
          <Route path="rejected" element={<Leads defaultStatus="rejected" />} />
          <Route path="tests" element={<Tests />} />
          <Route path="tests/new" element={<AddTest />} />
          <Route path="operators" element={<Operators />} />
          <Route path="calls" element={<Calls />} />
          <Route path="profile" element={<Profile />} />
          <Route path="results" element={<Results />} />
          <Route path="admin/dashboard" element={<Dashboard />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App

