import axios from 'axios'

const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'

const api = axios.create({
  baseURL,
  timeout: 15000,
})

export type StrategyItem = {
  strategyid: string
  content: any
}

export async function listStrategies(): Promise<{ items: StrategyItem[] }> {
  const res = await api.get('/api/strategies')
  return res.data
}

export async function getStrategy(strategyid: string): Promise<StrategyItem> {
  const res = await api.get(`/api/strategies/${encodeURIComponent(strategyid)}`)
  return res.data
}

export async function createStrategy(req: { strategyid: string; content: any }): Promise<StrategyItem> {
  const res = await api.post('/api/strategies', req)
  return res.data
}

export async function updateStrategy(
  strategyid: string,
  req: { strategyid: string; content: any },
): Promise<StrategyItem> {
  const res = await api.put(`/api/strategies/${encodeURIComponent(strategyid)}`, req)
  return res.data
}

export async function deleteStrategy(strategyid: string): Promise<void> {
  await api.delete(`/api/strategies/${encodeURIComponent(strategyid)}`)
}

