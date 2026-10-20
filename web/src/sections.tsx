import { useEffect, useMemo, useRef, useState } from 'react'
import { ArmViewport } from './ArmViewport'
import { Audit, Episode, Evidence, Report, Run, cancelRun, loadRuns, meanCompletion } from './api'
import { reduced, useCountUp, useInView } from './hooks'

const pct = (r: Report) => Math.round(r.paired_gain * 100)
const ci = (r: Report) => r.paired_gain_interval95.map(v => v.toFixed(2)).join(' to ')

function Count({ to, d = 0 }: { to: number; d?: number }) {
  const [ref, v] = useCountUp(to, d)
  return <span ref={ref}>{v}</span>
}

function SectionHead({ n, title, lede }: { n: string; title: React.ReactNode; lede?: string }) {
  return (
    <div className="sh">
      <div className="mono m50 n">{n}</div>
      <div><h2>{title}</h2>{lede && <p className="lede">{lede}</p>}</div>
    </div>
  )
}

/* 01 ─ failure */
export function Failure({ ev, onReplay }: { ev: Evidence; onReplay: () => void }) {
  const { fault, morph, random } = ev.audits
  const r = ev.summary.morph_report
  const tMorph = meanCompletion(morph), tRandom = meanCompletion(random)
  const spend = ev.context.planner_usage
  return (
    <section id="failure" className="first">
      <div className="hero">
        <div>
          <div className="mono m50">SO-101 vial placement &nbsp;/&nbsp; fault actuator150 &nbsp;/&nbsp; gain ×1.5</div>
          <h1>The arm started missing the rack. Morph found a fix and <mark>checked it on {r.denominator} new starts.</mark></h1>
          <div className="score">
            <div><div className="v dim"><Count to={fault.summary.successes} /><small>/{fault.summary.episodes}</small></div><label className="mono m50">Before</label></div>
            <div className="arrow" aria-hidden="true">→</div>
            <div><div className="v"><Count to={morph.summary.successes} /><small>/{morph.summary.episodes}</small></div><label className="mono m50">After</label></div>
          </div>
          <div className="actions">
            <button className="btn" onClick={onReplay}>Replay investigation <span aria-hidden="true">→</span></button>
            <a className="tl" href="#evidence">Read the evidence</a>
          </div>
        </div>
        <ArmViewport />
      </div>
      <div className="strip">
        <div><span className="mono m50">Paired gain</span><strong>+<Count to={pct(r)} /> pp</strong><p>95% interval {ci(r)}</p></div>
        <div><span className="mono m50">Unsafe contacts</span><strong><Count to={fault.summary.unsafe_rack_contacts} /> → <Count to={morph.summary.unsafe_rack_contacts} /></strong><p>Rack collisions, baseline to Morph</p></div>
        <div><span className="mono m50">Mean completion</span><strong>{tMorph != null ? <><Count to={tMorph} d={2} /> s</> : '—'}</strong><p>{tRandom != null ? `Random search took ${tRandom.toFixed(2)} s` : 'Successful episodes only'}</p></div>
        <div><span className="mono m50">Planner spend</span><strong>{spend ? <>$<Count to={spend.measured_total_cost_usd} d={4} /></> : '—'}</strong><p>{spend ? `${spend.attempts} Nemotron calls in total` : 'No usage record'}</p></div>
      </div>
    </section>
  )
}

/* 02 ─ investigation */
type Line = [string, string]
function buildLog(ev: Evidence): { lines: Line[]; stepAt: number[] } {
  const p = ev.context.planner, { morph, random } = ev.audits, s = ev.summary
  const devFault = p?.observations.find(o => o.candidate_id === 'fault_baseline')
  const lines: Line[] = [
    ['load', 'frozen protocol, evaluator and checkpoint hashes match'],
    ['fault', devFault ? `actuator150 reproduced, development ${devFault.successes}/${devFault.episodes}` : 'actuator150 reproduced'],
    ['plan', p ? p.model : 'planner record missing'],
    ['plan', p ? `candidate ${p.proposal.candidate_id} accepted by validator` : 'no candidate'],
    ['confirm', `morph ${morph.summary.successes}/${morph.summary.episodes}, unsafe ${morph.summary.unsafe_rack_contacts}`],
    ['confirm', `random comparator ${random.summary.successes}/${random.summary.episodes}, unsafe ${random.summary.unsafe_rack_contacts}`],
    ['decide', `${s.morph_report.decision}, CI [${s.morph_report.paired_gain_interval95.map(v => v.toFixed(3)).join(', ')}]`],
    ['pack', `bundle ${s.bundle_bytes} B, sha256 ${s.bundle_sha256.slice(0, 8)}…`],
  ]
  return { lines, stepAt: [0, 2, 4, 5, 7] }
}

export function Investigation({ ev, replayKey }: { ev: Evidence; replayKey: number }) {
  const { lines, stepAt } = useMemo(() => buildLog(ev), [ev])
  const [shown, setShown] = useState(lines.length)
  const timer = useRef<number | undefined>(undefined)
  const p = ev.context.planner

  useEffect(() => {
    if (!replayKey) return
    if (reduced()) { setShown(lines.length); return }
    setShown(0)
    let i = 0
    const next = () => { i++; setShown(i); if (i < lines.length) timer.current = window.setTimeout(next, 520) }
    timer.current = window.setTimeout(next, 300)
    return () => clearTimeout(timer.current)
  }, [replayKey, lines.length])

  const done = shown >= lines.length
  const current = done ? -1 : stepAt.reduce((acc, a, k) => (shown - 1 >= a ? k : acc), 0)
  const steps: [string, string][] = [
    ['Reproduce the fault', 'Gain drift broke a policy that passed 8/8 nominally.'],
    ['Ask Nemotron', p ? `It chose ${p.proposal.candidate_id} from ${p.candidate_registry.length} allowed candidates.` : 'Planner record unavailable.'],
    ['Confirm on unseen starts', `Frozen first, then run on ${ev.summary.morph_report.denominator} new starts.`],
    ['Compare with random search', 'Same budget, same starts, a fixed random candidate.'],
    ['Package the evidence', 'Manifests, episodes and checksums in one ZIP.'],
  ]
  const state = (k: number) => (done || k < current ? 'Done' : k === current ? 'Running' : 'Queued')

  return (
    <section id="investigation">
      <SectionHead n="02" title="How the investigation ran" lede="The planner only saw development starts. It picked from a fixed list, and the validator rejected anything else." />
      <div className="two">
        <div>
          <ol className="steps">
            {steps.map(([t, d], k) => (
              <li key={t} className={k === current ? 'run' : ''}>
                <span className="mono m50">{String.fromCharCode(65 + k)}</span>
                <div><b>{t}</b><p>{d}</p></div>
                <span className="mono m50 s">{state(k)}</span>
              </li>
            ))}
          </ol>
          {p && (
            <figure className="why">
              <figcaption className="mono m50">Nemotron's recorded reason</figcaption>
              <blockquote>{p.proposal.reason}</blockquote>
            </figure>
          )}
        </div>
        <div className="log" aria-live="polite">
          {lines.map(([k, t], i) => (
            <div key={i} className={`ln ${i < shown ? 'in' : ''}`}>
              <span className="d">{String(i + 1).padStart(2, '0')}</span>{'  '}<span className="k">{k.padEnd(7, ' ')}</span> {t}
            </div>
          ))}
          <div className="ln in"><span className="cur" /></div>
        </div>
      </div>
    </section>
  )
}

/* 03 ─ comparison */
const cellKind = (e: Episode) => (e.unsafe_rack_contact ? 'u' : e.success ? '' : 'o')
const outcome = (e: Episode) =>
  `${e.success ? 'Success' : e.timed_out ? 'Timed out' : 'Failed'}${e.unsafe_rack_contact ? ', unsafe rack contact' : ''}`

type Pick = { method: string; e: Episode }

function Matrix({ rows, pick, setPick }: { rows: [string, string, Audit][]; pick: Pick | null; setPick: (p: Pick) => void }) {
  return (
    <div className="matrix">
      {rows.map(([name, sub, a]) => (
        <div className="mr" key={name}>
          <div><b>{name}</b><span className="mono m50">{sub}</span></div>
          <div className="cells">
            {[...a.episodes].sort((x, y) => x.reset_row - y.reset_row).map((e, i) => (
              <button
                key={e.reset_row}
                className={`${cellKind(e)} ${pick?.method === name && pick.e.reset_row === e.reset_row ? 'sel' : ''}`}
                style={{ animationDelay: `${i * 12}ms` }}
                aria-label={`${name}, start ${e.reset_row}: ${outcome(e)}`}
                onClick={() => setPick({ method: name, e })}
              />
            ))}
          </div>
          <div className="tot">{a.summary.successes}</div>
        </div>
      ))}
    </div>
  )
}

function Inspector({ pick }: { pick: Pick | null }) {
  if (!pick) return <div className="insp mono m50">Select any bar to read that start's evaluator record.</div>
  const { e, method } = pick
  return (
    <div className="insp">
      <div className="mono m50">{method} · start {e.reset_row}</div>
      <dl>
        <div><dt className="mono m50">Outcome</dt><dd>{outcome(e)}</dd></div>
        <div><dt className="mono m50">Completion</dt><dd>{e.completion_seconds != null && e.success ? `${e.completion_seconds.toFixed(2)} s` : '—'}</dd></div>
        <div><dt className="mono m50">Peak rack force</dt><dd>{e.peak_rack_force_n != null ? `${e.peak_rack_force_n.toFixed(1)} N` : '—'}</dd></div>
      </dl>
    </div>
  )
}

function IntervalChart({ rows }: { rows: { n: string; r: Report; dashed?: boolean }[] }) {
  const x0 = 190, w = 430, min = -0.6, max = 1
  const X = (v: number) => x0 + ((v - min) / (max - min)) * w
  return (
    <svg className="cichart" viewBox="0 0 640 180" role="img"
      aria-label={rows.map(({ n, r }) => `${n}: ${r.paired_gain.toFixed(2)}, interval ${ci(r)}`).join('. ')}>
      <defs>
        <pattern id="hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="1" height="6" fill="var(--ink-12)" /></pattern>
      </defs>
      <rect x={X(min)} y="16" width={X(0) - X(min)} height="112" fill="url(#hatch)" />
      {[-0.5, 0, 0.5, 1].map(t => (
        <g key={t}>
          <line x1={X(t)} x2={X(t)} y1="16" y2="128" stroke={t === 0 ? 'var(--ink)' : 'var(--ink-12)'} />
          <text x={X(t)} y="148" textAnchor="middle">{(t > 0 ? '+' : '') + t.toFixed(1)}</text>
        </g>
      ))}
      <text x={X(-0.3)} y="170" textAnchor="middle">no effect</text>
      <text x={X(0.5)} y="170" textAnchor="middle">gain</text>
      {rows.map(({ n, r, dashed }, i) => {
        const y = 52 + i * 44, [lo, hi] = r.paired_gain_interval95, len = X(hi) - X(lo)
        return (
          <g key={n}>
            <text className="lbl" x="0" y={y + 5}>{n}</text>
            <line className="bar" style={{ ['--len' as string]: len }} x1={X(lo)} x2={X(hi)} y1={y} y2={y} stroke="var(--ink)" strokeWidth={dashed ? 2 : 4} />
            <line x1={X(lo)} x2={X(lo)} y1={y - 7} y2={y + 7} stroke="var(--ink)" strokeWidth="2" />
            <line x1={X(hi)} x2={X(hi)} y1={y - 7} y2={y + 7} stroke="var(--ink)" strokeWidth="2" />
            <rect x={X(r.paired_gain) - 7} y={y - 7} width="14" height="14" fill={dashed ? 'var(--paper)' : 'var(--signal)'} stroke="var(--ink)" strokeWidth="2" />
          </g>
        )
      })}
    </svg>
  )
}

export function Comparison({ ev }: { ev: Evidence }) {
  const [ref, go] = useInView<HTMLElement>(0.15)
  const [pick, setPick] = useState<Pick | null>(null)
  const { fault, morph, random } = ev.audits
  const reg = ev.context.planner?.candidate_registry ?? []
  const chosen = reg.find(c => c.candidate_id === ev.context.planner?.proposal.candidate_id)
  const rows: [string, string, Audit][] = [
    ['Fault baseline', 'unchanged', fault],
    ['Morph + Nemotron', chosen ? chosen.candidate_id : 'selected', morph],
    ['Matched random', 'arm67_jaw80', random],
  ]
  const table: [string, string, Audit, string, boolean][] = [
    ['Fault baseline', 'Unchanged controller', fault, 'Failed', false],
    ['Morph + Nemotron', chosen ? `Arm ${chosen.arm_scale_multiplier.toFixed(2)}, jaw ${chosen.jaw_scale_multiplier.toFixed(2)}` : 'Selected candidate', morph, 'Selected', true],
    ['Matched random', 'Arm 0.67, jaw 0.80', random, 'Comparator', false],
  ]
  const ciRows = [
    ...(ev.context.pilot ? [{ n: `Pilot, ${ev.context.pilot.morph_report.denominator} starts`, r: ev.context.pilot.morph_report, dashed: true }] : []),
    { n: `Confirmation, ${ev.summary.morph_report.denominator}`, r: ev.summary.morph_report },
  ]
  return (
    <section id="comparison" ref={ref} className={go ? 'go' : ''}>
      <SectionHead n="03" title={`Three controllers, ${fault.summary.episodes} starts each`}
        lede="Random search with the same budget matched Morph on success and was safer. Morph was faster. The claim is recovery, not that the model beats simple search." />
      <Matrix rows={rows} pick={pick} setPick={setPick} />
      <div className="under">
        <div className="key mono m50">
          <span><i />Success</span><span><i className="u" />Unsafe contact</span><span><i className="o" />Timed out</span><span>Ordered by start index</span>
        </div>
        <Inspector pick={pick} />
      </div>

      <div className="tblw">
        <table>
          <thead><tr className="mono m50"><th>Method</th><th>Success</th><th>Unsafe</th><th>Timeouts</th><th>Mean time</th><th>Decision</th></tr></thead>
          <tbody>
            {table.map(([n, sub, a, d, sel]) => {
              const t = meanCompletion(a)
              return (
                <tr key={n} className={sel ? 'pick' : ''}>
                  <td><b>{n}</b><span className="sub">{sub}</span></td>
                  <td className="num">{a.summary.successes} / {a.summary.episodes}</td>
                  <td className="num">{a.summary.unsafe_rack_contacts}</td>
                  <td className="num">{a.summary.timeouts}</td>
                  <td className="num">{t != null ? `${t.toFixed(2)} s` : '—'}</td>
                  <td className="mono">{d}</td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>

      <div className="ci">
        <IntervalChart rows={ciRows} />
        <div>
          <div className="mono m50">Is the gain real?</div>
          <p>{ev.context.pilot ? `The ${ev.context.pilot.morph_report.denominator}-start pilot crossed zero, so it proved nothing. ` : ''}The preregistered {ev.summary.morph_report.denominator}-start confirmation stayed clear of it.</p>
        </div>
      </div>
    </section>
  )
}

/* 04 ─ evidence */
export function EvidenceSection({ ev }: { ev: Evidence }) {
  const s = ev.summary
  const [copied, setCopied] = useState(false)
  const hashRef = useRef<HTMLDivElement>(null)
  const copy = () => {
    const select = () => { const r = document.createRange(); r.selectNodeContents(hashRef.current!); const g = getSelection(); g?.removeAllRanges(); g?.addRange(r) }
    navigator.clipboard?.writeText(s.bundle_sha256).then(() => { setCopied(true); setTimeout(() => setCopied(false), 1500) }, select) ?? select()
  }
  return (
    <section id="evidence">
      <div className="sh">
        <div className="mono m50 n">04</div>
        <div>
          <div className="mono m50" style={{ marginBottom: 12 }}>Recorded decision</div>
          <div className="decision"><span>{s.morph_report.decision}</span></div>
          <p className="lede">{s.morph_report.reason}</p>
        </div>
      </div>
      <div className="ev">
        <div>
          <div className="mono m50">Confirmation bundle v1 · {s.bundle_bytes.toLocaleString()} bytes</div>
          <div className="hash" ref={hashRef}>{s.bundle_sha256}</div>
          <div className="actions">
            <a className="btn" href="/api/v1/evidence/bundle" download>Download bundle</a>
            <button className="tl" onClick={copy}>{copied ? 'Copied' : 'Copy SHA-256'}</button>
          </div>
        </div>
        <div><div className="mono m50">Established</div><ul><li>Recovery in the pinned Isaac Lab simulation</li><li>Disjoint development and held-out starts</li><li>Real Nemotron calls, spend recorded</li></ul></div>
        <div className="no"><div className="mono m50">Not established</div><ul><li>Behaviour on a real arm</li><li>Nemotron beating random search</li><li>Other faults, robots or users</li></ul></div>
      </div>
    </section>
  )
}

/* 05 ─ runs */
export function Runs({ token, setToken }: { token: string; setToken: (t: string) => void }) {
  const [runs, setRuns] = useState<Run[] | null>(null)
  const [err, setErr] = useState('')
  const [draft, setDraft] = useState('')
  const refresh = () => {
    if (!token) return
    loadRuns(token).then(r => { setRuns(r); setErr('') }).catch(e => { setErr(e.message); if (String(e.message).includes('rejected')) setToken('') })
  }
  useEffect(refresh, [token])
  const cancel = (id: string) => cancelRun(token, id).then(refresh).catch(e => setErr(e.message))

  return (
    <section id="runs">
      <SectionHead n="05" title="Run queue" lede="Evidence above is public. Viewing and cancelling queued jobs needs the local operator token. Robot motion is not available from this screen." />
      {!token ? (
        <form className="tok" onSubmit={e => { e.preventDefault(); if (draft.length >= 32) setToken(draft) }}>
          <label htmlFor="token" className="mono m50">Operator token</label>
          <div className="tok-row">
            <input id="token" type="password" autoComplete="off" spellCheck={false} value={draft} onChange={e => setDraft(e.target.value)} placeholder="Paste MORPH_API_TOKEN" />
            <button className="btn" disabled={draft.length < 32}>Connect</button>
          </div>
          <span className="mono m50">{draft && draft.length < 32 ? `${32 - draft.length} more characters needed` : 'Kept in this browser session only'}</span>
        </form>
      ) : (
        <div className="queue">
          <div className="queue-h mono m50"><span>{runs ? `${runs.length} job${runs.length === 1 ? '' : 's'}` : 'Loading'}</span><span className="row"><button className="tl" onClick={refresh}>Refresh</button><button className="tl" onClick={() => setToken('')}>Disconnect</button></span></div>
          {err && <p className="err">{err}</p>}
          {runs && runs.length === 0 && <p className="lede">No jobs yet. Submit a bounded development manifest through the API, then run <code>uv run python -m morph worker-once</code>.</p>}
          {runs?.map(r => (
            <div className="job" key={r.id}>
              <span className={`st ${r.state}`} />
              <code>{r.id.slice(0, 12)}</code>
              <span className="mono">{r.state}</span>
              <span className="m50">{r.error ?? ''}</span>
              {r.state === 'queued' && <button className="tl" onClick={() => cancel(r.id)}>Cancel</button>}
            </div>
          ))}
        </div>
      )}
    </section>
  )
}
