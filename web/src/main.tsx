import { useEffect, useState } from 'react'
import { createRoot } from 'react-dom/client'
import { Evidence, loadEvidence } from './api'
import { useScrollSpy } from './hooks'
import { Comparison, EvidenceSection, Failure, Investigation, Runs } from './sections'
import './styles.css'

const SECTIONS: [string, string][] = [
  ['failure', '01 Failure'], ['investigation', '02 Investigation'], ['comparison', '03 Comparison'], ['evidence', '04 Evidence'], ['runs', '05 Runs'],
]

function TopBar({ ev }: { ev: Evidence | null }) {
  const active = useScrollSpy(SECTIONS.map(s => s[0]), !!ev)
  const locked = !ev || ev.status.hardware === 'disabled'
  return (
    <header className="top">
      <div className="w">
        <div className="word">MORPH</div>
        <nav className="links mono" aria-label="Sections">
          {SECTIONS.map(([id, label]) => <a key={id} href={`#${id}`} className={active === id ? 'on' : ''}>{label}</a>)}
        </nav>
        <div className="lock mono"><i /><span>{ev ? ev.status.mode : 'Simulation'} only · {locked ? 'motion locked' : 'motion enabled'}</span></div>
      </div>
    </header>
  )
}

function App() {
  const [ev, setEv] = useState<Evidence | null>(null)
  const [error, setError] = useState('')
  const [replay, setReplay] = useState(0)
  const [token, setTokenState] = useState(() => { try { return sessionStorage.getItem('morph-token') ?? '' } catch { return '' } })
  const setToken = (t: string) => { setTokenState(t); try { t ? sessionStorage.setItem('morph-token', t) : sessionStorage.removeItem('morph-token') } catch { /* storage blocked */ } }
  const load = () => { setError(''); loadEvidence().then(setEv).catch(e => setError(e.message)) }
  useEffect(load, [])

  const startReplay = () => {
    document.getElementById('investigation')?.scrollIntoView({ behavior: 'smooth' })
    setReplay(k => k + 1)
  }

  return (
    <>
      <TopBar ev={ev} />
      <main className="w">
        {error ? (
          <div className="state">
            <div className="mono m50">Evidence unavailable</div>
            <h2>{error}</h2>
            <p className="lede">Start the API on port 8091, then try again.</p>
            <button className="btn" onClick={load}>Try again</button>
          </div>
        ) : !ev ? (
          <div className="state" aria-busy="true"><div className="mono m50">Loading recorded evidence</div><div className="loadbar"><i /></div></div>
        ) : (
          <>
            <Failure ev={ev} onReplay={startReplay} />
            <Investigation ev={ev} replayKey={replay} />
            <Comparison ev={ev} />
            <EvidenceSection ev={ev} />
            <Runs token={token} setToken={setToken} />
            <footer className="mono m50">
              <span>Figures served from docs/verification by the local API. Viewport motion is illustrative.</span>
              <span>Planner: {ev.status.provider.replace(/_/g, ' ')}</span>
            </footer>
          </>
        )}
      </main>
    </>
  )
}

createRoot(document.getElementById('root')!).render(<App />)
