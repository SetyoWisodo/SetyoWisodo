import { useMemo, useState } from 'react'
import { motion, AnimatePresence } from 'motion/react'

/* Studio Anomali v2 — prototype interaktif (data MOCK, bukan data live).
   Sumber rancangan: PROJECT_STUDIO_ANOMALI_v2_NASIONAL_CLIPPER.md
   Ganti mock → data nyata saat SCRAPECREATORS_API_KEY tersedia. */

const niches = {
  bakso: { label:'Bakso (kuliner)', city:'Malang', baseViews: 42000 },
  batik: { label:'Batik tulis (fashion)', city:'Banyuwangi', baseViews: 31000 },
  kopi:  { label:'Kopi lokal', city:'Jember', baseViews: 27000 },
  lele:  { label:'Lele (kuliner)', city:'Banyuanyar', baseViews: 58000 },
  keripik:{label:'Keripik (oleh-oleh)', city:'Malang', baseViews: 19000 },
}

const outliersFor = (n) => [
  { mult:'20×', views: n.baseViews*20, hook:'"Jujur, harga segini belum pernah aku lihat di Malang"', format:'Talking head 0:23 + close-up produk', why:'Angka konkret + kejutan di 3 detik pertama' },
  { mult:'5×',  views: n.baseViews*5,  hook:'"Aku coba 3 warung, cuma satu yang ini"',               format:'Montase warung + voice-over', why:'Perbandingan dan rasa penasaran' },
  { mult:'3×',  views: n.baseViews*3,  hook:'"Kenapa orang Jatim beli ini tiap Minggu?"',            format:'Pertanyaan + jawaban di 0:08', why:'Pertanyaan sebagai judul, cocok untuk search' },
]

const transcript = [
  { t:'0:00', text:'Tiga warung, satu yang bikin aku balik lagi.', claim:'Pengalaman pribadi (opini)', quote:true },
  { t:'0:23', text:'Kuahnya dimasak dari tulang sejak subuh.', claim:'Proses — perlu bukti (video dapur)', quote:false },
  { t:'1:02', text:'Harga Rp15.000 untuk porsi besar.', claim:'Harga — konkret, mudah diverifikasi', quote:true },
]

const comments = [
  { type:'questions', text:'Buka jam berapa?', likes: 210 },
  { type:'pain', text:'Sering habis kalau siang, susah dapet', likes: 145 },
  { type:'requests', text:'Bisa bikin video cara masaknya?', likes: 93 },
  { type:'controversy', text:'Ah ini mah bukan asli, kurang rasa tradisional', likes: 38 },
  { type:'buying', text:'Minta template caption order dong', likes: 61 },
]

const trends = [
  { label:'Anomali + hipdut lokal', impact:86, src:'mock — referensi riset induk' },
  { label:'Raw UGC > polished', impact:88, src:'mock — referensi riset induk' },
  { label:'Nano creator 10K–100K', impact:82, src:'mock — referensi riset induk' },
  { label:'Search-friendly judul (pertanyaan)', impact:74, src:'mock — referensi riset induk' },
]

const creators = [
  { name:'@dapurmalang.id', city:'Malang', followers: 38000, er: 8.1, fit: 91, rate: 'Rp1,5 jt', rateIdr: 1500000, commission:'15%' },
  { name:'@banyuwangikain', city:'Banyuwangi', followers: 22000, er: 9.4, fit: 88, rate: 'Rp1 jt', rateIdr: 1000000, commission:'12%' },
  { name:'@jemberkopi', city:'Jember', followers: 61000, er: 5.2, fit: 79, rate: 'Rp2,5 jt', rateIdr: 2500000, commission:'15%' },
  { name:'@lelebanyuanyar', city:'Banyuanyar', followers: 12000, er: 11.0, fit: 94, rate: 'Rp600 rb', rateIdr: 600000, commission:'18%' },
  { name:'@surabaya.jajan', city:'Surabaya', followers: 84000, er: 3.1, fit: 62, rate: 'Rp3 jt', rateIdr: 3000000, commission:'10%' },
  { name:'@sego.tempong.id', city:'Surabaya', followers: 19000, er: 7.6, fit: 84, rate: 'Rp900 rb', rateIdr: 900000, commission:'15%' },
]

const cpa = { TikTok: 18.94, Google: 27.36, Meta: 38.33 }   // dari riset induk (RESEARCH_SOCIAL_MEDIA_PROJECT_POTENTIAL_2026.md)

const atoms = ['TikTok 9:16','Reels','Shorts','Carousel','Thread X','WA Status','Email','Iklan 15 dtk']

const tabs = [
  { id:'radar', label:'Radar Outlier' },
  { id:'hook', label:'Hook Transkrip' },
  { id:'voc', label:'VOC Komentar' },
  { id:'trend', label:'Trend' },
  { id:'creator', label:'Nano Matcher' },
  { id:'ads', label:'Simulator Ads' },
  { id:'calendar', label:'Kalender 8 Atom' },
]

const fmt = (n) => n.toLocaleString('id-ID')

export default function AnomalyStudio(){
  const [tab, setTab] = useState('radar')
  const [niche, setNiche] = useState('lele')
  const [pick, setPick] = useState(null)
  const [budget, setBudget] = useState(300)
  const [split, setSplit] = useState({ TikTok: 60, Meta: 25, Google: 15 })
  const [picked, setPicked] = useState([])
  const n = niches[niche]
  const outliers = useMemo(() => outliersFor(n), [niche])

  const splitTotal = Object.values(split).reduce((a,b)=>a+b,0)
  const cpaBlend = (Object.entries(split).reduce((a,[k,v]) => a + cpa[k]*v, 0) / (splitTotal||1))
  const conversions = Math.floor(budget / cpaBlend)

  const toggleCreator = (name) => setPicked(p => p.includes(name) ? p.filter(x=>x!==name) : [...p, name])

  return (
    <div>
      <div style={{ display:'flex', gap:8, flexWrap:'wrap', marginBottom:14 }}>
        {tabs.map(t => (
          <button key={t.id} onClick={()=>setTab(t.id)}
            style={{ padding:'8px 14px', borderRadius:999, border:'1px solid #d2d2d7', cursor:'pointer',
              background: tab===t.id ? '#1d1d1f' : '#fff', color: tab===t.id ? '#fff' : '#1d1d1f', fontWeight:600 }}>
            {t.label}
          </button>
        ))}
      </div>
      <div style={{ fontSize:12, color:'#86868b', marginBottom:12 }}>Data MOCK untuk prototipe. Angka CPA dari riset induk; sisanya ilustrasi.</div>

      <AnimatePresence mode="wait">
        <motion.div key={tab} initial={{ opacity:0, y:8 }} animate={{ opacity:1, y:0 }} exit={{ opacity:0, y:-8 }} transition={{ duration:0.2 }}>

          {tab==='radar' && (
            <div>
              <div style={{ display:'flex', gap:8, flexWrap:'wrap', marginBottom:12 }}>
                {Object.entries(niches).map(([k,v]) => (
                  <button key={k} onClick={()=>setNiche(k)}
                    style={{ padding:'6px 12px', borderRadius:8, border:'1px solid #d2d2d7', cursor:'pointer',
                      background: niche===k ? '#0a84ff' : '#fff', color: niche===k ? '#fff' : '#1d1d1f' }}>
                    {v.label}
                  </button>
                ))}
              </div>
              <div style={{ fontSize:13, color:'#6e6e73', marginBottom:10 }}>Niche <b>{n.label}</b> · basis {fmt(n.baseViews)} views (median mock) · kota fokus {n.city}</div>
              {outliers.map(o => (
                <div key={o.mult} style={{ border:'1px solid #e5e5ea', borderRadius:12, padding:14, marginBottom:10 }}>
                  <div style={{ display:'flex', justifyContent:'space-between' }}>
                    <b style={{ color:'#ff3b30' }}>{o.mult} median</b><span>{fmt(o.views)} views</span>
                  </div>
                  <div style={{ marginTop:6 }}>{o.hook}</div>
                  <div style={{ fontSize:13, color:'#6e6e73', marginTop:4 }}>Format: {o.format} · Kenapa: {o.why}</div>
                </div>
              ))}
              <div style={{ fontSize:12, color:'#86868b' }}>Skill: outlier-post-finder (median-baseline, 3 outlier teratas)</div>
            </div>
          )}

          {tab==='hook' && (
            <div>
              {transcript.map(row => (
                <div key={row.t} style={{ display:'grid', gridTemplateColumns:'60px 1fr 220px', gap:10, padding:'10px 0', borderBottom:'1px solid #f0f0f5' }}>
                  <code>{row.t}</code>
                  <span>{row.text}</span>
                  <span style={{ fontSize:12, color: row.quote ? '#30d158' : '#ff9f0a' }}>{row.claim}</span>
                </div>
              ))}
              <div style={{ fontSize:13, color:'#6e6e73', marginTop:10 }}>Kalimat "perlu bukti" harus dibuktikan dengan rekaman di video sebelum dipakai di iklan. Skill: transcript-intelligence.</div>
            </div>
          )}

          {tab==='voc' && (
            <div>
              {['questions','pain','requests','buying','controversy'].map(type => (
                <div key={type} style={{ marginBottom:10 }}>
                  <b style={{ textTransform:'capitalize' }}>{type}</b>
                  {comments.filter(c=>c.type===type).map(c => (
                    <div key={c.text} style={{ display:'flex', justifyContent:'space-between', padding:'6px 10px', background:'#f5f5f7', borderRadius:8, marginTop:4 }}>
                      <span>"{c.text}"</span><span style={{ color:'#6e6e73' }}>{c.likes} likes</span>
                    </div>
                  ))}
                </div>
              ))}
              <div style={{ fontSize:13, color:'#6e6e73' }}>Komentar "buying" dan "requests" jadi ide video berikutnya. Skill: comment-mining.</div>
            </div>
          )}

          {tab==='trend' && (
            <div>
              {trends.map(t => (
                <div key={t.label} style={{ marginBottom:12 }}>
                  <div style={{ display:'flex', justifyContent:'space-between' }}><b>{t.label}</b><span>{t.impact}/100</span></div>
                  <div style={{ height:8, background:'#f0f0f5', borderRadius:4, marginTop:4 }}>
                    <div style={{ width:`${t.impact}%`, height:'100%', background:'#0a84ff', borderRadius:4 }} />
                  </div>
                  <div style={{ fontSize:12, color:'#86868b', marginTop:2 }}>{t.src}</div>
                </div>
              ))}
              <div style={{ fontSize:13, color:'#6e6e73' }}>Skill: trend-discovery, social-listening-brief.</div>
            </div>
          )}

          {tab==='creator' && (
            <div>
              <div style={{ overflowX:'auto' }}>
                <table style={{ width:'100%', borderCollapse:'collapse', fontSize:14 }}>
                  <thead><tr style={{ textAlign:'left', color:'#6e6e73' }}>
                    <th></th><th>Creator</th><th>Kota</th><th>Followers</th><th>ER</th><th>Fit</th><th>Tarif</th><th>Komisi</th>
                  </tr></thead>
                  <tbody>
                    {creators.map(c => (
                      <tr key={c.name} style={{ borderTop:'1px solid #f0f0f5' }}>
                        <td><input type="checkbox" checked={picked.includes(c.name)} onChange={()=>toggleCreator(c.name)} /></td>
                        <td><b>{c.name}</b></td><td>{c.city}</td><td>{fmt(c.followers)}</td><td>{c.er}%</td>
                        <td>{c.fit}</td><td>{c.rate}</td><td>{c.commission}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              <div style={{ marginTop:12, padding:12, background:'#f5f5f7', borderRadius:10 }}>
                {picked.length===0 ? 'Centang creator untuk membuat brief kolaborasi.' :
                  <>Brief untuk <b>{picked.length}</b> creator: {picked.join(', ')} — tarif gabungan estimasi Rp{fmt(picked.reduce((a,nm)=>a+creators.find(x=>x.name===nm).rateIdr,0))}</>}
              </div>
              <div style={{ fontSize:12, color:'#86868b', marginTop:8 }}>Skill: influencer-prospecting, creator-profile-teardown. Tarif = mock.</div>
            </div>
          )}

          {tab==='ads' && (
            <div>
              <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:16 }}>
                <div>
                  <label>Budget per bulan: <b>${budget}</b></label>
                  <input type="range" min={100} max={2000} step={50} value={budget} onChange={e=>setBudget(+e.target.value)} style={{ width:'100%' }} />
                  {Object.keys(split).map(k => (
                    <div key={k} style={{ marginTop:10 }}>
                      <label>{k}: <b>{split[k]}%</b> (CPA ${cpa[k]})</label>
                      <input type="range" min={0} max={100} value={split[k]} onChange={e=>setSplit({...split, [k]:+e.target.value})} style={{ width:'100%' }} />
                    </div>
                  ))}
                  {splitTotal!==100 && <div style={{ color:'#ff3b30', fontSize:12 }}>Total split {splitTotal}% — idealnya 100%.</div>}
                </div>
                <div style={{ padding:14, background:'#f5f5f7', borderRadius:12 }}>
                  <div>CPA gabungan: <b>${cpaBlend.toFixed(2)}</b></div>
                  <div>Estimasi konversi: <b>{fmt(conversions)}</b> / bulan</div>
                  <div style={{ fontSize:12, color:'#6e6e73', marginTop:8 }}>Perhitungan sederhana: budget ÷ CPA gabungan. Bukan prediksi; belum memperhitungkan fatigue atau musim.</div>
                </div>
              </div>
              <div style={{ fontSize:12, color:'#86868b', marginTop:10 }}>Skill: ads-budget, ads-math, ads-plan. Sumber CPA: riset induk.</div>
            </div>
          )}

          {tab==='calendar' && (
            <div>
              <div style={{ display:'flex', flexWrap:'wrap', gap:8 }}>
                {atoms.map(a => (
                  <div key={a} style={{ padding:'10px 14px', border:'1px solid #d2d2d7', borderRadius:10, minWidth:130 }}>
                    <b>{a}</b>
                    <div style={{ fontSize:12, color:'#6e6e73' }}>Dari 1 sesi shoot</div>
                  </div>
                ))}
              </div>
              <div style={{ fontSize:13, color:'#6e6e73', marginTop:10 }}>Satu sesi rekam menghasilkan 8 bentuk konten. Skill: content-repurposing.</div>
            </div>
          )}

        </motion.div>
      </AnimatePresence>
    </div>
  )
}
