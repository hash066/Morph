import { useEffect, useRef, useState } from 'react'
import { reduced } from './hooks'

type Mode = 'base' | 'morph'
const BASE = { x: 90, y: 238 }, L1 = 170, L2 = 150, CYCLE = 5.4

const ease = (k: number) => (k < 0.5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2)
const lerp = (a: number, b: number, k: number) => a + (b - a) * k

/** Illustrative two-link arm. Baseline overshoots onto the rack; Morph seats the vial in the slot. */
export function ArmViewport() {
  const [mode, setMode] = useState<Mode>('morph')
  const svg = useRef<SVGSVGElement>(null)
  const read = useRef<HTMLDivElement>(null)
  const [flag, setFlag] = useState<string | null>(null)

  useEffect(() => {
    const s = svg.current, r = read.current
    if (!s || !r) return
    const q = (id: string) => s.querySelector<SVGElement>('#' + id)!
    const set = (el: SVGElement, a: Record<string, number | string>) => Object.entries(a).forEach(([k, v]) => el.setAttribute(k, String(v)))
    const base = mode === 'base', tx = base ? 392 : 361, ty = base ? 190 : 222, hi = 128
    let t0 = performance.now(), raf = 0, flagged = false
    setFlag(null)

    const draw = (T: number) => {
      let x: number, y: number
      if (T < 1.4) { const k = ease(T / 1.4); x = lerp(168, tx, k); y = lerp(140, hi, k) }
      else if (T < 2.3) { x = tx; y = lerp(hi, ty, ease((T - 1.4) / 0.9)) }
      else { x = tx; y = ty }
      const dx = x - BASE.x, dy = y - BASE.y, d = Math.hypot(dx, dy)
      const a1 = Math.atan2(dy, dx) - Math.acos(Math.min(1, (d * d + L1 * L1 - L2 * L2) / (2 * d * L1)))
      const ex = BASE.x + L1 * Math.cos(a1), ey = BASE.y + L1 * Math.sin(a1)
      const a2 = Math.atan2(y - ey, x - ex)
      let vx = x, vy = y, rot = 0
      if (base && T >= 2.3) { const k = Math.min(1, (T - 2.3) / 0.8); vx = x + k * 48; vy = y + k * k * 72; rot = k * 84 }
      set(q('l1'), { x1: BASE.x, y1: BASE.y, x2: ex, y2: ey })
      set(q('l2'), { x1: ex, y1: ey, x2: x, y2: y })
      set(q('j1'), { cx: ex, cy: ey })
      set(q('guide'), { x1: tx, y1: hi, x2: tx, y2: ty })
      q('vial').setAttribute('transform', `translate(${vx} ${vy}) rotate(${rot} 0 17)`)
      q('rackR').setAttribute('fill', base && T >= 2.1 && T < 3.6 ? 'url(#hazard)' : 'var(--paper)')
      r.querySelector('[data-k=x]')!.textContent = x.toFixed(1)
      r.querySelector('[data-k=y]')!.textContent = (262 - y).toFixed(1)
      r.querySelector('[data-k=q]')!.textContent = `${Math.round(-a1 * 180 / Math.PI)}° / ${Math.round((a2 - a1) * 180 / Math.PI)}°`
      r.querySelector('[data-k=t]')!.textContent = `${Math.min(T, 5).toFixed(2)} s`
      if (T > 2.5 && !flagged) { flagged = true; setFlag(base ? 'Unsafe rack contact' : 'Placed in slot') }
    }

    if (reduced()) { draw(3); return }
    const tick = (now: number) => {
      let T = (now - t0) / 1000
      if (T > CYCLE) { t0 = now; T = 0; flagged = false; setFlag(null) }
      draw(T)
      raf = requestAnimationFrame(tick)
    }
    raf = requestAnimationFrame(tick)
    return () => cancelAnimationFrame(raf)
  }, [mode])

  return (
    <div className="vp">
      <div className="vp-h">
        <span className="mono">Viewport · illustrative</span>
        <div className="tog mono" role="group" aria-label="Controller">
          {(['base', 'morph'] as Mode[]).map(m => (
            <button key={m} aria-pressed={mode === m} onClick={() => setMode(m)}>{m === 'base' ? 'Baseline' : 'Morph'}</button>
          ))}
        </div>
      </div>
      <div className="vp-stage">
        <svg ref={svg} viewBox="0 0 480 290" role="img" aria-label="Robot arm placing a vial into a rack. Baseline collides with the rack; Morph places the vial in the slot.">
          <defs>
            <pattern id="hazard" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
              <rect width="8" height="8" fill="var(--signal)" /><rect width="3.5" height="8" fill="var(--ink)" />
            </pattern>
          </defs>
          <line x1="0" y1="262" x2="480" y2="262" stroke="var(--ink)" />
          <rect x="62" y="238" width="56" height="24" fill="var(--ink)" />
          <rect x="314" y="226" width="32" height="36" fill="var(--paper)" stroke="var(--ink)" strokeWidth="1.5" />
          <rect id="rackR" x="376" y="226" width="32" height="36" fill="var(--paper)" stroke="var(--ink)" strokeWidth="1.5" />
          <line x1="361" y1="270" x2="361" y2="280" stroke="var(--ink)" />
          <text x="361" y="288" textAnchor="middle" className="svg-cap">SLOT</text>
          <line id="guide" stroke="var(--ink-30)" strokeDasharray="3 4" />
          <line id="l1" stroke="var(--ink)" strokeWidth="12" strokeLinecap="square" />
          <line id="l2" stroke="var(--ink)" strokeWidth="8" strokeLinecap="square" />
          <circle cx={BASE.x} cy={BASE.y} r="8" fill="var(--paper)" stroke="var(--ink)" strokeWidth="3" />
          <circle id="j1" r="6" fill="var(--paper)" stroke="var(--ink)" strokeWidth="3" />
          <g id="vial">
            <rect x="-9" y="0" width="18" height="34" fill="var(--signal)" stroke="var(--ink)" strokeWidth="1.5" />
            <rect x="-9" y="0" width="18" height="7" fill="var(--ink)" />
          </g>
        </svg>
        <div className={`flag mono ${flag ? 'show' : ''} ${mode === 'base' ? 'bad' : ''}`} aria-live="polite">{flag}</div>
      </div>
      <div className="vp-f mono" ref={read}>
        <div className="m50">EE x<b data-k="x">0.0</b></div>
        <div className="m50">EE y<b data-k="y">0.0</b></div>
        <div className="m50">q1 / q2<b data-k="q">0° / 0°</b></div>
        <div className="m50">t<b data-k="t">0.00 s</b></div>
      </div>
    </div>
  )
}
