export const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

// Fetch wrapper for admin pages: attaches the JWT and redirects to /login
// when the token is missing/expired (backend now requires auth on admin APIs).
export async function authFetch(path, options = {}) {
  const token = localStorage.getItem('access_token');
  const headers = { ...(options.headers || {}) };
  if (token) headers['Authorization'] = `Bearer ${token}`;

  const res = await fetch(`${API_BASE}${path}`, { ...options, headers });

  if (res.status === 401) {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    window.location.href = '/login';
  }
  return res;
}
