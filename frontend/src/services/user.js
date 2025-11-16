// ---------- GET ALL USERS (TEMP) ----------

export async function fetchUsers() {
  const res = await fetch('/api/accounts/users/')
  if (!res.ok) throw new Error(`HTTP ${res.status}`)
  return res.json() 
}