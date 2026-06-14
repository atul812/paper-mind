import axios from 'axios'

const apiClient = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 60000,
  headers: {
    'Content-Type': 'application/json',
  },
})

export async function runPipeline(query) {
  const response = await apiClient.post('/api/pipeline', { query })
  const payload = response.data

  if (!payload) {
    throw new Error('Empty response from backend')
  }

  if (payload.error) {
    throw new Error(payload.error)
  }

  if (payload.data) {
    return payload.data
  }

  return payload
}
