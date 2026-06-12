import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Users, CheckCircle, CreditCard, Clock, FilePlus2, Trophy, ArrowRight } from 'lucide-react';
import { authFetch } from '../../config';

// Tailwind can't generate runtime-built class names (`bg-${color}-500`),
// so every accent variant is spelled out statically here.
const ACCENTS = {
  blue:    { iconBg: 'bg-blue-50',    iconText: 'text-blue-600',    bar: 'bg-blue-500' },
  emerald: { iconBg: 'bg-emerald-50', iconText: 'text-emerald-600', bar: 'bg-emerald-500' },
  amber:   { iconBg: 'bg-amber-50',   iconText: 'text-amber-600',   bar: 'bg-amber-500' },
  purple:  { iconBg: 'bg-purple-50',  iconText: 'text-purple-600',  bar: 'bg-purple-500' },
};

const STATUS_LABELS = {
  pending:  { text: 'Kutilmoqda',   badge: 'bg-amber-50 text-amber-700 border-amber-200',     dot: 'bg-amber-500' },
  approved: { text: 'Tasdiqlangan', badge: 'bg-emerald-50 text-emerald-700 border-emerald-200', dot: 'bg-emerald-500' },
  rejected: { text: 'Rad etilgan',  badge: 'bg-red-50 text-red-700 border-red-200',           dot: 'bg-red-500' },
};

const PAYMENT_LABELS = { click: 'Click', payme: 'Payme', cash: 'Naqd' };

const formatMoney = (sum) => {
  if (sum >= 1_000_000) return `${(sum / 1_000_000).toFixed(1)}M so'm`;
  return `${sum.toLocaleString('uz-UZ')} so'm`;
};

const StatCard = ({ title, value, icon: Icon, accent }) => {
  const a = ACCENTS[accent] || ACCENTS.blue;
  return (
    <div className="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm hover:shadow-md transition-shadow duration-300 relative overflow-hidden">
      <div className={`absolute left-0 top-0 bottom-0 w-1 ${a.bar}`}></div>
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-gray-500 font-medium text-sm">{title}</h3>
        <div className={`p-2 rounded-lg ${a.iconBg} ${a.iconText}`}>
          <Icon size={20} />
        </div>
      </div>
      <div className="text-3xl font-bold text-gray-900">{value}</div>
    </div>
  );
};

export const Dashboard = () => {
  const navigate = useNavigate();
  const [participants, setParticipants] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    (async () => {
      try {
        const res = await authFetch('/registration/participants/');
        if (res.ok) {
          const data = await res.json();
          setParticipants(Array.isArray(data) ? data : (data.results || []));
        }
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  const approved = participants.filter(p => p.verification_status === 'approved');
  const pending = participants.filter(p => p.verification_status === 'pending');
  const revenue = approved.reduce((sum, p) => {
    const amount = p.payments?.[0]?.amount;
    return sum + (amount ? Number(amount) : 0);
  }, 0);

  const recent = [...participants]
    .sort((a, b) => new Date(b.registered_at) - new Date(a.registered_at))
    .slice(0, 6);

  return (
    <div className="max-w-7xl mx-auto">
      <div className="mb-8">
        <h1 className="text-2xl md:text-3xl font-bold text-gray-900">Olimpiada Boshqaruvi</h1>
        <p className="text-gray-500 mt-1">Xush kelibsiz, asosiy ko'rsatkichlar bilan tanishing.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5 mb-8">
        <StatCard title="Jami Ishtirokchilar" value={loading ? '…' : participants.length.toLocaleString('uz-UZ')} icon={Users} accent="blue" />
        <StatCard title="Tasdiqlanganlar" value={loading ? '…' : approved.length.toLocaleString('uz-UZ')} icon={CheckCircle} accent="emerald" />
        <StatCard title="Kutayotganlar" value={loading ? '…' : pending.length.toLocaleString('uz-UZ')} icon={Clock} accent="amber" />
        <StatCard title="Kassa (Tasdiqlangan)" value={loading ? '…' : formatMoney(revenue)} icon={CreditCard} accent="purple" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-white p-6 rounded-2xl border border-gray-200 shadow-sm">
          <div className="flex items-center justify-between mb-5">
            <h2 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
              <div className="w-1.5 h-6 bg-blue-500 rounded-full"></div>
              So'nggi Arizalar
            </h2>
            <button
              onClick={() => navigate('/leads')}
              className="text-blue-600 hover:text-blue-700 text-sm font-medium flex items-center gap-1 transition-colors"
            >
              Barchasi <ArrowRight size={14} />
            </button>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-gray-200 text-gray-500 text-xs uppercase tracking-wide">
                  <th className="pb-3 font-medium">F.I.SH</th>
                  <th className="pb-3 font-medium">Sinf / Fan</th>
                  <th className="pb-3 font-medium">To'lov</th>
                  <th className="pb-3 font-medium">Holat</th>
                </tr>
              </thead>
              <tbody className="text-sm">
                {loading && (
                  <tr><td colSpan={4} className="py-6 text-gray-400 text-center">Yuklanmoqda…</td></tr>
                )}
                {recent.length === 0 && !loading && (
                  <tr><td colSpan={4} className="py-6 text-gray-400 text-center">Hozircha arizalar yo'q</td></tr>
                )}
                {recent.map((item) => {
                  const st = STATUS_LABELS[item.verification_status] || STATUS_LABELS.pending;
                  return (
                    <tr
                      key={item.id}
                      onClick={() => navigate('/leads')}
                      className="border-b border-gray-100 hover:bg-gray-50 transition-colors cursor-pointer"
                    >
                      <td className="py-3.5 font-medium text-gray-900">{item.full_name}</td>
                      <td className="py-3.5 text-gray-500">{item.grade}-sinf, {item.subject}</td>
                      <td className="py-3.5">
                        <span className="px-2.5 py-1 bg-gray-100 text-gray-700 rounded-full text-xs font-medium">
                          {PAYMENT_LABELS[item.payment_type] || item.payment_type}
                        </span>
                      </td>
                      <td className="py-3.5">
                        <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium border ${st.badge}`}>
                          <span className={`w-1.5 h-1.5 rounded-full ${st.dot}`}></span>
                          {st.text}
                        </span>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>

        <div className="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm h-fit">
          <h2 className="text-lg font-semibold text-gray-900 flex items-center gap-2 mb-5">
            <div className="w-1.5 h-6 bg-purple-500 rounded-full"></div>
            Tezkor Harakatlar
          </h2>
          <div className="space-y-3">
            <button
              onClick={() => navigate('/tests/new')}
              className="w-full flex items-center justify-between p-4 rounded-xl bg-blue-50 border border-blue-100 hover:border-blue-300 hover:bg-blue-100/60 transition-all text-blue-700 group"
            >
              <span className="font-medium">Yangi test qo'shish</span>
              <div className="bg-blue-100 p-2 rounded-lg group-hover:scale-110 transition-transform">
                <FilePlus2 size={16} />
              </div>
            </button>
            <button
              onClick={() => navigate('/results')}
              className="w-full flex items-center justify-between p-4 rounded-xl bg-emerald-50 border border-emerald-100 hover:border-emerald-300 hover:bg-emerald-100/60 transition-all text-emerald-700 group"
            >
              <span className="font-medium">Natijalarni ko'rish</span>
              <div className="bg-emerald-100 p-2 rounded-lg group-hover:scale-110 transition-transform">
                <Trophy size={16} />
              </div>
            </button>
            <button
              onClick={() => navigate('/pending')}
              className="w-full flex items-center justify-between p-4 rounded-xl bg-amber-50 border border-amber-100 hover:border-amber-300 hover:bg-amber-100/60 transition-all text-amber-700 group"
            >
              <span className="font-medium">Kutilayotgan arizalar</span>
              <div className="bg-amber-100 p-2 rounded-lg group-hover:scale-110 transition-transform">
                <Clock size={16} />
              </div>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
