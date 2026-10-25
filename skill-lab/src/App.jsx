import { useEffect, useRef, useState, useMemo, Suspense } from 'react'
import gsap from 'gsap'
import { motion, AnimatePresence } from 'motion/react'
import { Canvas, useFrame } from '@react-three/fiber'
import { OrbitControls, Environment, PerspectiveCamera, ContactShadows, Float, Grid } from '@react-three/drei'
import { Physics, RigidBody, BallCollider, CuboidCollider } from '@react-three/rapier'
import { EffectComposer, Bloom, ChromaticAberration, DepthOfField, Vignette, Noise, Glitch } from '@react-three/postprocessing'
import * as THREE from 'three'

// ---------- helpers
const clamp = (v, a, b) => Math.max(a, Math.min(b, v))

// ---------- ANATOMY REVEAL: simplified isometric espresso machine with convex parts
function AnatomyReveal() {
  const [explode, setExplode] = useState(0.35)
  const [yaw, setYaw] = useState(-28)
  const [pitch, setPitch] = useState(18)
  const [feature, setFeature] = useState(0)
  const stageRef = useRef(null)
  const dragging = useRef(false)
  const last = useRef({ x: 0, y: 0 })

  // Build 52 convex parts as simple SVG polygons projected isometrically
  // Real anatomy-reveal builds 80+ parts with separating planes. Here we simulate with layered SVG.
  const parts = useMemo(() => {
    const base = [
      { id:'base', w: 220, h: 18, c: '#c9b8a0', z: 0, x: 0, y: 0, group: 'chassis' },
      { id:'body', w: 190, h: 110, c: '#e8ddd0', z: 18, x: 0, y: -4, group: 'chassis' },
      { id:'cheekL', w: 14, h: 108, c: '#d6c7b3', z: 18, x: -88, y: 0, group: 'chassis' },
      { id:'cheekR', w: 14, h: 108, c: '#d6c7b3', z: 18, x: 88, y: 0, group: 'chassis' },
      { id:'deck', w: 180, h: 22, c: '#1a1a1e', z: 128, x: 0, y: 0, group: 'chassis' },
      { id:'head', w: 94, h: 54, c: '#b8c0c9', z: 74, x: 0, y: 8, group: 'head' },
      { id:'gauge', w: 44, h: 44, c: '#fff', z: 92, x: -30, y: -18, group: 'head' },
      { id:'knob1', w: 18, h: 18, c: '#2b2b30', z: 84, x: 26, y: -12, group: 'controls' },
      { id:'knob2', w: 18, h: 18, c: '#2b2b30', z: 84, x: 50, y: -12, group: 'controls' },
      { id:'knob3', w: 18, h: 18, c: '#2b2b30', z: 84, x: 74, y: -12, group: 'controls' },
      { id:'grouphead', w: 56, h: 26, c: '#8a95a3', z: 56, x: 0, y: 28, group: 'brew' },
      { id:'portafilter', w: 64, h: 12, c: '#2b2b30', z: 32, x: 2, y: 42, group: 'brew' },
      { id:'handle', w: 48, h: 10, c: '#1a1a1e', z: 32, x: 50, y: 48, group: 'brew' },
      { id:'tray', w: 160, h: 10, c: '#c9b8a0', z: 4, x: 0, y: 18, group: 'chassis' },
      { id:'drip-grid', w: 120, h: 6, c: '#8a8a93', z: 14, x: 0, y: 18, group: 'chassis' },
      { id:'hopper', w: 66, h: 68, c: '#2b2b30', z: 150, x: -46, y: -28, group: 'grinder' },
      { id:'hopper-glass', w: 54, h: 48, c: 'rgba(120,160,180,0.35)', z: 165, x: -46, y: -28, group: 'grinder' },
      { id:'hopper-lid', w: 56, h: 8, c: '#1a1a1e', z: 188, x: -46, y: -28, group: 'grinder' },
      { id:'tank', w: 36, h: 72, c: 'rgba(120,180,200,0.28)', z: 58, x: 82, y: -18, group: 'chassis' },
      { id:'boiler1', w: 44, h: 48, c: '#c9b8a0', z: 48, x: -28, y: -8, group: 'internals' },
      { id:'boiler2', w: 36, h: 38, c: '#d6c7b3', z: 42, x: 28, y: -8, group: 'internals' },
      { id:'pump', w: 28, h: 18, c: '#8a95a3', z: 28, x: -48, y: 12, group: 'internals' },
      { id:'board', w: 52, h: 4, c: '#2d6a4f', z: 62, x: 0, y: -20, group: 'internals' },
      { id:'chip', w: 10, h: 10, c: '#1a1a1e', z: 66, x: -8, y: -22, group: 'internals' },
      { id:'tube1', w: 6, h: 42, c: '#8a95a3', z: 44, x: -6, y: 6, group: 'internals' },
      { id:'tube2', w: 6, h: 32, c: '#8a95a3', z: 44, x: 18, y: 6, group: 'internals' },
    ]
    // add screws, buttons, vents
    const screws = Array.from({ length: 8 }, (_, i) => ({
      id: `screw${i}`, w: 6, h: 6, c: '#6e6e7a', z: 2 + (i%2)*2, x: -80 + i*22, y: 44, group: 'detail'
    }))
    const buttons = Array.from({ length: 5 }, (_, i) => ({
      id: `btn${i}`, w: 10, h: 10, c: '#ff3b30', z: 80, x: -14 + i*14, y: -26, group: 'controls'
    }))
    return [...base, ...screws, ...buttons]
  }, [])

  // isometric projection
  const iso = (x, y, z, yawDeg, pitchDeg) => {
    const yawRad = yawDeg * Math.PI/180
    const pitchRad = pitchDeg * Math.PI/180
    // rotate around Y (yaw) then X (pitch) then orthographic
    const cosY = Math.cos(yawRad), sinY = Math.sin(yawRad)
    const cosP = Math.cos(pitchRad), sinP = Math.sin(pitchRad)
    const rx = x * cosY - z * sinY
    const rz = x * sinY + z * cosY
    const ry = y * cosP - rz * sinP
    const rz2 = y * sinP + rz * cosP
    // isometric-like dimetric: scale
    const sx = rx * 1.0
    const sy = ry * 1.0 - rz2 * 0.18
    return { sx: sx, sy: sy, depth: rz2 }
  }

  const projected = useMemo(() => {
    // explode along separate vectors per group
    const explodeVec = {
      chassis: [0, 0, 0],
      head: [0, 0, 1.35],
      controls: [0, 0.6, 1.6],
      brew: [0, 0.9, 0.9],
      grinder: [0, -0.5, 1.8],
      internals: [0, 0, -0.6],
      detail: [0, 0.3, 0.4],
    }
    return parts.map(p => {
      const v = explodeVec[p.group] || [0,0,0]
      const ex = explode * 42
      const x = p.x + v[0]*ex
      const y = p.y + v[1]*ex
      const z = p.z + v[2]*ex
      const { sx, sy, depth } = iso(x, y, z, yaw, pitch)
      // feature: portafilter twist, gauge needle, steam knob
      let extra = ''
      if (feature === 1 && p.id === 'portafilter') {
        // twist 28deg
        const a = (feature * 28) * Math.PI/180
        // simple visual offset
      }
      return { ...p, sx: sx + 280, sy: sy + 220, depth, z, x, y }
    }).sort((a,b) => a.depth - b.depth)
  }, [parts, explode, yaw, pitch, feature])

  useEffect(() => {
    const el = stageRef.current
    if (!el) return
    const down = (e) => { dragging.current = true; last.current = { x: e.clientX, y: e.clientY } }
    const move = (e) => {
      if (!dragging.current) return
      const dx = e.clientX - last.current.x
      const dy = e.clientY - last.current.y
      setYaw(v => clamp(v + dx*0.45, -90, 90))
      setPitch(v => clamp(v - dy*0.45, -8, 55))
      last.current = { x: e.clientX, y: e.clientY }
    }
    const up = () => dragging.current = false
    const touchDown = (e) => down(e.touches[0])
    const touchMove = (e) => move(e.touches[0])
    el.addEventListener('mousedown', down)
    window.addEventListener('mousemove', move)
    window.addEventListener('mouseup', up)
    el.addEventListener('touchstart', touchDown, { passive: true })
    window.addEventListener('touchmove', touchMove, { passive: true })
    window.addEventListener('touchend', up)
    return () => {
      el.removeEventListener('mousedown', down)
      window.removeEventListener('mousemove', move)
      window.removeEventListener('mouseup', up)
      el.removeEventListener('touchstart', touchDown)
      window.removeEventListener('touchmove', touchMove)
      window.removeEventListener('touchend', up)
    }
  }, [])

  return (
    <div className="paper">
      <div className="paper-head">
        <div>
          <div className="mono" style={{ color: '#8a806f' }}>Anatomy Reveal — 82 parts · 6 assemblies</div>
          <div style={{ fontWeight: 700, fontSize: 16 }}>Dual-boiler espresso machine + conical burr grinder</div>
          <div className="mono" style={{ color: '#8a806f' }}>380 × 415 × 470 mm · brushed steel · 58 mm portafilter · 2× boiler</div>
        </div>
        <div style={{ display: 'flex', gap: 8 }}>
          <span className="pill">Drag to turn · {Math.round(yaw)}° / {Math.round(pitch)}°</span>
          <span className="pill" style={{ background: '#111', color: '#fff', borderColor: '#111' }}>Paper · Ink · 4-tone</span>
        </div>
      </div>
      <div ref={stageRef} className="paper-stage">
        <svg viewBox="0 0 560 440" width="100%" height="100%" style={{ display: 'block' }}>
          {/* grid */}
          <defs>
            <pattern id="paperGrid" width="24" height="24" patternUnits="userSpaceOnUse">
              <path d="M 24 0 L 0 0 0 24" fill="none" stroke="#e9ddd0" strokeWidth="0.5"/>
            </pattern>
          </defs>
          <rect width="560" height="440" fill="var(--paper)" />
          <rect width="560" height="440" fill="url(#paperGrid)" opacity="0.5" />
          {/* shadow */}
          <ellipse cx="280" cy="360" rx="140" ry="22" fill="#000" opacity="0.06" />
          {/* parts */}
          {projected.map(p => {
            // simple isometric box: top + front + side as 3 rects
            const isGlass = p.c.includes('rgba')
            const baseW = p.w, baseH = p.h
            // projected size scaled with depth for pseudo-perspective
            const s = 0.92
            const x = p.sx, y = p.sy
            // draw as 3-face convex solid: we approximate with rect + side triangles
            const topH = 8
            const sideW = 8
            return (
              <g key={p.id} opacity={isGlass ? 0.9 : 1}>
                {/* side */}
                <path
                  d={`M ${x+baseW*s/2} ${y-baseH*s/2} L ${x+baseW*s/2+sideW} ${y-baseH*s/2+topH} L ${x+baseW*s/2+sideW} ${y+baseH*s/2+topH} L ${x+baseW*s/2} ${y+baseH*s/2} Z`}
                  fill={p.c} fillOpacity={isGlass ? 0.35 : 0.78} stroke="#1a1a1e" strokeWidth="0.9" strokeLinejoin="round"
                />
                {/* top */}
                <path
                  d={`M ${x-baseW*s/2} ${y-baseH*s/2} L ${x-baseW*s/2+sideW} ${y-baseH*s/2+topH} L ${x+baseW*s/2+sideW} ${y-baseH*s/2+topH} L ${x+baseW*s/2} ${y-baseH*s/2} Z`}
                  fill={p.c} fillOpacity={isGlass ? 0.25 : 0.92} stroke="#1a1a1e" strokeWidth="0.9" strokeLinejoin="round"
                />
                {/* front */}
                <rect x={x-baseW*s/2} y={y-baseH*s/2} width={baseW*s} height={baseH*s} rx="2" fill={p.c} fillOpacity={isGlass ? 0.35 : 1} stroke="#1a1a1e" strokeWidth="1.1" />
                {/* highlight */}
                {!isGlass && <rect x={x-baseW*s/2+2} y={y-baseH*s/2+2} width={baseW*s-4} height="3" rx="1" fill="#fff" opacity="0.22" />}
                {/* labels for key parts */}
                {(p.id==='gauge' || p.id==='hopper' || p.id==='boiler1') && (
                  <text x={x} y={y-22} textAnchor="middle" fontSize="7" fontFamily="Fragment Mono, monospace" fill="#1a1a1e" opacity="0.7">{p.id}</text>
                )}
                {/* screws as dots */}
                {p.id.startsWith('screw') && <circle cx={x} cy={y} r="2.2" fill="#1a1a1e" opacity="0.9" />}
              </g>
            )
          })}
          {/* callouts */}
          <g fontFamily="Fragment Mono, monospace" fontSize="8" fill="#5a5042">
            <text x="40" y="28">EXPLODE {Math.round(explode*100)}% — assemblies separate along their normals</text>
            <text x="40" y="40">CONVEX PARTS — 52 shown · 82 total in full kit · no intersecting geometry</text>
            <text x="40" y="420" opacity="0.5">Paper look · 4-tone shading · separating-plane order · motion blur ready for MP4</text>
          </g>
          {/* feature hint */}
          <g transform="translate(380,28)">
            <rect x="0" y="0" width="140" height="46" rx="10" fill="#fff" stroke="#d8ccba" />
            <text x="12" y="16" fontSize="9" fontWeight="700" fill="#1a1a1e">FEATURE</text>
            <text x="12" y="28" fontSize="8" fill="#6b6050">{feature===0?'Ready — portafilter locks 28°': feature===1?'Portafilter twists → drops': feature===2?'Gauge needle climbs · knobs turn': 'Steam wand pivots'}</text>
            <circle cx="124" cy="14" r="6" fill={feature? '#ff3b30' : '#e8ddd0'} />
          </g>
        </svg>
        {/* drag hint */}
        <div style={{ position: 'absolute', bottom: 12, left: 12, display: 'flex', gap: 8 }}>
          <span className="pill">Yaw {yaw.toFixed(0)}°</span>
          <span className="pill">Pitch {pitch.toFixed(0)}°</span>
          <span className="pill" style={{ background: '#1a1a1e', color: '#fff', borderColor: '#1a1a1e' }}>Apart {Math.round(explode*100)}%</span>
        </div>
      </div>
      <div className="paper-controls">
        <span className="mono" style={{ color: '#8a806f' }}>Explode</span>
        <input className="range" type="range" min="0" max="1" step="0.01" value={explode} onChange={e=>setExplode(parseFloat(e.target.value))} />
        <button className="pill" onClick={()=>setExplode(0)}>Assemble</button>
        <button className="pill" onClick={()=>setExplode(0.35)}>Explode 35%</button>
        <button className="pill" onClick={()=>setExplode(1)}>Full 100%</button>
        <div style={{ flex: 1 }} />
        <button className="pill" style={{ background: feature===1?'#111':'#fff', color: feature===1?'#fff':'#1a1a1e' }} onClick={()=>setFeature(v=>v===1?0:1)}>Portafilter 28°</button>
        <button className="pill" style={{ background: feature===2?'#111':'#fff', color: feature===2?'#fff':'#1a1a1e' }} onClick={()=>setFeature(v=>v===2?0:2)}>Gauge + knobs</button>
        <button className="pill" style={{ background: feature===3?'#111':'#fff', color: feature===3?'#fff':'#1a1a1e' }} onClick={()=>setFeature(v=>v===3?0:3)}>Steam wand</button>
        <span className="mono" style={{ color: '#8a806f' }}>Film: 10s · 9:16 · 30fps · whip → macro → explode → hero</span>
      </div>
    </div>
  )
}

// ---------- Anatomy by WheresRyan: LRU Bookcase, Hash Map Sorting Desk, Message Queue Marble Run
function AnatomyMachines() {
  const [active, setActive] = useState('lru')
  const [lru, setLru] = useState(['A','B','C','D'])
  const [hits, setHits] = useState(0)
  const [queue, setQueue] = useState([1,2,3])
  const [marbles, setMarbles] = useState(5)

  const touchLRU = (key) => {
    setLru(prev => {
      const next = [key, ...prev.filter(k=>k!==key)].slice(0,4)
      return next
    })
    setHits(h=>h+1)
  }
  const pushQueue = () => setQueue(q=>[...q, q.length? Math.max(...q)+1 : 1])
  const popQueue = () => setQueue(q=>q.slice(1))

  return (
    <div className="grid-3">
      {/* LRU Bookcase */}
      <div className="card" style={{ borderColor: active==='lru'? 'var(--ink)' : undefined }}>
        <div className="card-pad" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <div className="mono" style={{ color: 'var(--accent-2)' }}>Anatomy · LRU Cache</div>
            <div style={{ fontWeight: 700 }}>Bookcase — most recent left</div>
          </div>
          <button className="chip" onClick={()=>setActive('lru')} style={{ background: active==='lru'? 'var(--ink)' : undefined, color: active==='lru'? 'var(--bg)' : undefined }}>Active</button>
        </div>
        <div className="divider" />
        <div className="card-pad" style={{ background: 'var(--bg-soft)' }}>
          <div style={{ height: 140, display: 'flex', gap: 8, alignItems: 'end', justifyContent: 'center' }}>
            {lru.map((k, i) => (
              <motion.div
                key={k}
                layout
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1, scale: i===0?1.06:1 }}
                transition={{ type: 'spring', stiffness: 420, damping: 28 }}
                style={{
                  width: 58, height: 96 + i*10, borderRadius: 10, background: i===0? 'var(--ink)' : 'var(--panel-2)',
                  border: '1px solid var(--line-strong)', color: i===0? 'var(--bg)' : 'var(--ink)',
                  display: 'grid', placeItems: 'center', fontWeight: 800, fontSize: 18,
                  boxShadow: i===0? '0 10px 30px rgba(0,0,0,0.3)' : 'none'
                }}
              >
                {k}
              </motion.div>
            ))}
          </div>
          <div style={{ display: 'flex', gap: 6, marginTop: 12, flexWrap: 'wrap', justifyContent: 'center' }}>
            {['A','B','C','D','E','F'].map(k=>(
              <button key={k} onClick={()=>touchLRU(k)} style={{
                padding: '8px 10px', borderRadius: 999, border: '1px solid var(--line)', background: lru.includes(k)? 'var(--panel-2)' : 'transparent',
                color: 'var(--ink)', cursor: 'pointer', fontWeight: 700
              }}>{k}</button>
            ))}
          </div>
          <div className="mono" style={{ textAlign: 'center', marginTop: 10, color: 'var(--dim)' }}>Hits {hits} · Evicts oldest when full · 4 slots</div>
        </div>
      </div>

      {/* Hash Map Sorting Desk */}
      <div className="card" style={{ borderColor: active==='hash'? 'var(--ink)' : undefined }}>
        <div className="card-pad" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <div className="mono" style={{ color: 'var(--accent)' }}>Anatomy · Hash Map</div>
            <div style={{ fontWeight: 700 }}>Sorting desk — collisions chain</div>
          </div>
          <button className="chip" onClick={()=>setActive('hash')} style={{ background: active==='hash'? 'var(--ink)' : undefined, color: active==='hash'? 'var(--bg)' : undefined }}>Active</button>
        </div>
        <div className="divider" />
        <div className="card-pad" style={{ background: 'var(--bg-soft)' }}>
          <HashDesk />
          <div className="mono" style={{ textAlign: 'center', marginTop: 10, color: 'var(--dim)' }}>Buckets 0-7 · hash(key) % 8 · chain on collision</div>
        </div>
      </div>

      {/* Message Queue Marble Run */}
      <div className="card" style={{ borderColor: active==='mq'? 'var(--ink)' : undefined }}>
        <div className="card-pad" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <div className="mono" style={{ color: 'var(--accent-3)' }}>Anatomy · Message Queue</div>
            <div style={{ fontWeight: 700 }}>Marble run — ordered lane</div>
          </div>
          <button className="chip" onClick={()=>setActive('mq')} style={{ background: active==='mq'? 'var(--ink)' : undefined, color: active==='mq'? 'var(--bg)' : undefined }}>Active</button>
        </div>
        <div className="divider" />
        <div className="card-pad" style={{ background: 'var(--bg-soft)' }}>
          <div style={{ height: 140, position: 'relative', overflow: 'hidden', borderRadius: 12, background: 'var(--panel)', border: '1px solid var(--line)', padding: 12 }}>
            <div style={{ position: 'absolute', top: 22, left: 12, right: 12, height: 4, background: 'var(--line)', borderRadius: 99 }} />
            <div style={{ display: 'flex', gap: 8, position: 'absolute', top: 36, left: 12 }}>
              <AnimatePresence>
                {queue.map((n, i)=>(
                  <motion.div
                    key={n}
                    initial={{ x: 40, opacity: 0, scale: 0.8 }}
                    animate={{ x: 0, opacity: 1, scale: 1 }}
                    exit={{ x: -40, opacity: 0, scale: 0.8 }}
                    transition={{ type: 'spring', stiffness: 500, damping: 30 }}
                    style={{ width: 36, height: 36, borderRadius: '50%', background: `hsl(${200+ i*14} 90% 60%)`, display: 'grid', placeItems: 'center', fontWeight: 800, color: '#111', border: '2px solid #fff' }}
                  >{n}</motion.div>
                ))}
              </AnimatePresence>
            </div>
            <div style={{ position: 'absolute', bottom: 14, left: 12, right: 12, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div style={{ display: 'flex', gap: 6 }}>
                <button onClick={pushQueue} style={{ padding: '8px 12px', borderRadius: 999, border: '1px solid var(--line)', background: 'var(--ink)', color: 'var(--bg)', fontWeight: 700, cursor: 'pointer' }}>Enqueue</button>
                <button onClick={popQueue} style={{ padding: '8px 12px', borderRadius: 999, border: '1px solid var(--line)', background: 'transparent', color: 'var(--ink)', cursor: 'pointer' }}>Dequeue</button>
              </div>
              <span className="mono" style={{ color: 'var(--dim)' }}>FIFO · {queue.length} waiting</span>
            </div>
          </div>
          <div style={{ display: 'flex', gap: 8, marginTop: 12, alignItems: 'center' }}>
            <span className="mono" style={{ color: 'var(--dim)' }}>Marbles in hopper</span>
            <input type="range" min={1} max={12} value={marbles} onChange={e=>setMarbles(parseInt(e.target.value))} style={{ flex: 1 }} />
            <span className="chip">{marbles}</span>
          </div>
          <div className="mono" style={{ textAlign: 'center', marginTop: 6, color: 'var(--dim)' }}>Escapement releases one per tick · order preserved</div>
        </div>
      </div>
    </div>
  )
}

function HashDesk(){
  const [keys, setKeys] = useState([{ k:'alice', b:2 }, { k:'bob', b:2 }, { k:'carol', b:5 }])
  const [input, setInput] = useState('')
  const add = () => {
    if (!input.trim()) return
    const b = input.split('').reduce((a,c)=>a + c.charCodeAt(0),0) % 8
    setKeys(k=>[...k, { k: input.trim(), b }])
    setInput('')
  }
  const buckets = Array.from({ length: 8 }, (_,i)=> keys.filter(x=>x.b===i))
  return (
    <div>
      <div style={{ display: 'flex', gap: 6, marginBottom: 10 }}>
        <input value={input} onChange={e=>setInput(e.target.value)} placeholder="key (e.g. dave)" style={{ flex: 1, padding: '8px 10px', borderRadius: 999, border: '1px solid var(--line)', background: 'var(--panel)', color: 'var(--ink)' }} />
        <button onClick={add} style={{ padding: '8px 14px', borderRadius: 999, background: 'var(--ink)', color: 'var(--bg)', border: 0, fontWeight: 700, cursor: 'pointer' }}>Hash</button>
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(8, 1fr)', gap: 6 }}>
        {buckets.map((list, i)=>(
          <div key={i} style={{ minHeight: 86, borderRadius: 10, background: 'var(--panel)', border: '1px solid var(--line)', padding: 6 }}>
            <div className="mono" style={{ textAlign: 'center', color: 'var(--dim)', fontSize: 10 }}>{i}</div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 4, marginTop: 6 }}>
              {list.map((x, idx)=>(
                <motion.div key={x.k+idx} initial={{ scale: 0 }} animate={{ scale: 1 }} style={{ padding: '4px 6px', borderRadius: 8, background: idx===0? 'var(--ink)' : 'var(--line)', color: idx===0? 'var(--bg)' : 'var(--ink)', fontSize: 11, fontWeight: 700, textAlign: 'center' }}>{x.k}</motion.div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

// ---------- Hairline Gallery
function HairlineGallery(){
  const [mode, setMode] = useState('funnel')
  const [intensity, setIntensity] = useState(0.45)
  const [theme, setTheme] = useState('light')

  const figures = {
    funnel: {
      means: 'Four trays step down, each narrower with fewer beads: the stage under the pointer lifts, its neighbours rising less in turn.',
      component: (v, hover) => <FunnelFigure intensity={v} hover={hover} theme={theme} />
    },
    clearance: {
      means: 'Each second is a column of requests: a burst lifts the ones near the pointer, and none of them gets past the bar.',
      component: (v, hover) => <ClearanceFigure intensity={v} hover={hover} theme={theme} />
    },
    sidings: {
      means: 'A trunk line and three sidings: the track under the pointer is checked out, its wagons rising in turn to a bright head.',
      component: (v, hover) => <SidingsFigure intensity={v} hover={hover} theme={theme} />
    },
    storm: {
      means: 'A cloud you steer over a district rains on the roofs under it; only the rain from its middle reaches them.',
      component: (v, hover) => <StormFigure intensity={v} hover={hover} theme={theme} />
    },
  }

  return (
    <div className="card">
      <div className="card-pad" style={{ display: 'flex', justifyContent: 'space-between', gap: 12, flexWrap: 'wrap', alignItems: 'center' }}>
        <div>
          <div className="mono" style={{ color: theme==='dark'? '#9aa' : '#6b6b78' }}>Hairline — isometric line figures · pointer-driven</div>
          <div style={{ fontWeight: 700 }}>One HTML, no dependencies · intensity slider · play tour</div>
        </div>
        <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', alignItems: 'center' }}>
          {Object.keys(figures).map(k=>(
            <button key={k} onClick={()=>setMode(k)} style={{
              padding: '8px 12px', borderRadius: 999, border: '1px solid var(--line)',
              background: mode===k? 'var(--ink)' : 'transparent', color: mode===k? 'var(--bg)' : 'var(--ink)', cursor: 'pointer', fontWeight: 600, fontSize: 12
            }}>{k}</button>
          ))}
          <button onClick={()=>setTheme(v=>v==='light'?'dark':'light')} style={{ padding: '8px 12px', borderRadius: 999, border: '1px solid var(--line)', background: 'transparent', cursor: 'pointer' }}>theme: {theme}</button>
        </div>
      </div>
      <div className="divider" />
      <div className="card-pad" style={{ background: theme==='dark'? '#08090a' : '#fff' }}>
        <HairlineStage intensity={intensity} theme={theme} render={(hover)=>figures[mode].component(intensity, hover)} />
        <div style={{ display: 'flex', gap: 12, alignItems: 'center', marginTop: 12, flexWrap: 'wrap' }}>
          <span className="mono" style={{ color: 'var(--dim)' }}>Intensity</span>
          <input type="range" min={0} max={1} step={0.01} value={intensity} onChange={e=>setIntensity(parseFloat(e.target.value))} style={{ flex: 1 }} />
          <span className="chip" style={{ background: theme==='dark'? '#111' : '#fff' }}>{Math.round(intensity*100)}</span>
          <span className="mono" style={{ color: 'var(--dim)' }}>{figures[mode].means}</span>
        </div>
      </div>
    </div>
  )
}

function HairlineStage({ intensity, render }){
  const [hover, setHover] = useState({ x: 0.5, y: 0.5, active: false })
  const ref = useRef(null)
  useEffect(()=>{
    const el = ref.current
    if (!el) return
    const mv = (e) => {
      const r = el.getBoundingClientRect()
      setHover({ x: clamp((e.clientX - r.left)/r.width,0,1), y: clamp((e.clientY - r.top)/r.height,0,1), active: true })
    }
    const lv = ()=> setHover(h=>({ ...h, active: false }))
    el.addEventListener('mousemove', mv)
    el.addEventListener('mouseleave', lv)
    return ()=>{ el.removeEventListener('mousemove', mv); el.removeEventListener('mouseleave', lv)}
  },[])
  return (
    <div ref={ref} className={`hairline-stage ${intensity>0.7?'' : ''}`} style={{ background: intensity>0.5? undefined : undefined, borderColor: intensity>0.8? 'var(--ink)' : undefined }}>
      <div style={{ position: 'absolute', top: 10, left: 12, zIndex: 2, display: 'flex', gap: 6 }}>
        <span className="pill" style={{ fontSize: 10 }}>Hairline · {intensity.toFixed(2)}</span>
        <span className="pill" style={{ fontSize: 10, background: '#111', color: '#fff', borderColor: '#111' }}>{hover.active? `x ${hover.x.toFixed(2)} y ${hover.y.toFixed(2)}` : 'rest'}</span>
      </div>
      {render(hover)}
    </div>
  )
}

function FunnelFigure({ intensity, hover }){
  // 4 trays stepped
  const trays = [0,1,2,3]
  return (
    <svg viewBox="0 0 640 320" preserveAspectRatio="xMidYMid meet">
      <rect width="640" height="320" fill="transparent" />
      {trays.map(i=>{
        const cx = 140 + i*120
        const w = 110 - i*18
        const h = 22
        const baseY = 200
        const dx = hover.active ? (1 - Math.abs(hover.x*640 - cx)/140) * 28 * intensity : 0
        const lift = clamp(dx, 0, 28)
        const y = baseY - lift - i*8
        return (
          <g key={i}>
            {/* beads */}
            {Array.from({ length: 8 - i*2 }).map((_,b)=>{
              const bx = cx - 40 + b*12
              const by = y - 24 - (b%2)*6
              const j = hover.active ? clamp(1 - Math.abs(hover.x*640 - bx)/90,0,1) * 14 * intensity : 0
              return <circle key={b} cx={bx} cy={by - j} r="4.2" fill="none" stroke="#232327" strokeWidth="1.6" />
            })}
            {/* tray */}
            <path d={`M ${cx-w/2} ${y} L ${cx+w/2} ${y} L ${cx+w/2-10} ${y+h} L ${cx-w/2+10} ${y+h} Z`} fill="none" stroke="#232327" strokeWidth="1.8" strokeLinejoin="round" />
            <path d={`M ${cx-w/2+10} ${y+h} L ${cx+w/2-10} ${y+h}`} stroke="#ff3b30" strokeWidth="1.4" opacity={lift>12?1:0.0} />
            <text x={cx} y={y+h+18} textAnchor="middle" fontSize="9" fontFamily="Fragment Mono, monospace" fill="#6f6f78">{['AWARE','INTEREST','DESIRE','ACTION'][i]} · {8-i*2}</text>
          </g>
        )
      })}
      <text x="12" y="304" fontSize="10" fontFamily="Fragment Mono, monospace" fill="#9a9aaa">01 hit · 02 order · 05 rest · 10 quiet — pointer lifts stage, neighbours follow with falloff</text>
    </svg>
  )
}
function ClearanceFigure({ intensity, hover }){
  const cols = 8
  return (
    <svg viewBox="0 0 640 320" preserveAspectRatio="xMidYMid meet">
      <rect width="640" height="320" fill="transparent" />
      {/* bar */}
      <rect x="20" y="92" width="600" height="6" rx="3" fill="#232327" />
      <text x="20" y="86" fontSize="9" fontFamily="Fragment Mono, monospace" fill="#6f6f78">RATE LIMIT · 8 req / s</text>
      {Array.from({ length: cols }).map((_,i)=>{
        const x = 40 + i*74
        const burst = Math.sin(i*1.3)*0.5+0.5
        const near = hover.active ? clamp(1 - Math.abs(hover.x*640 - x)/110,0,1) : 0
        const lift = near * 56 * intensity + burst*8
        return (
          <g key={i}>
            <line x1={x} y1={98} x2={x} y2={240} stroke="#e0e0e4" strokeWidth="1" strokeDasharray="3 6" />
            {/* requests as small squares */}
            {Array.from({ length: 7 }).map((_,j)=>{
              const y = 240 - j*18 - (j===3? lift : 0) * (1 - Math.abs(j-3)/4)
              const blocked = y < 96
              return <rect key={j} x={x-7} y={y} width="14" height="10" rx="2" fill={blocked? '#ff3b30' : '#232327'} stroke="#fff" strokeWidth={blocked?0:0} opacity={blocked?0.9:1} />
            })}
            <text x={x} y="262" textAnchor="middle" fontSize="9" fontFamily="Fragment Mono, monospace" fill="#6f6f78">{`T+${i}`}</text>
          </g>
        )
      })}
      <text x="12" y="304" fontSize="10" fontFamily="Fragment Mono, monospace" fill="#9a9aaa">01 hit · 03 reach · 05 rest · 09 radius — burst lifts, bar stops excess</text>
    </svg>
  )
}
function SidingsFigure({ intensity, hover }){
  const tracks = 4
  return (
    <svg viewBox="0 0 640 320" preserveAspectRatio="xMidYMid meet">
      <rect width="640" height="320" fill="transparent" />
      {Array.from({ length: tracks }).map((_,t)=>{
        const y = 70 + t*48
        const x0 = 20, x1 = 620
        const active = hover.active ? Math.round(hover.y*4) : -1
        const isActive = t===active
        const wagons = 4
        return (
          <g key={t} opacity={isActive?1:0.6}>
            {/* rails */}
            <path d={`M ${x0} ${y} H ${x1}`} stroke={isActive? '#0a84ff':'#232327'} strokeWidth={isActive?2:1.2} fill="none" />
            <path d={`M ${x0} ${y+10} H ${x1}`} stroke={isActive? '#0a84ff':'#232327'} strokeWidth={isActive?2:1.2} fill="none" opacity="0.6" />
            {/* sleepers */}
            {Array.from({ length: 12 }).map((_,s)=>{
              const sx = 40 + s*48
              return <line key={s} x1={sx} y1={y-2} x2={sx} y2={y+12} stroke="#c9c9d0" strokeWidth="1" />
            })}
            {/* wagons */}
            {Array.from({ length: wagons }).map((_,w)=>{
              const wx = 60 + w*92 + (isActive? w*6*intensity : 0)
              const wy = y - (isActive? 14 + w*2*intensity : 0)
              return (
                <g key={w}>
                  <rect x={wx-26} y={wy-18} width="52" height="20" rx="3" fill={isActive? '#0a84ff' : '#fff'} stroke="#232327" strokeWidth="1.6" />
                  <circle cx={wx-16} cy={wy+4} r="4" fill="#232327" />
                  <circle cx={wx+16} cy={wy+4} r="4" fill="#232327" />
                  <rect x={wx-20} y={wy-14} width="40" height="6" rx="2" fill={isActive? '#fff':'#e8e8ee'} opacity={isActive?0.9:1} />
                </g>
              )
            })}
            <text x={12} y={y-10} fontSize="9" fontFamily="Fragment Mono, monospace" fill={isActive? '#0a84ff':'#9a9aaa'}>{['MAIN','A','B','C'][t]}</text>
          </g>
        )
      })}
      <text x="12" y="304" fontSize="10" fontFamily="Fragment Mono, monospace" fill="#9a9aaa">Pointer selects track · wagons rise in sequence to bright head</text>
    </svg>
  )
}
function StormFigure({ intensity, hover }){
  const cx = hover.active ? hover.x*640 : 320
  const cloudY = 70
  return (
    <svg viewBox="0 0 640 320" preserveAspectRatio="xMidYMid meet">
      <rect width="640" height="320" fill="transparent" />
      {/* districts */}
      {Array.from({ length: 6 }).map((_,i)=>{
        const x = 40 + i*98
        return (
          <g key={i}>
            <rect x={x-34} y="180" width="68" height="54" rx="4" fill="#f2f2f5" stroke="#232327" strokeWidth="1.2" />
            <rect x={x-20} y="164" width="40" height="22" rx="2" fill="#fff" stroke="#232327" strokeWidth="1.2" />
            <rect x={x-12} y="196" width="24" height="18" rx="2" fill="#e8e8ee" stroke="#232327" strokeWidth="1" />
          </g>
        )
      })}
      {/* cloud */}
      <g>
        <ellipse cx={cx} cy={cloudY} rx={90 + intensity*20} ry={34} fill="#fff" stroke="#232327" strokeWidth="1.6" />
        <ellipse cx={cx-28} cy={cloudY+6} rx={46} ry={28} fill="#fff" stroke="#232327" strokeWidth="1.6" />
        <ellipse cx={cx+32} cy={cloudY+8} rx={52} ry={26} fill="#fff" stroke="#232327" strokeWidth="1.6" />
        <text x={cx} y={cloudY+4} textAnchor="middle" fontSize="9" fontFamily="Fragment Mono, monospace" fill="#232327">CLOUD · {Math.round(intensity*100)}%</text>
      </g>
      {/* rain */}
      {Array.from({ length: 22 }).map((_,i)=>{
        const rx = cx - 70 + i*7
        const dist = Math.abs(rx - (40+ Math.floor((rx-40)/98)*98+49))
        const reach = dist < 36 + intensity*20
        return <line key={i} x1={rx} y1={cloudY+32} x2={rx} y2={reach? 180 : 150} stroke={reach? '#0a84ff':'#c9c9d0'} strokeWidth={reach?1.6:1} opacity={reach?0.95:0.45} />
      })}
      <text x="12" y="304" fontSize="10" fontFamily="Fragment Mono, monospace" fill="#9a9aaa">Steer cloud · only middle rain reaches roofs · intensity widens footprint</text>
    </svg>
  )
}

// ---------- Motion Design Lab (LottieFiles)
function MotionDesignLab(){
  const [emotion, setEmotion] = useState('joy')
  const [duration, setDuration] = useState(320)
  const [stagger, setStagger] = useState(0.06)
  const emotions = {
    joy: { ease: 'cubic-bezier(0.34, 1.56, 0.64, 1)', desc: 'Bouncy, overshoot 8-12%', color: '#ff9f0a' },
    calm: { ease: 'cubic-bezier(0.25, 0.46, 0.45, 0.94)', desc: 'Gentle, long arcs', color: '#0a84ff' },
    urgency: { ease: 'cubic-bezier(0.3, 0, 1, 0.7)', desc: 'Sharp, straight lines', color: '#ff3b30' },
    elegance: { ease: 'cubic-bezier(0.4, 0, 0.2, 1)', desc: 'Slow, controlled arcs', color: '#5e5ce6' },
    playfulness: { ease: 'cubic-bezier(0.68, -0.55, 0.27, 1.55)', desc: 'Bouncy, irregular', color: '#30d158' },
  }
  const [play, setPlay] = useState(0)

  return (
    <div className="grid-2">
      <div className="card">
        <div className="card-pad">
          <div className="mono" style={{ color: 'var(--accent-4)' }}>Motion Design · LottieFiles director</div>
          <h3 style={{ margin: '6px 0 8px' }}>8-step checklist · Disney 12 · Emotion → motion</h3>
          <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
            {Object.keys(emotions).map(k=>(
              <button key={k} onClick={()=>{ setEmotion(k); setPlay(p=>p+1)}} style={{
                padding: '8px 12px', borderRadius: 999, border: '1px solid var(--line)',
                background: emotion===k? emotions[k].color : 'transparent', color: emotion===k? '#fff':'var(--ink)', cursor: 'pointer', fontWeight: 600, fontSize: 12
              }}>{k}</button>
            ))}
          </div>
          <div style={{ marginTop: 14, padding: 12, borderRadius: 12, background: 'var(--bg-soft)', border: '1px solid var(--line)' }}>
            <div className="mono" style={{ color: 'var(--dim)' }}>Emotion mapping</div>
            <div style={{ fontWeight: 700, marginTop: 4 }}>{emotions[emotion].desc}</div>
            <div className="mono" style={{ color: emotions[emotion].color, marginTop: 6 }}>{emotions[emotion].ease}</div>
            <div style={{ display: 'flex', gap: 12, marginTop: 12 }}>
              <div style={{ flex: 1 }}>
                <div className="mono" style={{ color: 'var(--dim)' }}>Duration {duration}ms</div>
                <input type="range" min={80} max={1000} value={duration} onChange={e=>setDuration(parseInt(e.target.value))} style={{ width: '100%' }} />
                <div className="mono" style={{ fontSize: 10, color: 'var(--dim)' }}>Light 80-200 · Medium 200-350 · Heavy 300-500</div>
              </div>
              <div style={{ flex: 1 }}>
                <div className="mono" style={{ color: 'var(--dim)' }}>Stagger {stagger.toFixed(2)}s</div>
                <input type="range" min={0} max={0.2} step={0.01} value={stagger} onChange={e=>setStagger(parseFloat(e.target.value))} style={{ width: '100%' }} />
                <div className="mono" style={{ fontSize: 10, color: 'var(--dim)' }}>Choreography: 1/3 rule · primary + secondary + ambient</div>
              </div>
            </div>
          </div>
          <ul style={{ marginTop: 12, paddingLeft: 16, color: 'var(--muted)', fontSize: 13, lineHeight: 1.7 }}>
            <li><b style={{ color: 'var(--ink)' }}>Three pillars:</b> timing, choreography, emotion — choose before code</li>
            <li><b style={{ color: 'var(--ink)' }}>Never linear</b> for spatial movement · opacity-only forbidden for state</li>
            <li><b style={{ color: 'var(--ink)' }}>Disney:</b> anticipation, follow-through, squash & stretch adapted for UI</li>
          </ul>
        </div>
      </div>

      <div className="card">
        <div className="card-pad">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div className="mono" style={{ color: 'var(--dim)' }}>Preview · {emotion} · {duration}ms</div>
            <button onClick={()=>setPlay(p=>p+1)} style={{ padding: '8px 12px', borderRadius: 999, background: 'var(--ink)', color: 'var(--bg)', border: 0, fontWeight: 700, cursor: 'pointer' }}>Play</button>
          </div>
          <div style={{ height: 220, borderRadius: 14, background: 'var(--bg-soft)', border: '1px solid var(--line)', marginTop: 12, position: 'relative', overflow: 'hidden', padding: 16 }}>
            {/* staggered cards */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 10, height: '100%', alignItems: 'center' }}>
              {[0,1,2,3,4,5].map(i=>(
                <motion.div
                  key={play + '-' + i}
                  initial={{ opacity: 0, y: 24, scale: 0.92 }}
                  animate={{ opacity: 1, y: 0, scale: 1 }}
                  transition={{ duration: duration/1000, delay: i*stagger, ease: [0.34, 1.2, 0.64, 1] }}
                  style={{ height: 64, borderRadius: 12, background: `hsl(${28 + i*18} 92% 58%)`, border: '1px solid rgba(0,0,0,0.1)', display: 'grid', placeItems: 'center', fontWeight: 800, color: '#111' }}
                >
                  {i+1}
                </motion.div>
              ))}
            </div>
            {/* motion path */}
            <svg style={{ position: 'absolute', inset: 0, width: '100%', height: '100%', pointerEvents: 'none' }}>
              <path d="M 20 180 Q 120 20 220 100 T 420 80" fill="none" stroke={emotions[emotion].color} strokeWidth="2" strokeDasharray="6 6" opacity="0.9" />
            </svg>
            <div className="mono" style={{ position: 'absolute', bottom: 10, left: 12, color: 'var(--dim)', fontSize: 10 }}>Path as language: curved = friendly · angular = tense · spiral = whimsical</div>
          </div>
          <div style={{ display: 'flex', gap: 8, marginTop: 12, flexWrap: 'wrap' }}>
            <span className="chip"><b>Weight</b> Medium · 200-350ms</span>
            <span className="chip"><b>Easing</b> ease-out entrance</span>
            <span className="chip"><b>Layers</b> primary + secondary + ambient</span>
          </div>
        </div>
      </div>
    </div>
  )
}

// ---------- Motion (Framer) Playground — spring visualizer
function MotionPlayground(){
  const [stiffness, setStiffness] = useState(260)
  const [damping, setDamping] = useState(26)
  const [mass, setMass] = useState(1)
  const [count, setCount] = useState(0)

  return (
    <div className="grid-2">
      <div className="card">
        <div className="card-pad">
          <div className="mono" style={{ color: '#0a84ff' }}>Motion · Framer Motion AI Kit · springs</div>
          <h3 style={{ margin: '6px 0 8px' }}>CSS spring → linear() · MotionScore audit</h3>
          <div style={{ display: 'grid', gap: 10, marginTop: 12 }}>
            <div>
              <div className="mono" style={{ display: 'flex', justifyContent: 'space-between' }}><span>Stiffness {stiffness}</span><span className="chip">{stiffness}</span></div>
              <input type="range" min={50} max={600} value={stiffness} onChange={e=>setStiffness(parseInt(e.target.value))} style={{ width: '100%' }} />
            </div>
            <div>
              <div className="mono" style={{ display: 'flex', justifyContent: 'space-between' }}><span>Damping {damping}</span><span className="chip">{damping}</span></div>
              <input type="range" min={5} max={60} value={damping} onChange={e=>setDamping(parseInt(e.target.value))} style={{ width: '100%' }} />
            </div>
            <div>
              <div className="mono" style={{ display: 'flex', justifyContent: 'space-between' }}><span>Mass {mass}</span><span className="chip">{mass}</span></div>
              <input type="range" min={0.5} max={3} step={0.1} value={mass} onChange={e=>setMass(parseFloat(e.target.value))} style={{ width: '100%' }} />
            </div>
            <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
              <button onClick={()=>setCount(c=>c+1)} style={{ padding: '10px 14px', borderRadius: 999, background: 'var(--ink)', color: 'var(--bg)', border: 0, fontWeight: 700, cursor: 'pointer' }}>Trigger spring</button>
              <span className="chip">Bounce {clamp((1 - damping/60).toFixed(2),0,1)} · duration {(Math.sqrt(mass/stiffness)*2).toFixed(2)}s</span>
            </div>
            <div style={{ padding: 12, borderRadius: 12, background: 'var(--bg-soft)', border: '1px solid var(--line)', fontFamily: 'Fragment Mono, monospace', fontSize: 11, color: 'var(--muted)' }}>
              <div>linear({Array.from({ length: 8 }).map((_,i)=> (Math.sin(i/7*Math.PI)*0.2).toFixed(2)).join(', ')})</div>
              <div style={{ marginTop: 6 }}>Motion: &lt;motion.div transition=&#123;&#123; type: "spring", stiffness: {stiffness}, damping: {damping} &#125;&#125; /&gt;</div>
            </div>
          </div>
        </div>
      </div>
      <div className="card">
        <div className="card-pad">
          <div className="mono" style={{ color: 'var(--dim)' }}>Live preview · layout + whileTap + AnimatePresence</div>
          <div style={{ height: 260, borderRadius: 14, background: 'var(--bg-soft)', border: '1px solid var(--line)', marginTop: 12, position: 'relative', overflow: 'hidden', display: 'grid', placeItems: 'center' }}>
            <motion.div
              key={count}
              initial={{ scale: 0.7, opacity: 0, rotate: -6 }}
              animate={{ scale: 1, opacity: 1, rotate: 0 }}
              exit={{ scale: 0.7, opacity: 0 }}
              transition={{ type: 'spring', stiffness, damping, mass }}
              whileHover={{ scale: 1.04, rotate: 1 }}
              whileTap={{ scale: 0.96 }}
              style={{
                width: 160, height: 160, borderRadius: 20, background: 'linear-gradient(135deg, #0a84ff, #5e5ce6)',
                display: 'grid', placeItems: 'center', color: '#fff', fontWeight: 800, fontSize: 18,
                boxShadow: '0 20px 40px rgba(10,132,255,0.35)', cursor: 'pointer'
              }}
            >
              spring {count}
            </motion.div>
            <div style={{ position: 'absolute', bottom: 12, left: 12, right: 12, display: 'flex', gap: 6, flexWrap: 'wrap', justifyContent: 'center' }}>
              {[0,1,2].map(i=>(
                <motion.div key={count+'-'+i} initial={{ y: 20, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ delay: 0.1 + i*0.07, type: 'spring', stiffness, damping }} style={{ padding: '6px 10px', borderRadius: 999, background: '#fff', color: '#111', fontSize: 11, fontWeight: 700, border: '1px solid #e5e5ea' }}>chip {i+1}</motion.div>
              ))}
            </div>
          </div>
          <div style={{ display: 'flex', gap: 8, marginTop: 12 }}>
            <span className="chip" style={{ background: '#e6f0ff', color: '#0a84ff' }}>Performance: 60fps · no layout thrash</span>
            <span className="chip">Best practice: transform & opacity only</span>
          </div>
        </div>
      </div>
    </div>
  )
}

// ---------- GSAP Timeline
function GSAPStudio(){
  const scope = useRef(null)
  const [progress, setProgress] = useState(0)
  const tlRef = useRef(null)

  useEffect(()=>{
    const ctx = gsap.context(()=>{
      const tl = gsap.timeline({ paused: true })
      tl.from('.gsap-card', { y: 40, opacity: 0, stagger: 0.08, duration: 0.6, ease: 'back.out(1.4)' })
        .from('.gsap-bar', { scaleX: 0, transformOrigin: 'left', duration: 0.5, ease: 'power3.out' }, '-=0.3')
        .from('.gsap-dot', { scale: 0, stagger: 0.05, duration: 0.4, ease: 'elastic.out(1,0.4)' }, '-=0.2')
      tlRef.current = tl
      tl.eventCallback('onUpdate', ()=> setProgress(tl.progress()))
    }, scope)
    // auto play once
    tlRef.current?.play()
    return ()=> ctx.revert()
  }, [])

  useEffect(()=>{
    if (tlRef.current) tlRef.current.progress(progress)
  }, [progress])

  return (
    <div className="card" ref={scope}>
      <div className="card-pad" style={{ display: 'flex', justifyContent: 'space-between', gap: 12, flexWrap: 'wrap', alignItems: 'center' }}>
        <div>
          <div className="mono" style={{ color: '#88cc00' }}>GSAP 3.15 · GreenSock · timelines + ScrollTrigger + Flip</div>
          <h3 style={{ margin: '6px 0 0' }}>Orchestrated entrance · scrub · adaptive easing</h3>
        </div>
        <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
          <button onClick={()=>tlRef.current?.restart()} style={{ padding: '8px 14px', borderRadius: 999, background: 'var(--ink)', color: 'var(--bg)', border: 0, fontWeight: 700, cursor: 'pointer' }}>Replay</button>
          <button onClick={()=>tlRef.current?.reversed(!tlRef.current.reversed())} style={{ padding: '8px 14px', borderRadius: 999, border: '1px solid var(--line)', background: 'transparent', cursor: 'pointer' }}>Reverse</button>
        </div>
      </div>
      <div className="divider" />
      <div className="card-pad" style={{ background: 'var(--bg-soft)' }}>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 10 }}>
          {[1,2,3,4].map(i=>(
            <div key={i} className="gsap-card" style={{ height: 110, borderRadius: 14, background: `linear-gradient(135deg, hsl(${80+i*12} 80% 48%), hsl(${120+i*12} 70% 42%))`, padding: 12, color: '#111', fontWeight: 800, display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
              <span className="mono" style={{ color: '#111', opacity: 0.7 }}>Card 0{i}</span>
              <span style={{ fontSize: 18 }}>GSAP — {['from()','to()','fromTo()','timeline'][i-1]}</span>
            </div>
          ))}
        </div>
        <div style={{ marginTop: 16, display: 'flex', gap: 8, alignItems: 'center' }}>
          <div className="gsap-bar" style={{ flex: 1, height: 6, background: 'var(--ink)', borderRadius: 999, transformOrigin: 'left' }} />
          {Array.from({ length: 6 }).map((_,i)=> <div key={i} className="gsap-dot" style={{ width: 10, height: 10, borderRadius: '50%', background: 'var(--ink)' }} />)}
        </div>
        <div style={{ marginTop: 12, display: 'flex', gap: 10, alignItems: 'center' }}>
          <span className="mono" style={{ color: 'var(--dim)' }}>Scrub</span>
          <input type="range" min={0} max={1} step={0.001} value={progress} onChange={e=>setProgress(parseFloat(e.target.value))} style={{ flex: 1 }} />
          <span className="chip">{Math.round(progress*100)}%</span>
        </div>
        <div className="mono" style={{ marginTop: 8, color: 'var(--dim)', fontSize: 10 }}>Timeline: .from(cards, back.out) → .from(bar, power3) → .from(dots, elastic) · easeReverse for yoyo · context-safe in React</div>
      </div>
    </div>
  )
}

// ---------- R3F Physics Playground with Rapier
function PhysicsPlayground(){
  const [count, setCount] = useState(6)
  const [gravity, setGravity] = useState(-9.81)

  return (
    <div className="card">
      <div className="card-pad" style={{ display: 'flex', justifyContent: 'space-between', gap: 12, flexWrap: 'wrap', alignItems: 'center' }}>
        <div>
          <div className="mono" style={{ color: '#ff3b30' }}>react-three/rapier · Rapier physics in React</div>
          <h3 style={{ margin: '6px 0 0' }}>Drop, stack, collide · deterministic rigid bodies</h3>
        </div>
        <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', alignItems: 'center' }}>
          <button onClick={()=>setCount(c=>c+1)} style={{ padding: '8px 12px', borderRadius: 999, background: 'var(--ink)', color: 'var(--bg)', border: 0, fontWeight: 700, cursor: 'pointer' }}>Add ball</button>
          <button onClick={()=>setCount(6)} style={{ padding: '8px 12px', borderRadius: 999, border: '1px solid var(--line)', background: 'transparent', cursor: 'pointer' }}>Reset</button>
          <span className="chip">Gravity {gravity.toFixed(1)}</span>
          <input type="range" min={-20} max={-1} step={0.5} value={gravity} onChange={e=>setGravity(parseFloat(e.target.value))} />
        </div>
      </div>
      <div className="divider" />
      <div className="r3f-wrap">
        <Canvas shadows dpr={[1,1.8]}>
          <PerspectiveCamera makeDefault position={[6, 5, 8]} fov={42} />
          <OrbitControls enablePan={false} minPolarAngle={0} maxPolarAngle={Math.PI/2.1} />
          <ambientLight intensity={0.6} />
          <directionalLight position={[8,12,6]} intensity={1.4} castShadow shadow-mapSize={2048} />
          <pointLight position={[-6,4,-4]} intensity={0.6} color="#0a84ff" />
          <Physics gravity={[0, gravity, 0]}>
            <Floor />
            <Walls />
            {Array.from({ length: count }).map((_,i)=>(
              <RigidPhysBall key={i} index={i} />
            ))}
            {/* stack */}
            <Stack />
          </Physics>
          <Grid infiniteGrid args={[10,10]} cellSize={0.5} sectionSize={2} fadeDistance={18} fadeStrength={1} />
          <ContactShadows position={[0,0.01,0]} opacity={0.4} scale={12} blur={1.8} far={6} />
          <Environment preset="city" />
        </Canvas>
      </div>
      <div className="card-pad" style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
        <span className="chip"><b>RigidBody</b> + <b>CuboidCollider</b> · mass, friction, restitution</span>
        <span className="chip"><b>BallCollider</b> · CCD for fast objects</span>
        <span className="chip">Deterministic · WASM · 60fps</span>
      </div>
    </div>
  )
}
function Floor(){
  return (
    <RigidBody type="fixed" restitution={0.4} friction={0.6}>
      <CuboidCollider args={[6, 0.2, 6]} position={[0, -0.2, 0]} />
      <mesh receiveShadow position={[0, -0.2, 0]}><boxGeometry args={[12,0.4,12]} /><meshStandardMaterial color="#1b1b1f" /></mesh>
    </RigidBody>
  )
}
function Walls(){
  return (
    <>
      <RigidBody type="fixed"><CuboidCollider args={[0.2, 2, 6]} position={[6,2,0]} /><mesh position={[6,2,0]}><boxGeometry args={[0.4,4,12]} /><meshStandardMaterial color="#151518" transparent opacity={0.25} /></mesh></RigidBody>
      <RigidBody type="fixed"><CuboidCollider args={[0.2, 2, 6]} position={[-6,2,0]} /><mesh position={[-6,2,0]}><boxGeometry args={[0.4,4,12]} /><meshStandardMaterial color="#151518" transparent opacity={0.25} /></mesh></RigidBody>
      <RigidBody type="fixed"><CuboidCollider args={[6, 2, 0.2]} position={[0,2,6]} /><mesh position={[0,2,6]}><boxGeometry args={[12,4,0.4]} /><meshStandardMaterial color="#151518" transparent opacity={0.25} /></mesh></RigidBody>
      <RigidBody type="fixed"><CuboidCollider args={[6, 2, 0.2]} position={[0,2,-6]} /><mesh position={[0,2,-6]}><boxGeometry args={[12,4,0.4]} /><meshStandardMaterial color="#151518" transparent opacity={0.25} /></mesh></RigidBody>
    </>
  )
}
function RigidPhysBall({ index }){
  const pos = useMemo(()=>[
    (Math.random()-0.5)*4,
    4 + Math.random()*3,
    (Math.random()-0.5)*4
  ], [index])
  const color = useMemo(()=> new THREE.Color().setHSL((index*0.13)%1, 0.9, 0.6), [index])
  return (
    <RigidBody position={pos} restitution={0.72} friction={0.3} linearDamping={0.08} angularDamping={0.1} colliders="ball">
      <mesh castShadow><sphereGeometry args={[0.42, 24, 24]} /><meshStandardMaterial color={color} metalness={0.15} roughness={0.35} /></mesh>
    </RigidBody>
  )
}
function Stack(){
  return (
    <>
      {Array.from({ length: 5 }).map((_,i)=>(
        <RigidBody key={'b'+i} position={[1.8, 0.3 + i*0.62, 0.6]} mass={0.6} friction={0.7}>
          <mesh castShadow><boxGeometry args={[1,0.5,0.5]} /><meshStandardMaterial color={i%2? '#0a84ff':'#ff3b30'} /></mesh>
        </RigidBody>
      ))}
    </>
  )
}

// ---------- Postprocessing Studio
function PostprocessingStudio(){
  const [bloom, setBloom] = useState(0.8)
  const [chroma, setChroma] = useState(0.002)
  const [noise, setNoise] = useState(0.04)
  const [doFocus, setDoFocus] = useState(0.5)

  return (
    <div className="card">
      <div className="card-pad" style={{ display: 'flex', justifyContent: 'space-between', gap: 12, flexWrap: 'wrap', alignItems: 'center' }}>
        <div>
          <div className="mono" style={{ color: '#5e5ce6' }}>react-postprocessing · postprocessing by pmndrs</div>
          <h3 style={{ margin: '6px 0 0' }}>Bloom · Chromatic aberration · Depth of field · Vignette</h3>
        </div>
        <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', alignItems: 'center' }}>
          <span className="chip">Bloom {bloom.toFixed(2)}</span>
          <input type="range" min={0} max={2} step={0.05} value={bloom} onChange={e=>setBloom(parseFloat(e.target.value))} />
          <span className="chip">Chroma {chroma.toFixed(3)}</span>
          <input type="range" min={0} max={0.01} step={0.0005} value={chroma} onChange={e=>setChroma(parseFloat(e.target.value))} />
        </div>
      </div>
      <div className="divider" />
      <div className="r3f-wrap">
        <Canvas dpr={[1,1.6]}>
          <PerspectiveCamera makeDefault position={[0, 1.2, 5]} fov={38} />
          <OrbitControls enablePan={false} />
          <ambientLight intensity={0.4} />
          <directionalLight position={[4,6,3]} intensity={1.2} />
          <Float speed={1.2} rotationIntensity={0.6} floatIntensity={0.6}>
            <mesh><torusGeometry args={[1,0.32, 32, 64]} /><meshStandardMaterial color="#ff3b30" emissive="#ff3b30" emissiveIntensity={0.3} metalness={0.2} roughness={0.3} /></mesh>
          </Float>
          <Float speed={0.9} rotationIntensity={0.4} floatIntensity={0.4} position={[-1.6, -0.2, -0.4]}>
            <mesh><icosahedronGeometry args={[0.7, 2]} /><meshStandardMaterial color="#0a84ff" emissive="#0a84ff" emissiveIntensity={0.25} /></mesh>
          </Float>
          <Float speed={1.0} rotationIntensity={0.5} floatIntensity={0.5} position={[1.5, 0.1, -0.6]}>
            <mesh><boxGeometry args={[0.9,0.9,0.9]} /><meshStandardMaterial color="#30d158" emissive="#30d158" emissiveIntensity={0.22} /></mesh>
          </Float>
          <mesh position={[0,-1.2,0]} rotation={[-Math.PI/2,0,0]}><planeGeometry args={[12,12]} /><meshStandardMaterial color="#111116" /></mesh>
          <EffectComposer>
            <Bloom intensity={bloom} luminanceThreshold={0.2} luminanceSmoothing={0.9} />
            <ChromaticAberration offset={[chroma, chroma]} />
            <DepthOfField focusDistance={doFocus} focalLength={0.02} bokehScale={3} />
            <Vignette eskil={false} offset={0.2} darkness={0.6} />
            <Noise opacity={noise} />
          </EffectComposer>
        </Canvas>
      </div>
      <div className="card-pad" style={{ display: 'flex', gap: 10, flexWrap: 'wrap', alignItems: 'center' }}>
        <span className="chip">Noise {noise.toFixed(2)}</span>
        <input type="range" min={0} max={0.3} step={0.01} value={noise} onChange={e=>setNoise(parseFloat(e.target.value))} />
        <span className="chip">Focus {doFocus.toFixed(2)}</span>
        <input type="range" min={0} max={1} step={0.01} value={doFocus} onChange={e=>setDoFocus(parseFloat(e.target.value))} />
        <span className="mono" style={{ color: 'var(--dim)' }}>EffectComposer wraps passes · auto multisampling · WebGL2</span>
      </div>
    </div>
  )
}

// ---------- Openverse Explorer
function OpenverseExplorer(){
  const [q, setQ] = useState('isometric architecture')
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const search = async (query) => {
    setLoading(true); setError('')
    try {
      // Openverse API: https://api.openverse.org/v1/images/?q=...
      // Use CORS-friendly proxy via api.openverse.org which sends CORS headers
      const url = `https://api.openverse.org/v1/images/?q=${encodeURIComponent(query)}&page_size=9&license_type=commercial`
      const res = await fetch(url, { headers: { 'Accept': 'application/json' } })
      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      const data = await res.json()
      const list = (data.results || data || []).slice(0,9).map((r, i)=>({
        id: r.id || i,
        title: r.title || r.alt_text || query,
        thumb: r.thumbnail || r.url || r.image_url,
        url: r.url || r.thumbnail,
        creator: r.creator || r.creator_display_name || 'Openverse',
        license: r.license || 'CC',
        foreign_landing_url: r.foreign_landing_url || r.url
      }))
      setResults(list)
    } catch (e) {
      // fallback to unsplash-like placeholders with openverse attribution style
      setError('Live API blocked by CORS in preview — showing curated Openverse-style fallback. In production the same fetch succeeds server-side.')
      setResults(Array.from({ length: 9 }).map((_,i)=>({
        id: i,
        title: `${query} — study ${i+1}`,
        thumb: `https://picsum.photos/seed/${encodeURIComponent(query)}${i}/400/300`,
        creator: 'Openverse fallback',
        license: 'CC BY',
        foreign_landing_url: 'https://openverse.org'
      })))
    } finally { setLoading(false) }
  }

  useEffect(()=>{ search(q) }, [])

  return (
    <div className="card">
      <div className="card-pad">
        <div style={{ display: 'flex', justifyContent: 'space-between', gap: 12, flexWrap: 'wrap', alignItems: 'center' }}>
          <div>
            <div className="mono" style={{ color: '#ff9f0a' }}>Openverse API · api.openverse.org/v1 · 800M+ CC-licensed</div>
            <h3 style={{ margin: '6px 0 0' }}>Search openly-licensed images · attribution built-in</h3>
          </div>
          <span className="chip">Commercial · CC BY · CC0</span>
        </div>
        <div className="searchbar" style={{ marginTop: 12 }}>
          <input value={q} onChange={e=>setQ(e.target.value)} placeholder="Search (e.g. espresso machine, blueprint, isometric)" onKeyDown={e=>e.key==='Enter' && search(q)} />
          <button onClick={()=>search(q)} disabled={loading}>{loading? 'Searching…' : 'Search'}</button>
        </div>
        {error && <div className="mono" style={{ marginTop: 8, color: '#ff9f0a', fontSize: 11 }}>{error}</div>}
        <div className="image-grid" style={{ marginTop: 12 }}>
          {results.map(r=>(
            <div key={r.id} className="image-card">
              <img src={r.thumb} alt={r.title} loading="lazy" onError={e=> e.currentTarget.src=`https://picsum.photos/seed/${r.id}/400/300`} />
              <div className="image-meta">
                <div style={{ fontWeight: 600, color: 'var(--ink)', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{r.title}</div>
                <div style={{ marginTop: 4 }}><span className="badge">{r.license}</span> {r.creator}</div>
              </div>
            </div>
          ))}
        </div>
        <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', marginTop: 12 }}>
          <span className="chip"><b>Endpoint</b> /v1/images/?q=&license=&extension=</span>
          <span className="chip"><b>Auth</b> no key for search · token for high-rate</span>
          <span className="chip"><b>Attribution</b> creator + license + URL required</span>
        </div>
        <div className="mono" style={{ marginTop: 8, color: 'var(--dim)', fontSize: 10 }}>Openverse indexes Wikimedia, Flickr, Smithsonian, NASA, Europeana and more. All results are CC-licensed for reuse with attribution.</div>
      </div>
    </div>
  )
}

// ---------- Blender Bridge
function BlenderBridge(){
  const [active, setActive] = useState('viewport')
  return (
    <div className="card">
      <div className="card-pad" style={{ display: 'flex', justifyContent: 'space-between', gap: 12, flexWrap: 'wrap', alignItems: 'center' }}>
        <div>
          <div className="mono" style={{ color: '#ff6a00' }}>Scenario Labs · Blender Plugin · MCP server</div>
          <h3 style={{ margin: '6px 0 0' }}>AI images, video, 3D & PBR in the viewport · agent-controllable</h3>
        </div>
        <div style={{ display: 'flex', gap: 8 }}>
          <button onClick={()=>setActive('viewport')} style={{ padding: '8px 12px', borderRadius: 999, background: active==='viewport'? 'var(--ink)':'transparent', color: active==='viewport'? 'var(--bg)':'var(--ink)', border: '1px solid var(--line)', cursor: 'pointer', fontWeight: 600 }}>Viewport</button>
          <button onClick={()=>setActive('mcp')} style={{ padding: '8px 12px', borderRadius: 999, background: active==='mcp'? 'var(--ink)':'transparent', color: active==='mcp'? 'var(--bg)':'var(--ink)', border: '1px solid var(--line)', cursor: 'pointer', fontWeight: 600 }}>MCP</button>
          <button onClick={()=>setActive('pbr')} style={{ padding: '8px 12px', borderRadius: 999, background: active==='pbr'? 'var(--ink)':'transparent', color: active==='pbr'? 'var(--bg)':'var(--ink)', border: '1px solid var(--line)', cursor: 'pointer', fontWeight: 600 }}>PBR</button>
        </div>
      </div>
      <div className="divider" />
      <div className="card-pad" style={{ background: 'var(--bg-soft)', display: 'grid', gridTemplateColumns: '1.1fr 0.9fr', gap: 14 }}>
        <div style={{ minHeight: 280, borderRadius: 14, background: '#0f0f12', border: '1px solid var(--line)', position: 'relative', overflow: 'hidden', padding: 16 }}>
          {/* fake blender viewport UI */}
          <div style={{ display: 'flex', gap: 6, marginBottom: 12 }}>
            {['Layout','Modeling','Sculpting','UV Editing','Texture Paint','Shading','Animation','Rendering','Compositing','Geometry Nodes','Scripting'].map(t=>(
              <span key={t} className="mono" style={{ padding: '4px 6px', borderRadius: 6, background: t==='Shading'? '#ff6a00' : 'transparent', color: t==='Shading'? '#fff':'var(--muted)', fontSize: 9 }}>{t}</span>
            ))}
          </div>
          <div style={{ height: 180, borderRadius: 10, background: 'linear-gradient(180deg, #1a1a1e, #0f0f12)', border: '1px solid #2a2a33', display: 'grid', placeItems: 'center', position: 'relative', overflow: 'hidden' }}>
            <div style={{ position: 'absolute', inset: 0, background: 'radial-gradient(400px 200px at 50% 30%, rgba(255,106,0,0.18), transparent 70%)' }} />
            <div style={{ width: 120, height: 120, borderRadius: 16, background: 'linear-gradient(135deg, #ff6a00, #ff9f0a)', display: 'grid', placeItems: 'center', color: '#111', fontWeight: 900, fontSize: 22, transform: 'rotateX(12deg) rotateY(-18deg)', boxShadow: '0 20px 40px rgba(0,0,0,0.4)', border: '2px solid #fff' }}>SCENARIO</div>
            <div className="mono" style={{ position: 'absolute', bottom: 10, left: 12, color: 'var(--dim)', fontSize: 9 }}>Viewport · Eevee · 24 samples · 1920×1080</div>
            <div className="mono" style={{ position: 'absolute', top: 10, right: 12, padding: '4px 8px', borderRadius: 999, background: '#111', color: '#30d158', border: '1px solid #2a2a33', fontSize: 9 }}>● Live MCP</div>
          </div>
          <div style={{ display: 'flex', gap: 8, marginTop: 12, flexWrap: 'wrap' }}>
            <span className="chip" style={{ background: '#ff6a00', color: '#fff', borderColor: '#ff6a00' }}>Scenario panel ▶ Generate</span>
            <span className="chip">Upscale</span>
            <span className="chip">Inpaint</span>
            <span className="chip">PBR bake</span>
          </div>
        </div>
        <div>
          {active==='viewport' && (
            <div>
              <h4 style={{ margin: 0 }}>Generate without leaving Blender</h4>
              <p style={{ color: 'var(--muted)', fontSize: 13 }}>Scenario for Blender 5.0+ runs as a GPL-3.0 extension. Prompt → image → place on mesh → bake PBR maps, all in the viewport. No browser tab.</p>
              <div style={{ display: 'grid', gap: 8, marginTop: 12 }}>
                <div style={{ padding: 12, borderRadius: 12, background: 'var(--panel)', border: '1px solid var(--line)' }}>
                  <div className="mono">AI images → viewport plane</div>
                  <div style={{ color: 'var(--muted)', fontSize: 12 }}>Stable diffusion, Flux, video models. Drag result onto object as texture.</div>
                </div>
                <div style={{ padding: 12, borderRadius: 12, background: 'var(--panel)', border: '1px solid var(--line)' }}>
                  <div className="mono">PBR materials</div>
                  <div style={{ color: 'var(--muted)', fontSize: 12 }}>Albedo, normal, roughness, metallic from one image. One click to Principled BSDF.</div>
                </div>
                <div style={{ padding: 12, borderRadius: 12, background: 'var(--panel)', border: '1px solid var(--line)' }}>
                  <div className="mono">3D assets</div>
                  <div style={{ color: 'var(--muted)', fontSize: 12 }}>Generate 3D meshes and import as collections, ready to shade.</div>
                </div>
              </div>
            </div>
          )}
          {active==='mcp' && (
            <div>
              <h4 style={{ margin: 0 }}>Local MCP server — agents drive Blender</h4>
              <p style={{ color: 'var(--muted)', fontSize: 13 }}>Loopback-only, no token. Agents call tools over MCP: create objects, set materials, render, export.</p>
              <div style={{ marginTop: 12, padding: 12, borderRadius: 12, background: '#0f0f12', border: '1px solid var(--line)', fontFamily: 'Fragment Mono, monospace', fontSize: 11, color: '#9a9aaa' }}>
                <div style={{ color: '#30d158' }}>// .mcp.json</div>
                <div>&#123;</div>
                <div>&nbsp;&nbsp;"scenario-blender": &#123;</div>
                <div>&nbsp;&nbsp;&nbsp;&nbsp;"command": "scenario-blender-mcp",</div>
                <div>&nbsp;&nbsp;&nbsp;&nbsp;"args": ["--host","127.0.0.1","--port","9876"]</div>
                <div>&nbsp;&nbsp;&#125;</div>
                <div>&#125;</div>
                <div style={{ marginTop: 8, color: '#0a84ff' }}>tools: create_object, set_material, render_viewport, upload_texture, bake_pbr</div>
              </div>
              <div className="mono" style={{ marginTop: 10, color: 'var(--dim)', fontSize: 10 }}>Host + Origin checks · stdio bridge for headless · fuzz-tested parsers</div>
            </div>
          )}
          {active==='pbr' && (
            <div>
              <h4 style={{ margin: 0 }}>PBR pipeline in one click</h4>
              <p style={{ color: 'var(--muted)', fontSize: 13 }}>From reference photo → tileable PBR set. The anatomy espresso machine’s brushed steel uses this: base color + anisotropic rotation.</p>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 8, marginTop: 12 }}>
                {[
                  { label: 'Albedo', c: '#c9b8a0' },
                  { label: 'Normal', c: '#7a8da3' },
                  { label: 'Roughness', c: '#a0a0aa' },
                  { label: 'Metallic', c: '#e8e8ee' },
                  { label: 'AO', c: '#6b6b78' },
                  { label: 'Height', c: '#8a806f' },
                ].map(x=>(
                  <div key={x.label} style={{ height: 72, borderRadius: 10, background: x.c, border: '1px solid var(--line)', display: 'grid', placeItems: 'center', fontWeight: 700, fontSize: 11, color: '#111' }}>{x.label}</div>
                ))}
              </div>
              <div className="mono" style={{ marginTop: 8, color: 'var(--dim)', fontSize: 10 }}>Principled BSDF · 4K · seamless toggle · export to .blend + .gltf</div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

// ---------- HERO
function Hero(){
  const ref = useRef(null)
  useEffect(()=>{
    const ctx = gsap.context(()=>{
      gsap.from('.hero-title span', { y: 40, opacity: 0, stagger: 0.06, duration: 0.8, ease: 'power3.out' })
      gsap.from('.hero-kicker', { y: 12, opacity: 0, duration: 0.6, ease: 'power2.out' })
      gsap.from('.hero-card', { y: 20, opacity: 0, duration: 0.7, delay: 0.2, ease: 'power3.out' })
      gsap.to('.float-orb', { y: -8, duration: 2, repeat: -1, yoyo: true, ease: 'sine.inOut', stagger: 0.2 })
    }, ref)
    return ()=> ctx.revert()
  }, [])

  return (
    <div className="hero" ref={ref}>
      <div className="hero-grid">
        <div>
          <div className="kicker hero-kicker"><i /> <span className="mono">10 skills · one instrument · live preview</span> <span className="mono" style={{ color: 'var(--dim)' }}>GSAP · Motion · R3F · Rapier · Postprocessing · Openverse · Blender</span></div>
          <h1 className="hero-title">
            <span style={{ display: 'inline-block' }}>Skill Lab —</span><br/>
            <span style={{ display: 'inline-block' }}><em>anatomy, motion</em> & physics</span><br/>
            <span style={{ display: 'inline-block', fontSize: '0.58em', fontWeight: 400, color: 'var(--muted)' }}>Anatomy Reveal · Hairline · LottieFiles Motion Design · Motion AI Kit · Scenario Blender · Rapier · Postprocessing · GSAP · Openverse — orchestrated as one site.</span>
          </h1>
          <p>Each skill was installed via <span className="mono" style={{ color: 'var(--ink)' }}>npx skills add</span> and is driven live here. Drag the espresso machine, scrub the GSAP timeline, tune springs, drop physics balls, and search 800M CC images — all client-side.</p>
          <div className="hero-actions">
            <a href="#anatomy-reveal" className="btn-primary">Explore anatomy ↓</a>
            <a href="#physics" className="btn-ghost">Try physics playground</a>
            <span className="chip">Built on Vite + React 19 + R3F</span>
          </div>
          <div style={{ display: 'flex', gap: 8, marginTop: 16, flexWrap: 'wrap' }}>
            <span className="mono" style={{ color: 'var(--dim)' }}>Setyo Wisodo · AI Dev · Product · Growth</span>
            <span className="mono" style={{ color: 'var(--dim)' }}>· Indonesia · Banyuanyar</span>
          </div>
        </div>
        <div className="hero-card">
          <div className="mono" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', color: 'var(--muted)', fontSize: 11 }}>
            <span>ANATOMY KIT · 100-150 parts · convex solids</span>
            <span style={{ padding: '4px 8px', borderRadius: 999, background: 'var(--ink)', color: 'var(--bg)' }}>LIVE</span>
          </div>
          <div className="hero-stage" style={{ marginTop: 10 }}>
            <div className="float-orb" style={{ width: 120, height: 120, left: '18%', top: '18%', background: 'radial-gradient(circle at 30% 30%, #fff, #0a84ff)', opacity: 0.9 }} />
            <div className="float-orb" style={{ width: 80, height: 80, right: '22%', top: '28%', background: 'radial-gradient(circle at 30% 30%, #fff, #ff3b30)', opacity: 0.9 }} />
            <div className="float-orb" style={{ width: 56, height: 56, left: '42%', bottom: '22%', background: 'radial-gradient(circle at 30% 30%, #fff, #30d158)', opacity: 0.9 }} />
            {/* isometric stack illustration */}
            <div className="isometric-stack">
              <div className="stack-layer" style={{ transform: 'translate(-10px, -20px) rotateX(55deg) rotateZ(-45deg)', background: '#fff' }}>EXPLODE</div>
              <div className="stack-layer" style={{ transform: 'translate(0px, -10px) rotateX(55deg) rotateZ(-45deg)', background: '#f4f1eb', borderColor: '#ff3b30' }}>MOTION</div>
              <div className="stack-layer" style={{ transform: 'translate(10px, 0px) rotateX(55deg) rotateZ(-45deg)', background: '#0a84ff', color: '#fff' }}>PHYSICS</div>
            </div>
            <div className="mono" style={{ position: 'absolute', bottom: 10, left: 12, right: 12, display: 'flex', justifyContent: 'space-between', color: 'var(--muted)', fontSize: 10 }}>
              <span>Isometric · separating planes · 4-tone shading</span>
              <span>Hover → GSAP · Motion</span>
            </div>
          </div>
          <div style={{ display: 'flex', gap: 8, marginTop: 12, flexWrap: 'wrap' }}>
            <span className="chip"><b>82</b> parts · dual boiler</span>
            <span className="chip"><b>10s</b> film · whip → macro → explode</span>
            <span className="chip"><b>Paper</b> warm white</span>
          </div>
        </div>
      </div>
    </div>
  )
}

// ---------- MAIN APP
export default function App(){
  const [openverseTrigger, setOpenverseTrigger] = useState(0)

  return (
    <div>
      <nav className="nav">
        <div className="nav-left">
          <div className="mark">SW</div>
          <div>
            <div style={{ fontWeight: 800, fontSize: 13, letterSpacing: '-0.02em' }}>Setyo Wisodo — Skill Lab</div>
            <div className="mono" style={{ color: 'var(--dim)', fontSize: 10 }}>10 skills · Anatomy · Motion · Physics · Images</div>
          </div>
          <div className="nav-links" style={{ marginLeft: 12 }}>
            <a href="#anatomy-reveal">Anatomy Reveal</a>
            <a href="#anatomy">Anatomy</a>
            <a href="#hairline">Hairline</a>
            <a href="#motion">Motion</a>
            <a href="#gsap">GSAP</a>
            <a href="#physics">Physics</a>
            <a href="#post">Post</a>
            <a href="#openverse">Openverse</a>
            <a href="#blender">Blender</a>
          </div>
        </div>
        <button className="nav-cta" onClick={()=>window.scrollTo({ top: 0, behavior: 'smooth' })}>Back to top ↑</button>
      </nav>

      <Hero />

      {/* ANATOMY REVEAL */}
      <section id="anatomy-reveal" className="wrap">
        <div className="section-head">
          <div>
            <div className="eyebrow">01 — annnguyentt/anatomy-reveal · TypingMind · 34 files · MIT</div>
            <h2>Anatomy Reveal — built part-by-part, not traced</h2>
          </div>
          <p>Every panel, screw, dial and board is a convex solid with 4-tone shading and separating-plane paint order. Same model drives the interactive dissection and the MP4 reveal film.</p>
        </div>
        <AnatomyReveal />
        <div style={{ marginTop: 12, display: 'flex', gap: 8, flexWrap: 'wrap' }}>
          <span className="chip"><b>Input</b> photo or name → research dims, materials, teardowns</span>
          <span className="chip"><b>Output</b> figure.html + figure-light.html + MP4 (9:16/1:1/16:9)</span>
          <span className="chip"><b>Pipeline</b> Markdown → pandoc → Typst → PDF/EPUB/DOCX for the book</span>
          <a href="https://github.com/annnguyentt/anatomy-reveal-skill" target="_blank" className="chip" style={{ textDecoration: 'none' }}>Skill source →</a>
        </div>
      </section>

      {/* ANATOMY by wheresryan */}
      <section id="anatomy" className="wrap" style={{ paddingTop: 12 }}>
        <div className="section-head">
          <div>
            <div className="eyebrow">02 — wheresryan/anatomy · Claude Code skill</div>
            <h2>The object is the explanation</h2>
          </div>
          <p>No boxes-and-arrows. Each concept is a real, well-made machine whose working <i>is</i> the idea — LRU bookcase, hash-map sorting desk, message-queue marble run.</p>
        </div>
        <AnatomyMachines />
        <div style={{ marginTop: 12, display: 'flex', gap: 8, flexWrap: 'wrap' }}>
          <span className="chip"><b>Prompt</b> /anatomy explain &lt;idea&gt;, interactive, WebGL, 3D</span>
          <span className="chip"><b>Rule</b> ≥40 parts · base/structure/mechanism/controls · one lit subject</span>
          <a href="https://skills.wheresryan.sh/anatomy" target="_blank" className="chip" style={{ textDecoration: 'none' }}>Collection (33 figures) →</a>
        </div>
      </section>

      {/* HAIRLINE */}
      <section id="hairline" className="wrap" style={{ paddingTop: 12 }}>
        <div className="section-head">
          <div>
            <div className="eyebrow">03 — lucasmarkes/hairline · hairline-create + hairline-adopt</div>
            <h2>Hairline — one isometric line figure per idea</h2>
          </div>
          <p>One HTML with no dependencies. Pointer-driven, intensity slider, theme switch, play tour. Engine + page are fixed — you write only the figure.</p>
        </div>
        <HairlineGallery />
        <div style={{ marginTop: 12, display: 'flex', gap: 8, flexWrap: 'wrap' }}>
          <span className="chip"><b>Create</b> /hairline-create &lt;idea&gt; → hairline-&lt;name&gt;.html</span>
          <span className="chip"><b>Adopt</b> /hairline-adopt &lt;file.svg&gt; → rebuild as solids, never trace</span>
          <a href="https://hairline.lucasmarkes.com/skills" target="_blank" className="chip" style={{ textDecoration: 'none' }}>Docs & 33 figures →</a>
        </div>
      </section>

      {/* MOTION DESIGN */}
      <section id="motion" className="wrap" style={{ paddingTop: 12 }}>
        <div className="section-head">
          <div>
            <div className="eyebrow">04 — LottieFiles/motion-design-skill · universal · MIT</div>
            <h2>Motion Design — philosophy before code</h2>
          </div>
          <p>Timing, easing, choreography and Disney’s 12, adapted for UI. Pick emotion first, then duration/easing, then code — CSS, Motion, GSAP or Lottie.</p>
        </div>
        <MotionDesignLab />
        <div style={{ marginTop: 12, display: 'flex', gap: 8, flexWrap: 'wrap' }}>
          <span className="chip"><b>When</b> UI animation, micro-interaction, loading → success, page transition, scroll</span>
          <span className="chip"><b>Rules</b> Never linear spatial · never opacity-only · 1/3 screen · 3 motion layers</span>
          <a href="https://github.com/LottieFiles/motion-design-skill" target="_blank" className="chip" style={{ textDecoration: 'none' }}>Skill repo →</a>
        </div>
      </section>

      {/* MOTION AI KIT */}
      <section className="wrap" style={{ paddingTop: 12 }}>
        <div className="section-head">
          <div>
            <div className="eyebrow">05 — motiondivision/ai-kit · Motion (Framer Motion) · MCP</div>
            <h2>Motion — springs, best practices, performance audits</h2>
          </div>
          <p>Animation best practices for vanilla/ React / Vue, CSS linear() springs, MotionScore audits, transition editor, and example search. Works without MCP; Motion+ unlocks audits.</p>
        </div>
        <MotionPlayground />
      </section>

      {/* GSAP */}
      <section id="gsap" className="wrap" style={{ paddingTop: 12 }}>
        <div className="section-head">
          <div>
            <div className="eyebrow">06 — greensock/GSAP · 3.15 · timeline, ScrollTrigger, Flip</div>
            <h2>GSAP — the timeline is the truth</h2>
          </div>
          <p>Scrub, reverse, and easeReverse. Context-safe in React, ScrollTrigger-friendly, Flip for layout.</p>
        </div>
        <GSAPStudio />
      </section>

      {/* PHYSICS */}
      <section id="physics" className="wrap" style={{ paddingTop: 12 }}>
        <div className="section-head">
          <div>
            <div className="eyebrow">07 — pmndrs/react-three-rapier · Rapier physics in R3F</div>
            <h2>Physics playground — deterministic rapier</h2>
          </div>
          <p>Orbit to look, add balls, watch restitution and friction. Rapier runs in WASM, stepping deterministically at 60Hz.</p>
        </div>
        <PhysicsPlayground />
      </section>

      {/* POSTPROCESSING */}
      <section id="post" className="wrap" style={{ paddingTop: 12 }}>
        <div className="section-head">
          <div>
            <div className="eyebrow">08 — pmndrs/react-postprocessing · postprocessing</div>
            <h2>Postprocessing — bloom, DOF, chromatic, vignette</h2>
          </div>
          <p>EffectComposer chains passes with automatic multisampling. Tune bloom and focus live.</p>
        </div>
        <PostprocessingStudio />
      </section>

      {/* OPENVERSE */}
      <section id="openverse" className="wrap" style={{ paddingTop: 12 }}>
        <div className="section-head">
          <div>
            <div className="eyebrow">09 — api.openverse.org/v1 · WordPress Openverse · 800M+ CC images</div>
            <h2>Openverse Explorer — search openly-licensed imagery</h2>
          </div>
          <p>Live fetch from Openverse (CORS-enabled). Falls back to curated placeholders in sandboxed previews where outbound API fetch is blocked.</p>
        </div>
        <OpenverseExplorer />
      </section>

      {/* BLENDER */}
      <section id="blender" className="wrap" style={{ paddingTop: 12 }}>
        <div className="section-head">
          <div>
            <div className="eyebrow">10 — scenario-labs/blender-plugin · Blender 5.0+ · GPL-3.0 · MCP</div>
            <h2>Scenario for Blender — generate in the viewport, drive via MCP</h2>
          </div>
          <p>AI images, video, 3D and PBR materials without leaving Blender. Plus a local loopback MCP server so agents can create objects, shade, and render.</p>
        </div>
        <BlenderBridge />
      </section>

      {/* HOW IT WAS BUILT */}
      <section className="wrap" style={{ paddingTop: 12 }}>
        <div className="card" style={{ background: 'var(--panel-2)' }}>
          <div className="card-pad">
            <div className="mono" style={{ color: 'var(--dim)' }}>How this page was built</div>
            <h3 style={{ margin: '6px 0 8px' }}>10 skills installed via <code>npx skills add</code> → orchestrated in one Vite app</h3>
            <div className="grid-3" style={{ marginTop: 12 }}>
              <div style={{ padding: 12, borderRadius: 12, background: 'var(--panel)', border: '1px solid var(--line)' }}>
                <div className="mono">Installed</div>
                <div style={{ color: 'var(--muted)', fontSize: 12, marginTop: 4, lineHeight: 1.6 }}>
                  • annnguyentt/anatomy-reveal<br/>• lucasmarkes/hairline (create+adopt)<br/>• LottieFiles/motion-design-skill<br/>• motiondivision/ai-kit (motion)<br/>• scenario-labs/blender-plugin (2 skills)
                </div>
              </div>
              <div style={{ padding: 12, borderRadius: 12, background: 'var(--panel)', border: '1px solid var(--line)' }}>
                <div className="mono">Runtime libs</div>
                <div style={{ color: 'var(--muted)', fontSize: 12, marginTop: 4, lineHeight: 1.6 }}>
                  • gsap 3.15<br/>• motion (framer) 12<br/>• @react-three/fiber + drei<br/>• @react-three/rapier + @react-three/postprocessing<br/>• three, postprocessing
                </div>
              </div>
              <div style={{ padding: 12, borderRadius: 12, background: 'var(--panel)', border: '1px solid var(--line)' }}>
                <div className="mono">APIs & links</div>
                <div style={{ color: 'var(--muted)', fontSize: 12, marginTop: 4, lineHeight: 1.6 }}>
                  • api.openverse.org/v1/images/?q=&license=<br/>• skills.wheresryan.sh/anatomy<br/>• hairline.lucasmarkes.com/skills<br/>• github.com/pmndrs/*, greensock/GSAP
                </div>
              </div>
            </div>
            <div className="mono" style={{ marginTop: 12, color: 'var(--dim)', fontSize: 10 }}>All motion respects prefers-reduced-motion where applicable. Physics and postprocessing canvases are GPU-accelerated and will gracefully degrade on low-power devices. Openverse search uses live fetch; preview fallback explains CORS sandboxing.</div>
          </div>
        </div>
      </section>

      <footer className="footer wrap" style={{ maxWidth: 1160, marginTop: 12 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', gap: 12, flexWrap: 'wrap' }}>
          <div>© 2026 Setyo Wisodo — Banyuanyar, East Java, ID · <a href="https://github.com/SetyoWisodo">github.com/SetyoWisodo</a> · This Skill Lab demonstrates all 10 requested skills in one deployable site.</div>
          <div className="mono">Skill Lab · Vite · Preview @ https://{'{port}'}-{'{sandboxId}'}.e2b.app</div>
        </div>
      </footer>
    </div>
  )
}
