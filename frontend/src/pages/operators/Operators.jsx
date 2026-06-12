import React, { useState, useEffect, useCallback } from 'react'
import { UserPlus, Phone, Users, Trash2, Pencil, X, Check, RefreshCw, Search, Power } from 'lucide-react'
import { authFetch } from '../../config'

export default function Operators() {
  const [operators, setOperators] = useState([])
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [search, setSearch] = useState('')

  const [showForm, setShowForm] = useState(false)
  const [editing, setEditing] = useState(null) // operator object or null (new)
  const [form, setForm] = useState({ name: '', phone: '', is_active: true })
  const [error, setError] = useState('')

  const [deleteTarget, setDeleteTarget] = useState(null)

  const fetchData = useCallback(async () => {
    setLoading(true)
    try {
      const res = await authFetch('/registration/operators/')
      const data = await res.json()
      setOperators(Array.isArray(data) ? data : (data.results || []))
    } catch (e) {
      console.error(e)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => { fetchData() }, [fetchData])

  const openNew = () => {
    setEditing(null)
    setForm({ name: '', phone: '', is_active: true })
    setError('')
    setShowForm(true)
  }

  const openEdit = (op) => {
    setEditing(op)
    setForm({ name: op.name || '', phone: op.phone || '', is_active: op.is_active })
    setError('')
    setShowForm(true)
  }

  const handleSave = async () => {
    if (!form.name.trim()) {
      setError('Operator ismini kiriting')
      return
    }
    setSaving(true)
    setError('')
    try {
      const path = editing
        ? `/registration/operators/${editing.id}/`
        : '/registration/operators/'
      const method = editing ? 'PATCH' : 'POST'
      const res = await authFetch(path, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: form.name.trim(),
          phone: form.phone.trim() || null,
          is_active: form.is_active,
        }),
      })
      if (res.ok) {
        await fetchData()
        setShowForm(false)
      } else {
        const data = await res.json().catch(() => ({}))
        setError(data.detail || 'Saqlashda xatolik yuz berdi')
      }
    } catch (e) {
      setError('Server bilan bog\'lanishda xatolik')
    } finally {
      setSaving(false)
    }
  }

  const toggleActive = async (op) => {
    try {
      await authFetch(`/registration/operators/${op.id}/`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ is_active: !op.is_active }),
      })
      await fetchData()
    } catch (e) {
      console.error(e)
    }
  }

  const handleDelete = async () => {
    if (!deleteTarget) return
    setSaving(true)
    try {
      const res = await authFetch(`/registration/operators/${deleteTarget.id}/`, { method: 'DELETE' })
      if (res.ok) {
        await fetchData()
        setDeleteTarget(null)
      }
    } catch (e) {
      console.error(e)
    } finally {
      setSaving(false)
    }
  }

  const filtered = operators.filter(op => {
    const q = search.toLowerCase()
    return !q || op.name?.toLowerCase().includes(q) || op.phone?.includes(q)
  })

  const totalLeads = operators.reduce((sum, op) => sum + (op.participants_count || 0), 0)
  const activeCount = operators.filter(op => op.is_active).length

  return (
    <div className="max-w-6xl mx-auto">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
        <div>
          <h1 className="text-2xl md:text-3xl font-bold text-gray-900">Operatorlar</h1>
          <p className="text-gray-500 mt-1">Operatorlarni boshqaring va ularning natijalarini kuzating.</p>
        </div>
        <button
          onClick={openNew}
          className="inline-flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2.5 rounded-xl font-medium transition-colors shadow-sm"
        >
          <UserPlus size={18} />
          Yangi operator
        </button>
      </div>

      {/* Stat cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-5 mb-8">
        <div className="bg-white p-5 rounded-2xl border border-gray-200 shadow-sm">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-lg bg-blue-50 text-blue-600"><Users size={20} /></div>
            <div>
              <div className="text-2xl font-bold text-gray-900">{operators.length}</div>
              <div className="text-sm text-gray-500">Jami operatorlar</div>
            </div>
          </div>
        </div>
        <div className="bg-white p-5 rounded-2xl border border-gray-200 shadow-sm">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-lg bg-emerald-50 text-emerald-600"><Power size={20} /></div>
            <div>
              <div className="text-2xl font-bold text-gray-900">{activeCount}</div>
              <div className="text-sm text-gray-500">Faol operatorlar</div>
            </div>
          </div>
        </div>
        <div className="bg-white p-5 rounded-2xl border border-gray-200 shadow-sm">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-lg bg-purple-50 text-purple-600"><UserPlus size={20} /></div>
            <div>
              <div className="text-2xl font-bold text-gray-900">{totalLeads}</div>
              <div className="text-sm text-gray-500">Operatorlar olib kelgan mijozlar</div>
            </div>
          </div>
        </div>
      </div>

      {/* Toolbar */}
      <div className="flex items-center gap-3 mb-4">
        <div className="relative flex-1 max-w-sm">
          <Search size={18} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
          <input
            value={search}
            onChange={e => setSearch(e.target.value)}
            placeholder="Operator qidirish..."
            className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-gray-200 focus:border-blue-400 focus:ring-2 focus:ring-blue-100 outline-none text-sm"
          />
        </div>
        <button
          onClick={fetchData}
          className="inline-flex items-center gap-2 px-3 py-2.5 rounded-xl border border-gray-200 text-gray-600 hover:bg-gray-50 text-sm font-medium"
        >
          <RefreshCw size={16} className={loading ? 'animate-spin' : ''} />
          Yangilash
        </button>
      </div>

      {/* Table */}
      <div className="bg-white rounded-2xl border border-gray-200 shadow-sm overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead>
              <tr className="border-b border-gray-200 text-gray-500 text-xs uppercase tracking-wide bg-gray-50/50">
                <th className="px-5 py-3 font-medium">#</th>
                <th className="px-5 py-3 font-medium">Operator</th>
                <th className="px-5 py-3 font-medium">Telefon</th>
                <th className="px-5 py-3 font-medium text-center">Olib kelgan mijozlar</th>
                <th className="px-5 py-3 font-medium text-center">Holat</th>
                <th className="px-5 py-3 font-medium text-right">Amallar</th>
              </tr>
            </thead>
            <tbody className="text-sm">
              {loading && (
                <tr><td colSpan={6} className="px-5 py-10 text-center text-gray-400">Yuklanmoqda…</td></tr>
              )}
              {!loading && filtered.length === 0 && (
                <tr><td colSpan={6} className="px-5 py-10 text-center text-gray-400">
                  {search ? 'Operator topilmadi' : 'Hozircha operatorlar yo\'q. "Yangi operator" tugmasini bosing.'}
                </td></tr>
              )}
              {filtered.map((op, i) => (
                <tr key={op.id} className="border-b border-gray-100 hover:bg-gray-50 transition-colors">
                  <td className="px-5 py-4 text-gray-400">{i + 1}</td>
                  <td className="px-5 py-4">
                    <div className="flex items-center gap-3">
                      <div className="w-9 h-9 rounded-full bg-gradient-to-br from-blue-500 to-purple-500 text-white flex items-center justify-center font-semibold text-sm">
                        {op.name?.[0]?.toUpperCase() || '?'}
                      </div>
                      <span className="font-medium text-gray-900">{op.name}</span>
                    </div>
                  </td>
                  <td className="px-5 py-4 text-gray-600">
                    {op.phone ? (
                      <span className="inline-flex items-center gap-1.5"><Phone size={14} className="text-gray-400" />{op.phone}</span>
                    ) : <span className="text-gray-300">—</span>}
                  </td>
                  <td className="px-5 py-4 text-center">
                    <span className="inline-flex items-center justify-center min-w-8 px-2.5 py-1 rounded-full bg-blue-50 text-blue-700 font-semibold text-xs">
                      {op.participants_count ?? 0}
                    </span>
                  </td>
                  <td className="px-5 py-4 text-center">
                    <button
                      onClick={() => toggleActive(op)}
                      className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium border transition-colors ${
                        op.is_active
                          ? 'bg-emerald-50 text-emerald-700 border-emerald-200 hover:bg-emerald-100'
                          : 'bg-gray-100 text-gray-500 border-gray-200 hover:bg-gray-200'
                      }`}
                      title="Holatni o'zgartirish"
                    >
                      <span className={`w-1.5 h-1.5 rounded-full ${op.is_active ? 'bg-emerald-500' : 'bg-gray-400'}`} />
                      {op.is_active ? 'Faol' : 'Nofaol'}
                    </button>
                  </td>
                  <td className="px-5 py-4">
                    <div className="flex items-center justify-end gap-2">
                      <button
                        onClick={() => openEdit(op)}
                        className="p-2 rounded-lg text-gray-500 hover:bg-blue-50 hover:text-blue-600 transition-colors"
                        title="Tahrirlash"
                      >
                        <Pencil size={16} />
                      </button>
                      <button
                        onClick={() => setDeleteTarget(op)}
                        className="p-2 rounded-lg text-gray-500 hover:bg-red-50 hover:text-red-600 transition-colors"
                        title="O'chirish"
                      >
                        <Trash2 size={16} />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Create/Edit Modal */}
      {showForm && (
        <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4" onClick={() => setShowForm(false)}>
          <div className="bg-white rounded-2xl shadow-xl w-full max-w-md p-6" onClick={e => e.stopPropagation()}>
            <div className="flex items-center justify-between mb-5">
              <h2 className="text-lg font-semibold text-gray-900">
                {editing ? 'Operatorni tahrirlash' : 'Yangi operator qo\'shish'}
              </h2>
              <button onClick={() => setShowForm(false)} className="p-1.5 rounded-lg text-gray-400 hover:bg-gray-100">
                <X size={18} />
              </button>
            </div>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1.5">Ism *</label>
                <input
                  value={form.name}
                  onChange={e => setForm(p => ({ ...p, name: e.target.value }))}
                  placeholder="Masalan: Aziz Karimov"
                  className="w-full px-4 py-2.5 rounded-xl border border-gray-200 focus:border-blue-400 focus:ring-2 focus:ring-blue-100 outline-none"
                  autoFocus
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1.5">Telefon</label>
                <input
                  value={form.phone}
                  onChange={e => setForm(p => ({ ...p, phone: e.target.value }))}
                  placeholder="+998 90 123 45 67"
                  className="w-full px-4 py-2.5 rounded-xl border border-gray-200 focus:border-blue-400 focus:ring-2 focus:ring-blue-100 outline-none"
                />
              </div>
              <label className="flex items-center gap-3 cursor-pointer select-none">
                <input
                  type="checkbox"
                  checked={form.is_active}
                  onChange={e => setForm(p => ({ ...p, is_active: e.target.checked }))}
                  className="w-4 h-4 rounded accent-blue-600"
                />
                <span className="text-sm text-gray-700">Faol (ro'yxatdan o'tish formasida ko'rinadi)</span>
              </label>

              {error && <div className="text-sm text-red-600 bg-red-50 border border-red-100 rounded-lg px-3 py-2">{error}</div>}
            </div>

            <div className="flex gap-3 mt-6">
              <button
                onClick={() => setShowForm(false)}
                className="flex-1 px-4 py-2.5 rounded-xl border border-gray-200 text-gray-600 font-medium hover:bg-gray-50"
              >
                Bekor qilish
              </button>
              <button
                onClick={handleSave}
                disabled={saving}
                className="flex-1 inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-medium disabled:opacity-60"
              >
                <Check size={16} />
                {saving ? 'Saqlanmoqda…' : 'Saqlash'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Delete confirm */}
      {deleteTarget && (
        <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4" onClick={() => setDeleteTarget(null)}>
          <div className="bg-white rounded-2xl shadow-xl w-full max-w-sm p-6 text-center" onClick={e => e.stopPropagation()}>
            <div className="w-12 h-12 rounded-full bg-red-50 text-red-600 flex items-center justify-center mx-auto mb-4">
              <Trash2 size={22} />
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Operatorni o'chirish</h3>
            <p className="text-sm text-gray-500 mb-1">
              <strong>{deleteTarget.name}</strong> o'chirilsinmi?
            </p>
            {deleteTarget.participants_count > 0 && (
              <p className="text-xs text-amber-600 bg-amber-50 border border-amber-100 rounded-lg px-3 py-2 mb-1 mt-2">
                Bu operatorga {deleteTarget.participants_count} ta mijoz biriktirilgan. O'chirilsa, ular "operatorsiz" bo'lib qoladi.
              </p>
            )}
            <div className="flex gap-3 mt-5">
              <button
                onClick={() => setDeleteTarget(null)}
                className="flex-1 px-4 py-2.5 rounded-xl border border-gray-200 text-gray-600 font-medium hover:bg-gray-50"
              >
                Bekor qilish
              </button>
              <button
                onClick={handleDelete}
                disabled={saving}
                className="flex-1 px-4 py-2.5 rounded-xl bg-red-600 hover:bg-red-700 text-white font-medium disabled:opacity-60"
              >
                {saving ? 'O\'chirilmoqda…' : 'O\'chirish'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
