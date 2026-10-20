export type Episode = {
  reset_row: number
  success: boolean
  timed_out: boolean
  unsafe_rack_contact: boolean
  completion_seconds: number | null
  peak_rack_force_n?: number
}
export type Audit = {
  summary: { episodes: number; successes: number; timeouts: number; unsafe_rack_contacts: number }
  episodes: Episode[]
}
export type Report = {
  denominator: number
  baseline_successes: number
  candidate_successes: number
  paired_gain: number
  paired_gain_interval95: [number, number]
  decision: string
  reason: string
}
export type Summary = { morph_report: Report; random_report: Report; bundle_sha256: string; bundle_bytes: number }
export type Context = {
  planner: {
    model: string
    observations: { candidate_id: string; successes: number; episodes: number; unsafe: number }[]
    proposal: { candidate_id: string; reason: string; hypotheses: string[]; decision: string }
    candidate_registry: { candidate_id: string; arm_scale_multiplier: number; jaw_scale_multiplier: number }[]
  } | null
  planner_usage: { measured_total_cost_usd: number; attempts: number; validated_attempts: number } | null
  pilot: { morph_report: Report } | null
}
export type Status = { mode: string; simulation_gate: string; hardware: string; provider: string }
export type Run = { id: string; state: string; error?: string | null }
export type Evidence = { status: Status; summary: Summary; context: Context; audits: Record<'fault' | 'morph' | 'random', Audit> }

const json = (r: Response) => {
  if (!r.ok) throw Error(r.status === 401 ? 'Operator token rejected' : `Request failed (${r.status})`)
  return r.json()
}
const get = (path: string, token?: string) =>
  fetch(path, token ? { headers: { Authorization: `Bearer ${token}` } } : undefined).then(json)

export async function loadEvidence(): Promise<Evidence> {
  const [status, summary, context, fault, morph, random] = await Promise.all([
    get('/api/v1/status'),
    get('/api/v1/evidence/summary'),
    get('/api/v1/evidence/context'),
    get('/api/v1/evidence/audits/fault'),
    get('/api/v1/evidence/audits/morph'),
    get('/api/v1/evidence/audits/random'),
  ])
  return { status, summary, context, audits: { fault, morph, random } }
}

export const loadRuns = (token: string): Promise<Run[]> => get('/api/v1/runs', token).then(r => r.data)

export const cancelRun = (token: string, id: string) =>
  fetch(`/api/v1/runs/${id}/cancel`, { method: 'POST', headers: { Authorization: `Bearer ${token}` } }).then(json)

export const meanCompletion = (a: Audit) => {
  const done = a.episodes.filter(e => e.success && e.completion_seconds != null)
  return done.length ? done.reduce((s, e) => s + (e.completion_seconds ?? 0), 0) / done.length : null
}
