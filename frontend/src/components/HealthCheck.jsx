import { useEffect, useState } from 'react'
import { fetchHello } from '../services/health.js'

export default function HealthCheck() {
  const [status, setStatus] = useState('Loading...')
  const [error, setError] = useState('')

  useEffect(() => {
    fetchHello()
      .then(text => setStatus(text)) // should be "hello world"
      .catch(err => setError(err.message))
  }, [])

  if (error) return <div>Error: {error}</div>
  return <div>API Health: {status}</div>
}
