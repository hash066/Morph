import { useEffect, useRef, useState } from 'react'

const reduced = () => typeof matchMedia !== 'undefined' && matchMedia('(prefers-reduced-motion: reduce)').matches

/** Becomes true once the element has scrolled into view, then stays true. */
export function useInView<T extends Element>(threshold = 0.25) {
  const ref = useRef<T>(null)
  const [seen, setSeen] = useState(false)
  useEffect(() => {
    const el = ref.current
    if (!el || seen) return
    const io = new IntersectionObserver(([e]) => { if (e.isIntersecting) { setSeen(true); io.disconnect() } }, { threshold })
    io.observe(el)
    return () => io.disconnect()
  }, [seen, threshold])
  return [ref, seen] as const
}

/** Counts from 0 to target when visible; shows the final value at rest and under reduced motion. */
export function useCountUp(target: number, decimals = 0) {
  const [ref, seen] = useInView<HTMLSpanElement>(0.6)
  const [value, setValue] = useState(target)
  useEffect(() => {
    if (!seen || reduced()) { setValue(target); return }
    let raf = 0
    const t0 = performance.now()
    const tick = (now: number) => {
      const k = Math.min(1, (now - t0) / 1000)
      setValue(target * (1 - Math.pow(1 - k, 4)))
      if (k < 1) raf = requestAnimationFrame(tick)
    }
    raf = requestAnimationFrame(tick)
    return () => cancelAnimationFrame(raf)
  }, [seen, target])
  return [ref, value.toFixed(decimals)] as const
}

/** Tracks which section id is in the middle band of the viewport. */
export function useScrollSpy(ids: string[], ready: boolean) {
  const [active, setActive] = useState(ids[0])
  useEffect(() => {
    const io = new IntersectionObserver(
      es => es.forEach(e => e.isIntersecting && setActive(e.target.id)),
      { rootMargin: '-45% 0px -50% 0px' },
    )
    ids.forEach(id => { const el = document.getElementById(id); if (el) io.observe(el) })
    return () => io.disconnect()
  }, [ids.join(), ready])
  return active
}

export { reduced }
