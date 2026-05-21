import React from 'react';
import { Users, CheckCircle, XCircle, CreditCard, Clock } from 'lucide-react';

const StatCard = ({ title, value, icon: Icon, colorClass }) => (
  <div className="bg-[#1e1e24] p-6 rounded-2xl border border-white/5 shadow-lg relative overflow-hidden group hover:border-white/20 transition-all duration-300">
    <div className={`absolute -right-6 -top-6 w-24 h-24 rounded-full blur-2xl opacity-20 group-hover:opacity-40 transition-opacity duration-300 ${colorClass}`}></div>
    <div className="flex items-center justify-between mb-4 relative z-10">
      <h3 className="text-gray-400 font-medium text-sm">{title}</h3>
      <div className={`p-2 rounded-lg ${colorClass.replace('bg-', 'bg-').replace('500', '500/20')} text-${colorClass.split('-')[1]}-400`}>
        <Icon size={20} />
      </div>
    </div>
    <div className="text-3xl font-bold text-white relative z-10">{value}</div>
  </div>
);

export const Dashboard = () => {
  return (
    <div className="p-8 max-w-7xl mx-auto min-h-screen bg-[#121216] text-white font-sans">
      <div className="mb-8">
        <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-emerald-400 bg-clip-text text-transparent">Olimpiada Boshqaruvi</h1>
        <p className="text-gray-400 mt-2">Hush kelibsiz, asosiy ko'rsatkichlar bilan tanishing.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatCard title="Jami Ishtirokchilar" value="1,245" icon={Users} colorClass="bg-blue-500" />
        <StatCard title="Tasdiqlanganlar" value="840" icon={CheckCircle} colorClass="bg-emerald-500" />
        <StatCard title="Kutayotganlar" value="312" icon={Clock} colorClass="bg-amber-500" />
        <StatCard title="Kassa (Tasdiqlangan)" value="159.6M so'm" icon={CreditCard} colorClass="bg-purple-500" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 bg-[#1e1e24] p-6 rounded-2xl border border-white/5 shadow-lg">
          <h2 className="text-xl font-semibold mb-6 flex items-center gap-2"><div className="w-2 h-6 bg-blue-500 rounded-full"></div>So'nggi Arizalar</h2>
          
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-white/10 text-gray-400 text-sm">
                  <th className="pb-4 font-medium">F.I.SH</th>
                  <th className="pb-4 font-medium">Sinf / Fan</th>
                  <th className="pb-4 font-medium">To'lov</th>
                  <th className="pb-4 font-medium">Holat</th>
                  <th className="pb-4 font-medium">Harakat</th>
                </tr>
              </thead>
              <tbody className="text-sm">
                {[
                  { name: "Aliyev Vali", grade: 9, subject: "Matematika", payment: "Click", status: "Kutilmoqda", color: "amber" },
                  { name: "Azizov Sardor", grade: 11, subject: "Fizika", payment: "Payme", status: "Tasdiqlangan", color: "emerald" },
                  { name: "Sohibova Malika", grade: 8, subject: "Ingliz tili", payment: "Naqd", status: "Kutilmoqda", color: "amber" },
                ].map((item, idx) => (
                  <tr key={idx} className="border-b border-white/5 hover:bg-white/5 transition-colors">
                    <td className="py-4 font-medium">{item.name}</td>
                    <td className="py-4 text-gray-400">{item.grade}-sinf, {item.subject}</td>
                    <td className="py-4">
                      <span className="px-3 py-1 bg-white/10 rounded-full text-xs font-medium border border-white/10">{item.payment}</span>
                    </td>
                    <td className="py-4">
                      <div className="flex items-center gap-2">
                        <div className={`w-2 h-2 rounded-full bg-${item.color}-500`}></div>
                        <span className={`text-${item.color}-400`}>{item.status}</span>
                      </div>
                    </td>
                    <td className="py-4">
                      <button className="text-blue-400 hover:text-blue-300 transition-colors text-sm font-medium">Ko'rish</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="bg-[#1e1e24] p-6 rounded-2xl border border-white/5 shadow-lg">
          <h2 className="text-xl font-semibold mb-6 flex items-center gap-2"><div className="w-2 h-6 bg-purple-500 rounded-full"></div>Tezkor Harakatlar</h2>
          <div className="space-y-4">
            <button className="w-full flex items-center justify-between p-4 rounded-xl bg-gradient-to-r from-blue-500/10 to-blue-500/5 border border-blue-500/20 hover:border-blue-500/40 transition-all text-blue-400 group">
              <span className="font-medium">Yangi test qo'shish</span>
              <div className="bg-blue-500/20 p-2 rounded-lg group-hover:scale-110 transition-transform">
                <Users size={16} />
              </div>
            </button>
            <button className="w-full flex items-center justify-between p-4 rounded-xl bg-gradient-to-r from-emerald-500/10 to-emerald-500/5 border border-emerald-500/20 hover:border-emerald-500/40 transition-all text-emerald-400 group">
              <span className="font-medium">Monitorlarni ochish</span>
              <div className="bg-emerald-500/20 p-2 rounded-lg group-hover:scale-110 transition-transform">
                <Clock size={16} />
              </div>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
