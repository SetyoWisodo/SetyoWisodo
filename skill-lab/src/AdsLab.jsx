import { useState, useMemo } from 'react'
import { motion, AnimatePresence } from 'motion/react'

const platforms = [
  { id:'google', label:'Google Ads', mark:'G', color:'#4285F4', accent:'#0a84ff' },
  { id:'meta', label:'Meta Ads', mark:'M', color:'#0668E1', accent:'#0081FB' },
  { id:'youtube', label:'YouTube Ads', mark:'YT', color:'#FF0000', accent:'#ff3b30' },
  { id:'linkedin', label:'LinkedIn Ads', mark:'IN', color:'#0077B5', accent:'#0077B5' },
  { id:'tiktok', label:'TikTok Ads', mark:'TT', color:'#000000', accent:'#00f2ea' },
  { id:'microsoft', label:'Microsoft', mark:'MS', color:'#ffb900', accent:'#f25022' },
  { id:'apple', label:'Apple Ads', mark:'Ap', color:'#000000', accent:'#555555' },
  { id:'amazon', label:'Amazon Ads', mark:'Am', color:'#FF9900', accent:'#febd69' },
  { id:'reddit', label:'Reddit Ads', mark:'RD', color:'#FF4500', accent:'#ff4500' },
  { id:'pinterest', label:'Pinterest', mark:'Pi', color:'#E60023', accent:'#e60023' },
  { id:'snapchat', label:'Snapchat', mark:'SC', color:'#FFFC00', accent:'#fffc00' },
  { id:'x', label:'X Ads', mark:'X', color:'#000000', accent:'#1d9bf0' },
]

const mockSetup = {
  business_model:'B2B SaaS — project management tool',
  industry:'Software',
  geography:'US + EU',
  regulated:false,
  objective:'Lower CAC while scaling trials',
  conversion:'Free trial → paid (14d), value $420',
  attribution:'GA4 + Meta CAPI, 30/90d windows',
  monthly_spend: 48000,
  per_platform: { google:18000, meta:14000, linkedin:8000, tiktok:5000, youtube:3000 },
  account_age:'18 months',
  pixel_history:'Meta Pixel 14d cold-start (new domain), GA4 18m, gtag 12m',
  data_source:'CSV export (2026-08-01 → 2026-09-30, UTC, USD)',
}

const mockAudit = {
  run_id:'ads-20261025-9f3a',
  bundle_version:'2.0.0',
  status:'provisional', // complete | provisional | partial | insufficient_evidence
  coverage: 74,
  platform_results: platforms.map((p,i)=>({
    platform:p.id,
    status: i<8 ? (['pass','pass','fail','pass','fail','unknown','pass','pass'][i] || 'pass') : (i===9?'unknown':'not_applicable'),
    coverage: [92,84,68,88,55,72,90,82,61,44,79,58][i],
    findings: [
      { control_id:`${p.id.toUpperCase()}-MEAS-01`, status: i%3===0?'fail':'pass', confidence: i%3===0?'high':'medium', evidence:[{kind:'account_export', ref:'input:conversions'}], observation:'Conversion window mismatch: GA4 30d vs Meta 7d click', diagnosis:'Double-counting risk', recommendation:'Align windows to primary conversion; add cross-platform dedup table' },
      { control_id:`${p.id.toUpperCase()}-BUDG-02`, status: i%2===0?'pass':'fail', confidence:'high', evidence:[{kind:'account_export', ref:'input:budgets'}], observation:`Spend ${mockSetup.per_platform[p.id] ? '$'+mockSetup.per_platform[p.id] : 'n/a'} vs pacing ${i%2===0?'on track':'behind 22%'}`, diagnosis: i%2===0?'Pacing healthy':'Under-delivery', recommendation: i%2===0?'Hold bidding':'Raise budget ceiling or loosen targeting' },
      { control_id:`${p.id.toUpperCase()}-CREAT-03`, status:'unknown', confidence:'low', evidence:[{kind:'missing_inputs', ref:'creative fatigue'}], observation:'No creative fatigue signal in export', diagnosis:'Cannot judge creative freshness', recommendation:'Provide asset age + impressions per creative' },
    ],
    disabled_health:true,
  })),
  cross_platform: [
    { domain:'measurement', findings:[{ control_id:'X-MEAS-01', status:'fail', confidence:'high', observation:'Conversion totals differ: GA4 1,240 vs platform sum 1,880 (+52%)', diagnosis:'No cross-platform total; vendor double-count', recommendation:'Publish one cross-platform conversion total; GA4 as source of truth' }] },
    { domain:'creative', findings:[{ control_id:'X-CREA-02', status:'pass', confidence:'medium', observation:'12 active creatives, 3 aging >45d', diagnosis:'Mild fatigue risk', recommendation:'Rotate 2 creatives; add UGC variant' }] },
  ],
  evidence_policy:'Official API > account export > dated practitioner > community (license-checked). Load-bearing claims require source_id + retrieval_date + confidence + refresh_due. Stale blocks release-current.',
  completeness:'provisional: all required workers ok, but 3 platforms 60-79% coverage',
}

function CoverageBadge({ v }){
  const level = v>=80 ? 'graded' : v>=60 ? 'provisional' : 'insufficient'
  const color = v>=80 ? '#30d158' : v>=60 ? '#ff9f0a' : '#ff3b30'
  return <span className="mono" style={{ padding:'2px 8px', borderRadius:999, background:`color-mix(in srgb, ${color} 14%, transparent)`, color, border:`1px solid ${color}`, fontSize:10 }}>{level} · {v}%</span>
}
function StatusDot({ status }){
  const map = { pass:'#30d158', fail:'#ff3b30', unknown:'#ff9f0a', not_applicable:'#6e6e7a' }
  return <span className="mono" style={{ padding:'2px 8px', borderRadius:999, background: map[status] || '#6e6e7a', color:'#fff', fontSize:10 }}>{status}</span>
}

export default function AdsLab(){
  const [tab, setTab] = useState('setup') // setup | audit | report | monitor | optimize | cockpit
  const [selectedPlat, setSelectedPlat] = useState('google')
  const [auditRun, setAuditRun] = useState(false)
  const [applyCeilings, setApplyCeilings] = useState(false)
  const [drift, setDrift] = useState(null)

  const selected = useMemo(()=> mockAudit.platform_results.find(p=>p.platform===selectedPlat) || mockAudit.platform_results[0], [selectedPlat])

  return (
    <div className="card">
      <div className="card-pad" style={{ display:'flex', justifyContent:'space-between', gap:12, flexWrap:'wrap', alignItems:'center' }}>
        <div>
          <div className="mono" style={{ color:'#4285F4' }}>AgriciDaniel/claude-ads · Claude-first paid-media ops · 12 platforms · 34 skills · v2.1.0 · development candidate</div>
          <h3 style={{ margin:'6px 0 0' }}>Paid-Media Operations Cockpit — source-grounded audits, deterministic findings, versioned JSON</h3>
          <div className="mono" style={{ color:'var(--muted)', marginTop:6 }}>12 account-health scoring profiles disabled → audits report <b style={{color:'var(--ink)'}}>findings + unknowns + coverage</b>, not health scores. All 110 endpoints stay read-only until mutation gate passes.</div>
        </div>
        <div style={{ display:'flex', gap:6, flexWrap:'wrap' }}>
          <span className="mono" style={{ padding:'6px 10px', borderRadius:999, background:'#ff3b30', color:'#fff' }}>Status: development candidate</span>
          <span className="mono" style={{ padding:'6px 10px', borderRadius:999, background:'var(--panel-2)', border:'1px solid var(--line)' }}>Bundle {mockAudit.bundle_version} · Run {mockAudit.run_id}</span>
        </div>
      </div>

      <div style={{ padding:'0 16px 12px', display:'flex', gap:6, flexWrap:'wrap', borderBottom:'1px solid var(--line)' }}>
        {[
          { id:'setup', label:'/ads setup', icon:'⚙️' },
          { id:'audit', label:'/ads audit', icon:'🔍' },
          { id:'report', label:'/ads report', icon:'📄' },
          { id:'monitor', label:'/ads monitor', icon:'📡' },
          { id:'optimize', label:'/ads optimize', icon:'🚀' },
          { id:'cockpit', label:'/ads cockpit', icon:'🛰️' },
        ].map(t=>(
          <button key={t.id} onClick={()=>setTab(t.id)} style={{
            padding:'8px 12px', borderRadius:999, border:'1px solid var(--line)', background: tab===t.id ? 'var(--ink)' : 'var(--panel)', color: tab===t.id ? 'var(--bg)' : 'var(--muted)', cursor:'pointer', fontWeight: tab===t.id?700:500, fontSize:12
          }}>{t.icon} {t.label}</button>
        ))}
        <span className="mono" style={{ color:'var(--dim)', marginLeft:6, alignSelf:'center' }}>Commands route 1:1 to skills — one owner per trigger · untrusted-data rule enforced</span>
      </div>

      {/* platform rail */}
      <div style={{ padding:'12px 16px', display:'flex', gap:8, flexWrap:'wrap', alignItems:'center', background:'var(--bg-soft)', borderBottom:'1px solid var(--line)' }}>
        <span className="mono" style={{ color:'var(--dim)' }}>12 platforms:</span>
        {platforms.map(p=>(
          <button key={p.id} onClick={()=>{ setSelectedPlat(p.id); setTab('audit')}} style={{
            padding:'6px 10px', borderRadius:999, border:'1px solid var(--line)', background: selectedPlat===p.id ? p.color : 'var(--panel)', color: selectedPlat===p.id ? '#fff' : 'var(--ink)', cursor:'pointer', fontWeight:600, fontSize:11, display:'flex', alignItems:'center', gap:6
          }}>
            <span style={{ width:18, height:18, borderRadius:'50%', background:'#fff', color:'#111', display:'grid', placeItems:'center', fontSize:10, fontWeight:800 }}>{p.mark}</span>
            {p.label}
          </button>
        ))}
        <span className="mono" style={{ color:'var(--dim)' }}>YouTube reported separately even when Google supplies data</span>
      </div>

      <div style={{ padding:16, minHeight:420, background:'var(--bg)' }}>
        {tab==='setup' && (
          <div style={{ display:'grid', gridTemplateColumns:'1.2fr 0.8fr', gap:12 }}>
            <div style={{ padding:14, borderRadius:14, background:'var(--panel)', border:'1px solid var(--line)' }}>
              <div className="mono" style={{ color:'var(--dim)' }}>Setup profile — never stores secrets · credential ref only</div>
              <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:10, marginTop:10, fontSize:12 }}>
                <Field label="Business model" value={mockSetup.business_model} />
                <Field label="Objective + conversion" value={mockSetup.objective + ' · ' + mockSetup.conversion} />
                <Field label="Monthly spend" value={`$${mockSetup.monthly_spend.toLocaleString()} · ${Object.entries(mockSetup.per_platform).map(([k,v])=> `${k} $${v}`).join(' · ')}`} />
                <Field label="Geography" value={mockSetup.geography} />
                <Field label="Account age / Pixel" value={`${mockSetup.account_age} · ${mockSetup.pixel_history}`} />
                <Field label="Attribution" value={mockSetup.attribution} />
                <Field label="Data source" value={mockSetup.data_source} />
                <Field label="Credential refs" value={'{configured:true, source:environment, secret_ref:META_API_TOKEN} · never in repo/profile/logs'} mono />
              </div>
              <div style={{ marginTop:12, padding:10, borderRadius:10, background:'var(--bg-soft)', border:'1px solid var(--line)', fontFamily:'Fragment Mono, monospace', fontSize:11, color:'#9a9aaa' }}>
                <div style={{ color:'#30d158' }}>Run manifest (created before analysis)</div>
                <div>{`{ run_id:"${mockAudit.run_id}", bundle_version:"${mockAudit.bundle_version}", window:"2026-08-01→2026-09-30", currency:"USD", timezone:"UTC", platforms:[${platforms.slice(0,4).map(p=>'"'+p.id+'"').join(',')}], data_source:"CSV export", classification:"operational", retention:"30d or exception" }`}</div>
              </div>
              <div style={{ marginTop:10, display:'flex', gap:8, flexWrap:'wrap' }}>
                <span className="chip"><b>Refs</b> ads/setup → ads/references/google-audit.md, gaql-notes.md</span>
                <span className="chip"><b>Safety</b> missing ceilings = no write · deletion not supported in v2</span>
              </div>
            </div>
            <div style={{ padding:14, borderRadius:14, background:'var(--panel)', border:'1px solid var(--line)' }}>
              <div className="mono">Lifecycle · data-lifecycle.json</div>
              <div style={{ marginTop:10, display:'grid', gap:8 }}>
                {[
                  { k:'Purpose + retention', v:'Ops audit only · 30d auto-delete or documented exception' },
                  { k:'At-rest / in-transit', v:'AES-256 at rest · TLS 1.2+ · evidence: verify with tool results' },
                  { k:'Owner / roles', v:'Ops lead (owner) · analyst (read) · approver (approve)' },
                  { k:'Deletion / verify', v:'Shred + audit destination · rollback window documented' },
                  { k:'Incident', v:'Owner: privacy@ · channel: #ads-incidents' },
                ].map(r=>(
                  <div key={r.k} style={{ padding:'8px 10px', borderRadius:10, background:'var(--bg-soft)', border:'1px solid var(--line)', fontSize:12 }}>
                    <div className="mono" style={{ color:'var(--dim)', fontSize:10 }}>{r.k}</div>
                    <div style={{ marginTop:2, color:'var(--ink)' }}>{r.v}</div>
                  </div>
                ))}
              </div>
              <div className="mono" style={{ marginTop:10, color:'var(--dim)', fontSize:10 }}>Operational contract, not legal advice. Secret values in env/keychain/secret manager — never in profile, report, or log.</div>
            </div>
          </div>
        )}

        {tab==='audit' && (
          <div>
            <div style={{ display:'flex', gap:8, flexWrap:'wrap', alignItems:'center', marginBottom:12 }}>
              <button onClick={()=>setAuditRun(v=>!v)} style={{ padding:'10px 14px', borderRadius:999, background: auditRun?'var(--line)':'var(--ink)', color: auditRun?'var(--muted)':'var(--bg)', border:0, fontWeight:700, cursor:'pointer' }}>{auditRun ? '✓ Audit dispatched (conductor + 12 workers)' : 'Run /ads audit all → dispatch 12 workers'}</button>
              <span className="mono" style={{ color:'var(--dim)' }}>Deterministic scoring (not prompt) · workers return schema-valid JSON · conductor aggregates</span>
              <span className="mono" style={{ padding:'4px 8px', borderRadius:999, background: auditRun? '#ff9f0a' : 'var(--line)', color:'#fff' }}>{auditRun ? mockAudit.status : 'idle'}</span>
              <CoverageBadge v={mockAudit.coverage} />
              <span className="mono" style={{ color:'var(--muted)' }}>Coverage: 80%+ graded · 60-79% provisional · &lt;60% insufficient</span>
            </div>

            <div style={{ display:'grid', gridTemplateColumns:'0.9fr 1.1fr', gap:12 }}>
              <div style={{ padding:12, borderRadius:14, background:'var(--panel)', border:'1px solid var(--line)' }}>
                <div className="mono" style={{ color:'var(--dim)' }}>Platform result — {selected.platform.toUpperCase()} · {platforms.find(p=>p.id===selected.platform)?.label}</div>
                <div style={{ display:'flex', gap:8, alignItems:'center', marginTop:8 }}>
                  <StatusDot status={selected.status} />
                  <CoverageBadge v={selected.coverage} />
                  <span className="mono" style={{ color:'var(--dim)', fontSize:10 }}>health: null (profile disabled) · scoring 0% until policy approved</span>
                </div>
                <div style={{ height:6, borderRadius:999, background:'var(--line)', marginTop:10, overflow:'hidden' }}><i style={{ display:'block', height:'100%', width:`${selected.coverage}%`, background:selected.coverage>=80?'#30d158':selected.coverage>=60?'#ff9f0a':'#ff3b30' }} /></div>
                <div style={{ marginTop:12, display:'grid', gap:8 }}>
                  {selected.findings.map(f=>(
                    <div key={f.control_id} style={{ padding:10, borderRadius:10, background:'var(--bg-soft)', border:'1px solid var(--line)' }}>
                      <div style={{ display:'flex', gap:6, alignItems:'center', flexWrap:'wrap' }}>
                        <span className="mono" style={{ padding:'2px 6px', borderRadius:6, background:'var(--panel)', border:'1px solid var(--line)', fontSize:10 }}>{f.control_id}</span>
                        <StatusDot status={f.status} />
                        <span className="mono" style={{ color:'var(--dim)', fontSize:10 }}>confidence {f.confidence}</span>
                      </div>
                      <div style={{ marginTop:6, fontSize:12, color:'var(--ink)' }}><b>Obs:</b> {f.observation}</div>
                      <div style={{ fontSize:12, color:'var(--muted)' }}><b>Dx:</b> {f.diagnosis} · <b>Fix:</b> {f.recommendation}</div>
                      <div className="mono" style={{ color:'var(--dim)', fontSize:10, marginTop:4 }}>evidence: {f.evidence.map(e=>`${e.kind}:${e.ref}`).join(' · ')} · source_classification: evidence_based · confidence: {f.confidence}</div>
                    </div>
                  ))}
                </div>
                <div className="mono" style={{ marginTop:10, color:'var(--dim)', fontSize:10 }}>No `result`/`severity`/`evidence_refs` shortcuts — every envelope validated against audit-worker-result v1. Optional/beta/premium stay unscored.</div>
              </div>

              <div style={{ padding:12, borderRadius:14, background:'var(--panel)', border:'1px solid var(--line)' }}>
                <div className="mono">Completeness + evidence policy</div>
                <div style={{ marginTop:10, display:'grid', gap:8 }}>
                  <div style={{ padding:10, borderRadius:10, background:'var(--bg-soft)', border:'1px solid var(--line)' }}>
                    <div className="mono" style={{ color:'var(--dim)' }}>Run completeness</div>
                    <div style={{ marginTop:4, fontSize:12, color:'var(--ink)' }}><b>{mockAudit.completeness}</b> — {mockAudit.cross_platform.length} cross-platform domains · 12 platform workers · required-worker failure → partial (weight renormalized, stale weight never reused)</div>
                  </div>
                  <div style={{ padding:10, borderRadius:10, background:'var(--bg-soft)', border:'1px solid var(--line)' }}>
                    <div className="mono" style={{ color:'var(--dim)' }}>Cross-platform systemic</div>
                    {mockAudit.cross_platform.map(c=>(
                      <div key={c.domain} style={{ marginTop:6, fontSize:12, color:'var(--muted)' }}><b style={{color:'var(--ink)', textTransform:'capitalize'}}>{c.domain}:</b> {c.findings[0].observation} → {c.findings[0].recommendation}</div>
                    ))}
                  </div>
                  <div style={{ padding:10, borderRadius:10, background:'#0f0f12', border:'1px solid var(--line)', fontFamily:'Fragment Mono, monospace', fontSize:11, color:'#9a9aaa' }}>
                    <div style={{ color:'#30d158' }}>// audit-worker-result v1 (one per platform)</div>
                    <div>{`{ schema_version:"1.0.0", platform:"${selected.platform}", status:"${selected.status}", findings:[…], missing_inputs:[…], stale_sources:[], recovery_hints:[…] }`}</div>
                    <div style={{ marginTop:6, color:'#ff9f0a' }}>Evidence: official API {'>'} export {'>'} dated practitioner {'>'} community · stale blocks release-current until reverified</div>
                  </div>
                </div>
              </div>
            </div>

            <div style={{ marginTop:12, display:'grid', gridTemplateColumns:'repeat(3, 1fr)', gap:12 }}>
              {[
                { title:'Evidence coverage', desc:`Portfolio ${mockAudit.coverage}% provisional — 3 platforms 60-79% (creative fatigue, tracking)`, hint:'Provide asset age + pixel history to lift to graded' },
                { title:'Regulatory exposure', desc:'EU AI Act Art.50 (transparency) — no AI disclosure in ad copy detected (low confidence)', hint:'Review control-plane/compliance.md before claiming' },
                { title:'Opportunities (unscored)', desc:'Beta: Meta Advantage+ Shopping (unavailable in EU for this objective) → unscored_opportunity', hint:'Do not penalize health for unavailable beta' },
              ].map(c=>(
                <div key={c.title} style={{ padding:12, borderRadius:12, background:'var(--panel)', border:'1px solid var(--line)' }}>
                  <div className="mono">{c.title}</div>
                  <div style={{ marginTop:6, fontSize:12, color:'var(--muted)' }}>{c.desc}</div>
                  <div className="mono" style={{ marginTop:8, color:'var(--dim)', fontSize:10 }}>{c.hint}</div>
                </div>
              ))}
            </div>
          </div>
        )}

        {tab==='report' && (
          <div style={{ display:'grid', gridTemplateColumns:'1.1fr 0.9fr', gap:12 }}>
            <div style={{ padding:14, borderRadius:14, background:'var(--panel)', border:'1px solid var(--line)' }}>
              <div className="mono">Rendered report — from canonical JSON bundle (never prose-only)</div>
              <div style={{ marginTop:10, padding:12, borderRadius:12, background:'var(--bg-soft)', border:'1px solid var(--line)', fontSize:12, lineHeight:1.7, color:'var(--muted)' }}>
                <div style={{ fontWeight:800, color:'var(--ink)' }}>Paid-Media Audit — {mockSetup.business_model} — 2026-08-01→2026-09-30 (UTC, USD)</div>
                <div style={{ marginTop:6 }}>Run <code>{mockAudit.run_id}</code> · bundle <code>{mockAudit.bundle_version}</code> · status <b style={{color:'#ff9f0a'}}>{mockAudit.status}</b> · coverage {mockAudit.coverage}% provisional.</div>
                <div style={{ marginTop:8 }}>No health scores — 12 profiles disabled. Findings: 18 pass, 9 fail, 7 unknown, 6 not_applicable. See evidence table.</div>
                <div style={{ marginTop:8 }}><b style={{color:'var(--ink)'}}>Top fails:</b> conversion window mismatch (+52% double-count), Meta Pixel cold-start 14d, under-delivery on LinkedIn (−22%). <b style={{color:'var(--ink)'}}>Next:</b> <code>/ads next</code> → align windows + add dedup table (owner: Ops, due in 7d, rollback: revert windows).</div>
                <div style={{ marginTop:8, fontFamily:'Fragment Mono, monospace', fontSize:11, color:'var(--dim)' }}>Sources: Meta Marketing API v26.0 (retrieved 2026-10-12), Google Ads developer-token sunset (2026-07-12), LinkedIn 202511 due 2026-11-16 — each with source_id + refresh_due. Stale blocks release-current.</div>
              </div>
              <div style={{ display:'flex', gap:8, marginTop:12, flexWrap:'wrap' }}>
                <span className="chip"><b>Versions</b> JSON canonical → Markdown/HTML/PDF renderings</span>
                <span className="chip"><b>Verify</b> bundle completeness, citations, privacy</span>
                <span className="chip"><b>Command</b> /ads report {mockAudit.run_id}</span>
              </div>
            </div>
            <div style={{ padding:12, borderRadius:14, background:'#0f0f12', border:'1px solid var(--line)', fontFamily:'Fragment Mono, monospace', fontSize:11, color:'#9a9aaa' }}>
              <div style={{ color:'#30d158' }}>// versioned bundle (excerpt)</div>
              <div>{`{ run_id:"${mockAudit.run_id}", bundle_version:"${mockAudit.bundle_version}", status:"${mockAudit.status}", coverage:${mockAudit.coverage}, platforms:[`}</div>
              {mockAudit.platform_results.slice(0,2).map(p=>(
                <div key={p.platform} style={{ paddingLeft:12 }}>{`  { platform:"${p.platform}", status:"${p.status}", coverage:${p.coverage}, findings:[…] },`}</div>
              ))}
              <div>{`  ], cross_platform:[…], evidence_policy:"source_id+retrieved+confidence+refresh_due", completeness:"${mockAudit.completeness}" }`}</div>
              <div style={{ marginTop:10, color:'#ff9f0a' }}>Render with current registry; reject fabricated health or incompatible history — regenerate via current registry.</div>
              <div style={{ marginTop:8, display:'flex', gap:8 }}>
                <button onClick={()=>setDrift(drift? null : { msg:'No drift — bundle validates against claude_ads_core/scoring.py' })} style={{ padding:'6px 10px', borderRadius:999, background:'var(--panel)', border:'1px solid var(--line)', color:'var(--ink)', fontSize:11, cursor:'pointer' }}>{drift ? 'Hide validate' : 'Validate bundle'}</button>
                <span className="mono" style={{ color:'var(--dim)', alignSelf:'center' }}>{drift?.msg || 'Python: claude_ads_core --version · validate finding path/to/finding.json'}</span>
              </div>
            </div>
          </div>
        )}

        {tab==='monitor' && (
          <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:12 }}>
            <div style={{ padding:14, borderRadius:14, background:'var(--panel)', border:'1px solid var(--line)' }}>
              <div className="mono">Monitor — pacing, delivery, fatigue, tracking, policy</div>
              <div style={{ marginTop:10, display:'grid', gap:8 }}>
                {[
                  { k:'Pacing', v:'LinkedIn under-delivery −22% (last 7d) → behind', color:'#ff9f0a', action:'Raise budget ceiling or loosen geo; check dayparting' },
                  { k:'Delivery', v:'Meta Pixel cold-start 14d → 0 convs last 3d', color:'#ff3b30', action:'Add CAPI + dedup; verify event match quality' },
                  { k:'Fatigue', v:'3 creatives >45d, frequency 4.2 (Meta) → mild fatigue', color:'#ff9f0a', action:'Rotate UGC variant; schedule refresh in 7d' },
                  { k:'Policy', v:'No policy flags; X Ads brand-safety eligible (US)', color:'#30d158', action:'Continue; review policy refs weekly' },
                ].map(r=>(
                  <div key={r.k} style={{ padding:10, borderRadius:10, background:'var(--bg-soft)', border:'1px solid var(--line)', display:'flex', gap:10, alignItems:'center' }}>
                    <span style={{ width:8, height:8, borderRadius:'50%', background:r.color, flex:'none' }} />
                    <div style={{ flex:1 }}>
                      <div style={{ fontWeight:700, fontSize:12 }}>{r.k}</div>
                      <div className="mono" style={{ color:'var(--muted)', fontSize:11 }}>{r.v}</div>
                      <div className="chip" style={{ marginTop:6, fontSize:10 }}><b>Next</b> {r.action}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
            <div style={{ padding:14, borderRadius:14, background:'var(--panel)', border:'1px solid var(--line)' }}>
              <div className="mono">Health (disabled) vs evidence</div>
              <div style={{ marginTop:10, padding:12, borderRadius:12, background:'var(--bg-soft)', border:'1px solid var(--line)', fontSize:12, lineHeight:1.6, color:'var(--muted)' }}>
                <div><b style={{color:'var(--ink)'}}>Health scores:</b> null for all 12 platforms — production profiles remain disabled (needs severity + weight policy + independent verification). Do not invent scores.</div>
                <div style={{ marginTop:6 }}><b style={{color:'var(--ink)'}}>Evidence coverage:</b> {mockAudit.coverage}% provisional. Unknown controls reduce coverage without changing known health. Withhold portfolio health rather than invent weights when defensible weights unavailable.</div>
                <div style={{ marginTop:8, display:'flex', gap:6, flexWrap:'wrap' }}>
                  <span className="chip"><b>Complete</b> ≥80% graded</span>
                  <span className="chip"><b>Provisional</b> 60-79%</span>
                  <span className="chip"><b>Insufficient</b> &lt;60%</span>
                </div>
              </div>
              <div style={{ marginTop:10, fontFamily:'Fragment Mono, monospace', fontSize:11, color:'var(--dim)' }}>Command: <code>/ads monitor</code> — checks pacing, delivery, tracking, fatigue, policy. See ads-monitor + ads-monitor references.</div>
            </div>
          </div>
        )}

        {tab==='optimize' && (
          <div style={{ display:'grid', gridTemplateColumns:'1.1fr 0.9fr', gap:12 }}>
            <div style={{ padding:14, borderRadius:14, background:'var(--panel)', border:'1px solid var(--line)' }}>
              <div className="mono">Optimize — capability-gated, drafts by default</div>
              <div style={{ marginTop:10, display:'grid', gap:8 }}>
                {[
                  { id:'GOOG-BID-01', title:'Align conversion windows + dedup table', blast:'All platforms · reporting', before:'GA4 30d vs Meta 7d → sum 1,880', after:'Single total 1,240 (GA4 truth) + dedup', ceilings:'ops-approve ≤ $0 spend' },
                  { id:'META-TRK-02', title:'Add Meta CAPI with deduplication', blast:'Meta only · tracking', before:'Pixel cold-start 14d · 0 convs', after:'CAPI + event match quality ≥ 7.0', ceilings:'dev-key + tracking-approve' },
                ].map(op=>(
                  <div key={op.id} style={{ padding:12, borderRadius:12, background:'var(--bg-soft)', border:'1px solid var(--line)' }}>
                    <div style={{ display:'flex', gap:8, alignItems:'center' }}>
                      <span className="mono" style={{ padding:'2px 6px', borderRadius:6, background:'var(--panel)', border:'1px solid var(--line)', fontSize:10 }}>{op.id}</span>
                      <span style={{ fontWeight:700, fontSize:13 }}>{op.title}</span>
                      <span className="mono" style={{ color:'var(--dim)', fontSize:10 }}>blast: {op.blast}</span>
                    </div>
                    <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:8, marginTop:8, fontSize:11 }}>
                      <div><span className="mono" style={{ color:'var(--dim)' }}>Before</span><div style={{ marginTop:2, color:'var(--muted)' }}>{op.before}</div></div>
                      <div><span className="mono" style={{ color:'var(--dim)' }}>After</span><div style={{ marginTop:2, color:'var(--ink)' }}>{op.after}</div></div>
                    </div>
                    <div className="mono" style={{ marginTop:8, color:'var(--dim)', fontSize:10 }}>Ceilings: {op.ceilings} · idempotency: ads-optimize:{op.id}:{mockAudit.run_id} · verify: remote state == precondition · rollback: revert window</div>
                  </div>
                ))}
              </div>
              <div style={{ marginTop:12, display:'flex', gap:8, alignItems:'center', flexWrap:'wrap' }}>
                <label className="mono" style={{ display:'flex', alignItems:'center', gap:8, padding:'6px 10px', borderRadius:999, border:'1px solid var(--line)', background:'var(--panel-2)', cursor:'pointer' }}>
                  <input type="checkbox" checked={applyCeilings} onChange={e=>setApplyCeilings(e.target.checked)} />
                  I have explicit account+object IDs, ceilings, and owner approval
                </label>
                <button disabled={!applyCeilings} style={{ padding:'8px 12px', borderRadius:999, background: applyCeilings?'var(--ink)':'var(--line)', color: applyCeilings?'var(--bg)':'var(--muted)', border:0, fontWeight:700, fontSize:12, cursor: applyCeilings?'pointer':'not-allowed' }}>
                  {applyCeilings ? '/ads optimize --apply (gated)' : '/ads optimize --draft (safe)'}
                </button>
                <span className="mono" style={{ color:'var(--dim)', fontSize:10 }}>Missing ceilings → no write · deletion not supported in v2 · verify via tool before claiming complete</span>
              </div>
            </div>
            <div style={{ padding:14, borderRadius:14, background:'var(--panel)', border:'1px solid var(--line)' }}>
              <div className="mono">Mutation gate (6 checks)</div>
              <ol style={{ margin:'10px 0 0', paddingLeft:16, fontSize:12, lineHeight:1.7, color:'var(--muted)' }}>
                <li>Tested capability for exact operation</li>
                <li>Explicit account + object IDs</li>
                <li>Before/after diff + blast radius</li>
                <li>Owner approval within ceilings</li>
                <li>Idempotency + audit destination + rollback + verification window</li>
                <li>Precondition still holds on remote</li>
              </ol>
              <div style={{ marginTop:12, padding:10, borderRadius:10, background:'#0f0f12', border:'1px solid var(--line)', fontFamily:'Fragment Mono, monospace', fontSize:11, color:'#9a9aaa' }}>
                <div style={{ color:'#30d158' }}>// capability manifest (excerpt)</div>
                <div>{`{ operation:"pause_campaign", enabled:true, tested:true, approver_required:true, ceilings:{ daily_budget: 500 } }`}</div>
                <div style={{ marginTop:6, color:'#ff9f0a' }}>No manifest → no capability claim. No approval/rollback → no mutation.</div>
              </div>
            </div>
          </div>
        )}

        {tab==='cockpit' && (
          <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:12 }}>
            <div style={{ padding:14, borderRadius:14, background:'var(--panel)', border:'1px solid var(--line)' }}>
              <div className="mono">Cockpit — optional companion (not selected by main skill until requested)</div>
              <div style={{ marginTop:10, display:'grid', gap:8 }}>
                <div style={{ padding:10, borderRadius:10, background:'var(--bg-soft)', border:'1px solid var(--line)', fontSize:12, color:'var(--muted)' }}>Cockpit lives in <code>mods/claude-ads-cockpit</code> + <code>claude_ads_core.cockpit</code> — Overview, Checks, Inputs, Compare, Reports panes (no scroll, paged j/u, filtered f). Actions limited to validate-input, validate-run, render-report, bound to snapshot fingerprint — never writes into lifecycle-restricted run.</div>
                <div style={{ padding:10, borderRadius:10, background:'#0f0f12', border:'1px solid var(--line)', fontFamily:'Fragment Mono, monospace', fontSize:11, color:'#9a9aaa' }}>
                  <div style={{ color:'#30d158' }}>cockpit CLI</div>
                  <div>cockpit doctor → snapshot → compare → action → demo</div>
                  <div>claude_ads_core.cockpit.publish() → canonical artifacts only, at workflow boundaries</div>
                </div>
                <div className="mono" style={{ color:'var(--dim)', fontSize:10 }}>All scoring profiles stay disabled in Cockpit. No health score, no account write. See docs/cockpit/compatibility.md + control-plane/COCKPIT.md.</div>
              </div>
            </div>
            <div style={{ padding:14, borderRadius:14, background:'var(--panel)', border:'1px solid var(--line)' }}>
              <div className="mono">Why it’s a development candidate</div>
              <div style={{ marginTop:10, padding:12, borderRadius:12, background:'var(--bg-soft)', border:'1px solid var(--line)', fontSize:12, lineHeight:1.6, color:'var(--muted)' }}>
                <div><b style={{color:'#ff3b30'}}>Not release-ready</b> until every gate in <code>control-plane/RELEASE_REQUIREMENTS.md</code> passes fresh.</div>
                <div style={{ marginTop:6 }}>All 12 health profiles disabled · Cockpit not natively accepted · Account changes drafts only · Evidence ledger requires dated source_id + retrieval/confidence/refresh_due.</div>
                <div style={{ marginTop:8, display:'flex', gap:6, flexWrap:'wrap' }}>
                  <span className="mono" style={{ padding:'4px 8px', borderRadius:999, background:'var(--line)', color:'var(--muted)' }}>Python 3.11/3.12 · 817 tests · glibc 2.28</span>
                  <span className="mono" style={{ padding:'4px 8px', borderRadius:999, background:'var(--line)', color:'var(--muted)' }}>ShellCheck + pip check + advisory audit</span>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      <div style={{ padding:'12px 16px', borderTop:'1px solid var(--line)', display:'flex', gap:8, flexWrap:'wrap', justifyContent:'space-between', alignItems:'center' }}>
        <div className="mono" style={{ color:'var(--dim)' }}>Source-grounded audits · deterministic findings · versioned JSON → Markdown/HTML/PDF · evidence coverage disclosed · private incident owner/channel required. See <a href="https://github.com/AgriciDaniel/claude-ads" target="_blank" style={{ color:'var(--ink)' }}>AgriciDaniel/claude-ads</a> + control-plane/RELEASE_REQUIREMENTS.md</div>
        <a href="https://github.com/AgriciDaniel/claude-ads#quickstart" target="_blank" style={{ padding:'8px 12px', borderRadius:999, background:'var(--ink)', color:'var(--bg)', textDecoration:'none', fontWeight:700, fontSize:12 }}>/ads setup → audit → report → next</a>
      </div>
    </div>
  )
}

function Field({ label, value, mono }){
  return <div style={{ padding:'8px 10px', borderRadius:10, background:'var(--bg-soft)', border:'1px solid var(--line)' }}>
    <div className="mono" style={{ color:'var(--dim)', fontSize:10 }}>{label}</div>
    <div style={{ marginTop:2, fontSize:12, color:'var(--ink)', fontFamily: mono ? 'Fragment Mono, monospace' : undefined, lineHeight:1.4 }}>{value}</div>
  </div>
}
