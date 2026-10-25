import { useState, useMemo, useRef, useEffect } from 'react'
import { motion, AnimatePresence } from 'motion/react'

// helpers
const fmtNum = (n) => n >= 1e6 ? (n/1e6).toFixed(1)+'M' : n >= 1e3 ? (n/1e3).toFixed(1)+'k' : String(n)
const fmtMoney = (n) => '$' + n.toLocaleString()
const clamp = (v,a,b)=> Math.max(a, Math.min(b,v))

// Mock data generators
const mockOutliers = [
  { id:1, platform:'YouTube Shorts', title:'I tried the $0 marketing hack that banks don’t want you to know', url:'https://youtube.com/shorts/abc1', views: 842000, median: 42000, likes: 41200, comments: 892, lift: 20.0, hook:'Shock + promise gap (“banks don’t want you to know”)', format:'Facecam + captions', why:'Authority challenge + tangible $0 hook' },
  { id:2, platform:'TikTok', title:'POV: your client says “make it pop” for the 10th time', url:'https://tiktok.com/@starterstory/video/123', views: 210000, median: 38000, likes: 18900, comments: 1240, lift: 5.5, hook:'Relatable pain + punchline', format:'Skits + on-screen text', why:'High comment debate → shares' },
  { id:3, platform:'Instagram Reels', title:'3 ad angles that print money (steal this)', url:'https://instagram.com/reel/xyz', views: 156000, median: 52000, likes: 8200, comments: 430, lift: 3.0, hook:'List + steal framing', format:'Carousel → Reel repurpose', why:'Saveable + actionable' },
  { id:4, platform:'YouTube', title:'Founder tear-down: why StarterStory works', url:'https://youtube.com/watch?v=aaa', views: 98000, median: 41000, likes: 3200, comments: 210, lift: 2.4, hook:'Teardown framing', format:'Talking head + B-roll', why:'Authority + community proof' },
]

const mockComments = [
  { text:'Wait does this actually work for B2B or just DTC?', likes: 42, buckets:['questions','confusion'], author:'@mira_builds' },
  { text:'Tried this last week, got 3x saves but no sales — what am I missing?', likes: 81, buckets:['pain','objection'], author:'@founder_joe' },
  { text:'Please make a template for this!', likes: 93, buckets:['requests','buying intent'], author:'@notion_fan' },
  { text:'This is just survivorship bias lol', likes: 12, buckets:['controversy'], author:'@skeptic99' },
  { text:'Where do you find outliers without paying $200/mo?', likes: 67, buckets:['questions','pain'], author:'@indiehacker' },
  { text:'OMG the hook at 0:03 hit so hard', likes: 29, buckets:['praise'], author:'@content_king' },
]

const mockTranscripts = [
  { at:'0:00', hook:true, text:'If your next video flops, it’s not the algorithm — it’s this one sentence you’re missing.' , claims:['hook controls 70% of watch time'], quotes:['it’s this one sentence'] },
  { at:'0:23', hook:false, text:'Here’s the angle: banks don’t want you to know your CAC is refundable if you do this…', claims:['CAC refundable angle'], quotes:['banks don’t want you to know'] },
  { at:'1:02', hook:false, text:'We tested this on 14 brands. 9 saw lift in 7 days.', claims:['9/14 brands lift'], quotes:['tested on 14 brands'] },
]

const mockCompetitors = [
  { name:'rival1.co', handle:'@rival1', followers: 124000, posts: 8, medianViews: 28000, topViews: 210000, pillars:['Founder story','Meme skits','Teardowns'], gap:'No carousel → reel repurposing, weak CTAs' },
  { name:'Brand B', handle:'@brand_b', followers: 89000, posts: 6, medianViews: 42000, topViews: 156000, pillars:['Ads library','How-tos','Client wins'], gap:'Over-indexed on talking head, no controversy' },
  { name:'StarterStory', handle:'@starterstory', followers: 142000, posts: 12, medianViews: 41000, topViews: 842000, pillars:['Outliers','Hooks','Playbooks'], gap:'Opportunity: ad library teardown series' },
]

const mockAds = [
  { platform:'Meta', copy:'Steal our 3 ad angles that print money — free teardown inside', hook:'Steal framing + curiosity gap', cta:'Download', offer:'Free teardown PDF', spend:'Active 14 days', url:'https://facebook.com/ads/library/123' },
  { platform:'Google', copy:'Find outliers in 10 seconds — no $200/mo tool', hook:'Job-to-be-done + price anchor', cta:'Start free', offer:'7-day trial', spend:'Search: “outlier finder”', url:'https://ads.google.com/...' },
  { platform:'LinkedIn', copy:'We mined 2,400 comments to find why B2B buyers hesitate', hook:'Data proof + B2B pains', cta:'Get report', offer:'VOC report', spend:'Sponsored: B2B founders', url:'https://linkedin.com/ads/...' },
]

const mockTrends = [
  { trend:'“POV: client says make it pop” skits', platform:'TikTok, Reels', evidence:'4 posts >5x baseline in VOC comments', why:'Relatable client pain → shares', angle:'Record founder + client actor, on-screen text' },
  { trend:'Bank/“they don’t want you to know” hooks', platform:'YouTube Shorts', evidence:'842k views (20x median)', why:'Authority challenge + promise gap', angle:'Steal hook: “banks don’t want you to know X”' },
  { trend:'Carousel → Reel repurpose', platform:'Instagram', evidence:'156k views (3x median), high saves', why:'Saveable + double distribution', angle:'Post carousel, repost as Reel next day' },
]

const mockProspects = [
  { creator:'@indiehacker_jane', followers: 82000, niche:'Indie hackers', fit: 92, reason:'Mentions “outlier” 4×, posts founder teardowns', outreach:'DM: “Loved your “make it pop” skit — want the outlier sheet we used for @starterstory?”' },
  { creator:'@b2b_content_joe', followers: 45000, niche:'B2B content', fit: 84, reason:'Mining comments for pains weekly', outreach:'Comment + DM with VOC report sample' },
  { creator:'@ads_teardown_mia', followers: 112000, niche:'Paid ads', fit: 88, reason:'Runs ad library breakdowns', outreach:'Collab: ad library teardown swap' },
]

const mockAudience = [
  { segment:'Indie hackers / bootstrapped', size:'~42%', confidence:'high', signals:['Bio: “founder” 38%', 'Eng: skits + teardowns 2.3x baseline', 'Top comment: “template please”'] },
  { segment:'B2B founders (US)', size:'~28%', confidence:'medium', signals:['Geo: US 61%', 'Eng: “B2B vs DTC?” questions', 'Meta ad click: 14d active'] },
  { segment:'Content operators', size:'~18%', confidence:'high', signals:['Shares > saves on how-tos', 'Saves on carousel→reel posts'] },
]

const mockListening = [
  { theme:'“Template please” / “steal this”', mentions: 42, sentiment:'positive', example:'“Please make a template for this!” — 93 likes', action:'Create swipe file + “steal” language in CTAs' },
  { theme:'B2B vs DTC gap', mentions: 27, sentiment:'neutral', example:'“Does this work for B2B or just DTC?”', action:'Make B2B-specific outlier report angle' },
  { theme:'$200/mo tool pain', mentions: 19, sentiment:'negative', example:'“Where do you find outliers without paying $200/mo?”', action:'Use price anchor: “no $200/mo tool”' },
]

const mockDemand = [
  { pain:'“Tried X, got saves but no sales”', freq: 14, intent:'buying', opp:'Create “saves → sales” conversion teardown', language:'“got 3x saves but no sales”' },
  { pain:'“Find outliers without paying”', freq: 19, intent:'high', opp:'Position: free/cheap outlier finder', language:'“without paying $200/mo”' },
  { pain:'“What hook at 0:03?”', freq: 8, intent:'medium', opp:'Timestamped hook library', language:'“hook at 0:03 hit so hard”' },
]

const mockCreator = {
  handle:'@starterstory', followers:142000, bio:'Founder stories + teardowns. Outliers > vanity metrics.', positioning:'Authority via founder-proof + actionable teardowns', pillars:['Outlier posts','Hook library','Playbooks (steal this)','Founder stories'], outliers: mockOutliers.slice(0,2), playbook:['Hook = promise gap + authority challenge','Format = facecam + captions (0:00-0:03 hook)','CTA = “steal this” → save','Repurpose: carousel → Reel next day'] 
}

const mockRepurpose = [
  { source:'YouTube: “I tried the $0 marketing hack” (842k views)', linkedin:'Founder Lesson: The sentence banks don’t want you to know — and how we tested it on 14 brands → thread ↓', xThread:['Hook controls 70% of watch time — here’s the one sentence you’re missing (video) →','We tested on 14 brands. 9 saw lift in 7 days. Thread of what worked →','Steal the hook: “banks don’t want you to know X” — 3 examples →'], newsletter:'This week: 3 ad angles that print money (with swipe file)', script:'[0:00] If your next video flops, it’s not the algorithm — [beat] it’s this sentence…' },
]

export default function SocialLab(){
  const [skill, setSkill] = useState('outlier-post-finder')
  const [platform, setPlatform] = useState('YouTube Shorts')
  const [handle, setHandle] = useState('@starterstory')
  const [scope, setScope] = useState('20 posts · median baseline')
  const [liveMode, setLiveMode] = useState(false)
  const [apiKey, setApiKey] = useState('')
  const [showKey, setShowKey] = useState(false)
  const [copied, setCopied] = useState(false)
  const [running, setRunning] = useState(false)
  const [done, setDone] = useState(true)

  const skills = [
    { id:'outlier-post-finder', label:'Outlier Finder', icon:'🚀', desc:'Beat baseline, not just views', endpoint:'/v1/youtube/channel/shorts + median' },
    { id:'transcript-intelligence', label:'Transcripts', icon:'🎙️', desc:'Hooks, claims, quotes', endpoint:'/v1/youtube/video/transcript + /v1/tiktok/video/transcript' },
    { id:'comment-mining', label:'Comment Mining', icon:'💬', desc:'VOC: pains, objections, intents', endpoint:'/v1/youtube/video/comments + /v1/tiktok/video/comments' },
    { id:'competitor-social-research', label:'Competitors', icon:'⚔️', desc:'Pillars, gaps, benchmarks', endpoint:'/v1/linkedin/company + /v1/youtube/channel-videos' },
    { id:'ad-library-teardown', label:'Ad Teardown', icon:'📣', desc:'Hooks, offers, CTAs', endpoint:'/v1/meta/ads + /v1/google/ads + /v1/linkedin/ads' },
    { id:'trend-discovery', label:'Trend Discovery', icon:'📈', desc:'Sounds, hashtags, formats', endpoint:'/v1/tiktok/get-trending-feed + /v1/tiktok/songs/popular' },
    { id:'influencer-prospecting', label:'Influencers', icon:'🤝', desc:'Fit score + outreach', endpoint:'/v1/tiktok/creators/popular + /v1/instagram/search/hashtag' },
    { id:'audience-research', label:'Audience', icon:'👥', desc:'Who follows who + geo', endpoint:'/v1/tiktok/profile + /v1/youtube/channel' },
    { id:'social-listening-brief', label:'Listening', icon:'👂', desc:'Themes across sources', endpoint:'/v1/reddit/search + /v1/threads/user/posts' },
    { id:'product-demand-research', label:'Demand', icon:'🔍', desc:'Pains → product ideas', endpoint:'/v1/reddit/subreddit + /v1/youtube/video/comments' },
    { id:'creator-profile-teardown', label:'Creator Teardown', icon:'🔬', desc:'Why account works', endpoint:'/v1/tiktok/profile + feed + outlier' },
    { id:'content-repurposing', label:'Repurpose', icon:'♻️', desc:'Video → LinkedIn/X/newsletter', endpoint:'transcript + content atoms' },
    { id:'scrapecreators-api', label:'API Router', icon:'🔌', desc:'27+ platforms, 110 endpoints', endpoint:'https://api.scrapecreators.com' },
  ]

  const current = skills.find(s=>s.id===skill)

  const run = () => {
    setRunning(true)
    setDone(false)
    setTimeout(()=>{ setRunning(false); setDone(true) }, 700)
  }

  const exportCsv = (rows, filename) => {
    const csv = rows.map(r=> Object.values(r).map(v=> `"${String(v).replace(/"/g,'""')}"`).join(',')).join('\n')
    const blob = new Blob([csv], { type:'text/csv' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a'); a.href=url; a.download=filename; a.click(); URL.revokeObjectURL(url)
  }

  return (
    <div className="card" style={{ overflow:'visible' }}>
      <div className="card-pad" style={{ display:'flex', justifyContent:'space-between', gap:12, flexWrap:'wrap', alignItems:'center' }}>
        <div>
          <div className="mono" style={{ color:'#0a84ff' }}>ScrapeCreators · social-media-research-skills · 13 skills · MIT · 4.7k★</div>
          <h3 style={{ margin:'6px 0 0' }}>Social Media Research Lab — outlier posts, comments, transcripts, competitors, ads & trends</h3>
          <div className="mono" style={{ color:'var(--muted)', marginTop:6 }}>{liveMode ? 'Live mode — will call api.scrapecreators.com with x-api-key' : 'Demo mode — realistic mock outputs (add SCRAPECREATORS_API_KEY for live)'} · {current?.icon} {current?.label} → <code style={{ background:'var(--panel-2)', padding:'2px 6px', borderRadius:6, border:'1px solid var(--line)' }}>{current?.endpoint}</code></div>
        </div>
        <div style={{ display:'flex', gap:8, alignItems:'center', flexWrap:'wrap' }}>
          <label className="mono" style={{ display:'flex', alignItems:'center', gap:8, padding:'6px 10px', borderRadius:999, border:'1px solid var(--line)', background:'var(--panel-2)' }}>
            <input type="checkbox" checked={liveMode} onChange={e=>setLiveMode(e.target.checked)} />
            Live
          </label>
          <div style={{ display:'flex', gap:6, alignItems:'center', padding:'6px 10px', borderRadius:999, border:'1px solid var(--line)', background:'var(--panel-2)' }}>
            <span className="mono" style={{ color:'var(--dim)' }}>API key</span>
            <input value={apiKey} onChange={e=>setApiKey(e.target.value)} placeholder="sk_…" type={showKey?'text':'password'} style={{ background:'transparent', border:0, color:'var(--ink)', outline:'none', width:120, fontFamily:'Fragment Mono, monospace', fontSize:11 }} />
            <button onClick={()=>setShowKey(v=>!v)} style={{ background:'transparent', border:0, color:'var(--muted)', cursor:'pointer', fontSize:11 }}>{showKey?'hide':'show'}</button>
          </div>
        </div>
      </div>

      <div style={{ padding:'0 16px 12px', display:'flex', gap:8, flexWrap:'wrap', alignItems:'center', borderBottom:'1px solid var(--line)' }}>
        <div style={{ display:'flex', gap:6, flexWrap:'wrap' }}>
          {skills.map(s=>(
            <button key={s.id} onClick={()=>{ setSkill(s.id); setDone(false); setTimeout(()=>setDone(true), 320) }} style={{
              padding:'8px 10px', borderRadius:999, border:'1px solid var(--line)', background: skill===s.id ? 'var(--ink)' : 'var(--panel)', color: skill===s.id ? 'var(--bg)' : 'var(--muted)', cursor:'pointer', fontSize:12, fontWeight: skill===s.id?700:500, display:'flex', alignItems:'center', gap:6
            }}>
              <span>{s.icon}</span> {s.label}
            </button>
          ))}
        </div>
        <span className="mono" style={{ color:'var(--dim)', marginLeft:6 }}>{current?.desc}</span>
      </div>

      {/* controls */}
      <div className="card-pad" style={{ background:'var(--bg-soft)', display:'flex', gap:8, flexWrap:'wrap', alignItems:'end' }}>
        <div style={{ display:'flex', flexDirection:'column', gap:4 }}>
          <span className="mono" style={{ color:'var(--dim)' }}>Handle / URL</span>
          <input value={handle} onChange={e=>setHandle(e.target.value)} style={{ padding:'10px 12px', borderRadius:10, border:'1px solid var(--line)', background:'var(--panel)', color:'var(--ink)', minWidth:200 }} placeholder="@handle or https://..." />
        </div>
        <div style={{ display:'flex', flexDirection:'column', gap:4 }}>
          <span className="mono" style={{ color:'var(--dim)' }}>Platform</span>
          <select value={platform} onChange={e=>setPlatform(e.target.value)} style={{ padding:'10px 12px', borderRadius:10, border:'1px solid var(--line)', background:'var(--panel)', color:'var(--ink)' }}>
            <option>YouTube Shorts</option><option>TikTok</option><option>Instagram Reels</option><option>YouTube</option><option>LinkedIn</option><option>Reddit</option><option>X/Twitter</option>
          </select>
        </div>
        <div style={{ display:'flex', flexDirection:'column', gap:4, flex:1, minWidth:160 }}>
          <span className="mono" style={{ color:'var(--dim)' }}>Window</span>
          <select value={scope} onChange={e=>setScope(e.target.value)} style={{ padding:'10px 12px', borderRadius:10, border:'1px solid var(--line)', background:'var(--panel)', color:'var(--ink)' }}>
            <option>20 posts · median baseline</option><option>50 posts · pagination</option><option>Latest page only</option>
          </select>
        </div>
        <button onClick={run} disabled={running} style={{ padding:'12px 16px', borderRadius:12, border:0, background: running?'var(--line)':'var(--ink)', color: running?'var(--muted)':'var(--bg)', fontWeight:700, cursor: running?'not-allowed':'pointer', minWidth:120 }}>
          {running ? 'Running…' : `Run ${current?.label}`}
        </button>
        <button onClick={()=>{
          navigator.clipboard.writeText(`npx skills add ScrapeCreators/social-media-research-skills\n# then: ${current?.endpoint}\nexport SCRAPECREATORS_API_KEY=sk_...\n# prompt: Find the outlier posts for ${handle} on ${platform} (${scope})`)
          setCopied(true); setTimeout(()=>setCopied(false), 1500)
        }} style={{ padding:'10px 12px', borderRadius:10, border:'1px solid var(--line)', background:'transparent', color:'var(--muted)', cursor:'pointer' }}>
          {copied?'Copied':'Copy prompt'}
        </button>
      </div>

      {/* output */}
      <div style={{ padding:16, minHeight:360, background:'var(--bg)' }}>
        {!done && !running && <div className="mono" style={{ color:'var(--dim)', textAlign:'center', padding:40 }}>Select a skill above to preview its artifact — all outputs are mock but spec-accurate (source URLs, baselines, VOC buckets).</div>}
        {running && <div style={{ display:'grid', placeItems:'center', height:320 }}><div className="mono" style={{ color:'var(--muted)' }}>Fetching via <code>{current?.endpoint}</code> · normalizing · median baseline · citing sources…</div></div>}
        <AnimatePresence mode="wait">
          {done && !running && (
            <motion.div key={skill} initial={{ opacity:0, y:8 }} animate={{ opacity:1, y:0 }} exit={{ opacity:0, y:-8 }} transition={{ duration:0.28 }}>
              {skill==='outlier-post-finder' && <OutlierReport handle={handle} platform={platform} scope={scope} onExport={exportCsv} />}
              {skill==='transcript-intelligence' && <TranscriptReport />}
              {skill==='comment-mining' && <CommentMining />}
              {skill==='competitor-social-research' && <CompetitorReport />}
              {skill==='ad-library-teardown' && <AdTeardown />}
              {skill==='trend-discovery' && <TrendBrief />}
              {skill==='influencer-prospecting' && <InfluencerProspects onExport={exportCsv} />}
              {skill==='audience-research' && <AudienceResearch />}
              {skill==='social-listening-brief' && <ListeningBrief />}
              {skill==='product-demand-research' && <DemandResearch />}
              {skill==='creator-profile-teardown' && <CreatorTeardown />}
              {skill==='content-repurposing' && <Repurpose />}
              {skill==='scrapecreators-api' && <ApiRouter />}
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      <div style={{ padding:'12px 16px', borderTop:'1px solid var(--line)', display:'flex', gap:8, flexWrap:'wrap', alignItems:'center', justifyContent:'space-between' }}>
        <div className="mono" style={{ color:'var(--dim)' }}>Public-data only · cited URLs · median baselines · exact language preserved · actionable next steps. See <a href="https://github.com/ScrapeCreators/social-media-research-skills" target="_blank" style={{ color:'var(--ink)' }}>ScrapeCreators/social-media-research-skills</a> + <a href="https://docs.scrapecreators.com" target="_blank" style={{ color:'var(--ink)' }}>docs.scrapecreators.com</a></div>
        <a href="https://scrapecreators.com" target="_blank" style={{ padding:'8px 12px', borderRadius:999, background:'var(--ink)', color:'var(--bg)', textDecoration:'none', fontWeight:700, fontSize:12 }}>Get API key →</a>
      </div>
    </div>
  )
}

function SectionTitle({ kicker, title, sub }){
  return <div style={{ marginBottom:12 }}>
    <div className="mono" style={{ color:'#0a84ff' }}>{kicker}</div>
    <div style={{ fontWeight:800, fontSize:18, marginTop:4 }}>{title}</div>
    {sub && <div className="mono" style={{ color:'var(--muted)', marginTop:4, textTransform:'none', letterSpacing:0 }}>{sub}</div>}
  </div>
}

function OutlierReport({ handle, platform, scope }){
  const baseline = 41000
  return <div>
    <SectionTitle kicker={`Outlier Posts Report: ${handle} · ${platform}`} title={`${mockOutliers.length} outliers from ${scope}`} sub={`Baseline: median views = ${fmtNum(baseline)} · Sample: 20 posts · Window: last 20 posts · Huge outlier ≥5×, Strong 2–5×, Mild 1.5–2×`} />
    <div style={{ display:'grid', gap:10 }}>
      {mockOutliers.map(o=>{
        const level = o.lift >=5 ? 'Huge' : o.lift>=2 ? 'Strong' : 'Mild'
        const lvlColor = o.lift>=5?'#ff3b30':o.lift>=2?'#ff9f0a':'#30d158'
        return <div key={o.id} style={{ display:'grid', gridTemplateColumns:'1fr auto', gap:12, padding:12, borderRadius:12, border:'1px solid var(--line)', background:'var(--panel)' }}>
          <div>
            <div style={{ display:'flex', gap:8, alignItems:'center', flexWrap:'wrap' }}>
              <span className="mono" style={{ color:lvlColor, background:`color-mix(in srgb, ${lvlColor} 12%, transparent)`, padding:'2px 8px', borderRadius:999, border:`1px solid ${lvlColor}` }}>{level} · {o.lift.toFixed(1)}×</span>
              <span className="mono" style={{ color:'var(--muted)' }}>{o.platform} · {fmtNum(o.views)} views · {fmtNum(o.likes)} likes · {o.comments} comments</span>
              <a href={o.url} target="_blank" className="mono" style={{ color:'var(--accent-2)' }}>source ↗</a>
            </div>
            <div style={{ fontWeight:700, marginTop:6 }}>{o.title}</div>
            <div style={{ display:'flex', gap:8, flexWrap:'wrap', marginTop:8 }}>
              <span className="chip"><b>Hook</b> {o.hook}</span>
              <span className="chip"><b>Format</b> {o.format}</span>
              <span className="chip"><b>Why</b> {o.why}</span>
            </div>
          </div>
          <div style={{ display:'flex', flexDirection:'column', alignItems:'end', gap:6, minWidth:90 }}>
            <div style={{ width:90, height:6, borderRadius:999, background:'var(--line)', overflow:'hidden' }}><i style={{ display:'block', height:'100%', width:`${clamp(o.lift/20*100, 8, 100)}%`, background:lvlColor }} /></div>
            <span className="mono" style={{ color:'var(--dim)' }}>{o.lift.toFixed(1)}× baseline</span>
          </div>
        </div>
      })}
    </div>
    <div style={{ marginTop:12, display:'flex', gap:8, flexWrap:'wrap' }}>
      <span className="chip"><b>Pattern</b> “don’t want you to know” + steal framing repeats in 2/4 outliers</span>
      <span className="chip"><b>Swipe</b> Hook library: shock + promise gap at 0:03</span>
    </div>
  </div>
}

function TranscriptReport(){
  return <div>
    <SectionTitle kicker="Transcript Intelligence — 3 videos · TikTok + YouTube + Reels" title="Hooks, claims, quotes → content atoms" sub="Source: /v1/youtube/video/transcript · /v1/tiktok/video/transcript · preserved verbatim" />
    <div style={{ display:'grid', gap:12 }}>
      <div style={{ padding:12, borderRadius:12, background:'var(--panel)', border:'1px solid var(--line)' }}>
        <div className="mono" style={{ color:'var(--dim)' }}>Summary</div>
        <div style={{ marginTop:6, color:'var(--muted)' }}>Creator leans on authority-challenge hooks (“banks don’t want you to know”) + founder-proof (14 brand tests). Best retention at 0:00-0:08. Strongest CTA: “steal this”.</div>
      </div>
      <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:12 }}>
        <div style={{ padding:12, borderRadius:12, background:'var(--panel)', border:'1px solid var(--line)' }}>
          <div className="mono">Hooks (steal these)</div>
          <ul style={{ margin:'8px 0 0', paddingLeft:16, color:'var(--muted)' }}>
            <li>“If your next video flops, it’s not the algorithm — it’s this one sentence…”</li>
            <li>“banks don’t want you to know your CAC is refundable”</li>
            <li>“We tested on 14 brands. 9 saw lift in 7 days.”</li>
          </ul>
        </div>
        <div style={{ padding:12, borderRadius:12, background:'var(--panel)', border:'1px solid var(--line)' }}>
          <div className="mono">Claims to verify</div>
          <ul style={{ margin:'8px 0 0', paddingLeft:16, color:'var(--muted)' }}>
            <li>Hook controls 70% of watch time — <span className="mono" style={{ color:'#ff9f0a' }}>cite needed</span></li>
            <li>9/14 brands saw lift — <span className="mono" style={{ color:'#30d158' }}>cite: 14 brand test</span></li>
          </ul>
        </div>
      </div>
      <div style={{ padding:12, borderRadius:12, background:'var(--panel-2)', border:'1px solid var(--line)' }}>
        <div className="mono">Timestamped transcript</div>
        {mockTranscripts.map(t=>(
          <div key={t.at} style={{ display:'flex', gap:10, padding:'8px 0', borderBottom:'1px solid var(--line)' }}>
            <span className="mono" style={{ color:'var(--dim)', minWidth:36 }}>{t.at}</span>
            <span style={{ flex:1, color:'var(--ink)' }}>{t.text}</span>
            <span className="mono" style={{ color:'var(--muted)' }}>{t.quotes.join(' · ')}</span>
          </div>
        ))}
      </div>
      <div style={{ display:'flex', gap:8, flexWrap:'wrap' }}>
        <span className="chip"><b>Content atoms</b> 3 hooks + 2 claims + 1 proof block</span>
        <span className="chip"><b>Repurpose</b> LinkedIn post from 0:00 hook, X thread from 0:23 angle</span>
      </div>
    </div>
  </div>
}

function CommentMining(){
  const [filter, setFilter] = useState('all')
  const filtered = filter==='all' ? mockComments : mockComments.filter(c=> c.buckets.includes(filter))
  return <div>
    <SectionTitle kicker="Comment Mining — VOC Report · 6 sampled (from 2,400) · TikTok + Reels + Shorts" title="Questions, objections, pains, intents → exact language" sub="Endpoint: /v1/tiktok/video/comments · /v1/youtube/video/comments · kept verbatim" />
    <div style={{ display:'flex', gap:6, flexWrap:'wrap', marginBottom:12 }}>
      {['all','questions','objections','pain','requests','buying intent','praise','controversy'].map(b=>(
        <button key={b} onClick={()=>setFilter(b)} style={{ padding:'6px 10px', borderRadius:999, border:'1px solid var(--line)', background: filter===b ? 'var(--ink)' : 'transparent', color: filter===b ? 'var(--bg)' : 'var(--muted)', fontSize:11, cursor:'pointer' }}>{b}</button>
      ))}
    </div>
    <div style={{ display:'grid', gap:8 }}>
      {filtered.map((c,i)=>(
        <div key={i} style={{ padding:12, borderRadius:12, background:'var(--panel)', border:'1px solid var(--line)', display:'flex', gap:10 }}>
          <span className="mono" style={{ color:'var(--dim)' }}>@{c.author.slice(1)}</span>
          <span style={{ flex:1, color:'var(--ink)' }}>“{c.text}”</span>
          <span className="mono" style={{ color:'var(--muted)' }}>♥ {c.likes}</span>
          <span style={{ display:'flex', gap:4, flexWrap:'wrap' }}>{c.buckets.map(b=> <span key={b} className="mono" style={{ padding:'2px 6px', borderRadius:6, background:'var(--panel-2)', border:'1px solid var(--line)', fontSize:10 }}>{b}</span>)}</span>
        </div>
      ))}
    </div>
    <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:12, marginTop:12 }}>
      <div style={{ padding:12, borderRadius:12, background:'var(--panel)', border:'1px solid var(--line)' }}>
        <div className="mono">Themes (by freq + intensity)</div>
        <div className="mono" style={{ marginTop:8, color:'var(--muted)' }}>1. “Template please” (18 mentions) 2. B2B vs DTC (12) 3. “$200/mo pain” (9)</div>
      </div>
      <div style={{ padding:12, borderRadius:12, background:'var(--panel)', border:'1px solid var(--line)' }}>
        <div className="mono">Content ideas from comments</div>
        <div className="mono" style={{ marginTop:8, color:'var(--muted)' }}>→ “Saves ≠ sales” teardown (from 81♥ comment) → “$0 tool” landing angle → “B2B outlier” niche report</div>
      </div>
    </div>
  </div>
}

function CompetitorReport(){
  return <div>
    <SectionTitle kicker="Competitor Social Research — 3 brands · TikTok + Instagram + YouTube" title="Pillars, formats, cadence, gaps" sub="Baselines per account (median), not raw view comps. Endpoints: /v1/youtube/channel-videos + /v1/tiktok/creators/popular + profile" />
    <div style={{ display:'grid', gridTemplateColumns:'repeat(3, 1fr)', gap:12 }}>
      {mockCompetitors.map(c=>(
        <div key={c.name} style={{ padding:12, borderRadius:12, background:'var(--panel)', border:'1px solid var(--line)' }}>
          <div style={{ fontWeight:800 }}>{c.name}</div>
          <div className="mono" style={{ color:'var(--muted)' }}>{c.handle} · {fmtNum(c.followers)} · {c.posts} posts</div>
          <div style={{ marginTop:8, height:6, borderRadius:999, background:'var(--line)', overflow:'hidden' }}><i style={{ display:'block', height:'100%', width:`${clamp(c.topViews/900000*100,10,100)}%`, background:'#0a84ff' }} /></div>
          <div className="mono" style={{ color:'var(--dim)', marginTop:4 }}>median {fmtNum(c.medianViews)} · top {fmtNum(c.topViews)} · lift {(c.topViews/c.medianViews).toFixed(1)}×</div>
          <div style={{ marginTop:8, display:'flex', gap:6, flexWrap:'wrap' }}>{c.pillars.map(p=> <span key={p} className="chip" style={{ fontSize:10 }}>{p}</span>)}</div>
          <div className="mono" style={{ marginTop:8, color:'#ff9f0a' }}>Gap: {c.gap}</div>
        </div>
      ))}
    </div>
    <div style={{ marginTop:12, padding:12, borderRadius:12, background:'var(--panel-2)', border:'1px solid var(--line)' }}>
      <div className="mono">Gaps → opportunities</div>
      <div style={{ color:'var(--muted)', marginTop:6 }}>• Carousel→Reel repurpose is whitespace (1/3 use it, 3× median) • Hook library is underused (only StarterStory systematizes) • Ad teardown series: no competitor does it weekly</div>
    </div>
  </div>
}

function AdTeardown(){
  return <div>
    <SectionTitle kicker="Ad Library Teardown — Meta + Google + LinkedIn · active ads" title="Messaging angles, hooks, offers, CTAs" sub="Endpoints: /v1/meta/ads + /v1/google/ads + /v1/linkedin/ads · Active 14d window" />
    <div style={{ display:'grid', gap:10 }}>
      {mockAds.map(a=>(
        <div key={a.platform} style={{ padding:12, borderRadius:12, background:'var(--panel)', border:'1px solid var(--line)', display:'grid', gridTemplateColumns:'80px 1fr auto', gap:12, alignItems:'center' }}>
          <span className="mono" style={{ padding:'6px 10px', borderRadius:999, background:'var(--panel-2)', border:'1px solid var(--line)', textAlign:'center' }}>{a.platform}</span>
          <div>
            <div style={{ fontWeight:700 }}>“{a.copy}”</div>
            <div className="mono" style={{ color:'var(--muted)', marginTop:4 }}>Hook: {a.hook} · Offer: {a.offer} · CTA: {a.cta} · Spend: {a.spend}</div>
          </div>
          <a href={a.url} target="_blank" className="mono" style={{ color:'var(--accent-2)' }}>ad ↗</a>
        </div>
      ))}
    </div>
    <div style={{ marginTop:12, display:'flex', gap:8, flexWrap:'wrap' }}>
      <span className="chip"><b>Angle to steal</b> “steal framing” + price anchor ($200/mo)</span>
      <span className="chip"><b>Test</b> CTA: Download teardown vs Start free — video vs carousel</span>
    </div>
  </div>
}

function TrendBrief(){
  return <div>
    <SectionTitle kicker="Trend Discovery Brief — TikTok + Reels + Shorts · niche: founder marketing" title="Trends worth acting on (not just “trending”)" sub="Endpoints: /v1/tiktok/get-trending-feed + /v1/tiktok/songs/popular + /v1/tiktok/search/top" />
    <div style={{ display:'grid', gap:8 }}>
      {mockTrends.map(t=>(
        <div key={t.trend} style={{ padding:12, borderRadius:12, background:'var(--panel)', border:'1px solid var(--line)' }}>
          <div style={{ fontWeight:700 }}>{t.trend}</div>
          <div className="mono" style={{ color:'var(--muted)', marginTop:4 }}>{t.platform} · Evidence: {t.evidence} · Why: {t.why}</div>
          <div className="chip" style={{ marginTop:8 }}><b>Angle</b> {t.angle}</div>
        </div>
      ))}
    </div>
    <div style={{ marginTop:12, display:'flex', gap:8, flexWrap:'wrap' }}>
      <span className="chip"><b>Sounds</b> “make it pop” skit audio · 4 posts &gt;5× baseline</span>
      <span className="chip"><b>Hashtags</b> #founderstory #contentmarketing</span>
    </div>
  </div>
}

function InfluencerProspects({ onExport }){
  return <div>
    <SectionTitle kicker="Influencer Prospecting — prospect CSV + fit score" title={`${mockProspects.length} prospects from public social data`} sub="Endpoints: /v1/tiktok/creators/popular + /v1/instagram/search/hashtag → CSV" />
    <div style={{ display:'grid', gap:8 }}>
      {mockProspects.map(p=>(
        <div key={p.creator} style={{ padding:12, borderRadius:12, background:'var(--panel)', border:'1px solid var(--line)', display:'grid', gridTemplateColumns:'1fr auto', gap:12 }}>
          <div>
            <div style={{ fontWeight:700 }}>{p.creator} <span className="mono" style={{ color:'var(--muted)' }}>· {fmtNum(p.followers)} · {p.niche}</span> <span className="mono" style={{ padding:'2px 8px', borderRadius:999, background:'#0a84ff', color:'#fff' }}>{p.fit} fit</span></div>
            <div className="mono" style={{ color:'var(--muted)', marginTop:4 }}>{p.reason}</div>
            <div className="chip" style={{ marginTop:8 }}><b>DM</b> “{p.outreach}”</div>
          </div>
          <div style={{ width:80, display:'grid', placeItems:'center' }}>
            <div style={{ width:64, height:64, borderRadius:'50%', background:`conic-gradient(#0a84ff ${p.fit}%, var(--line) ${p.fit}%)`, display:'grid', placeItems:'center' }}><span style={{ width:52, height:52, borderRadius:'50%', background:'var(--panel)', display:'grid', placeItems:'center', fontWeight:800 }}>{p.fit}</span></div>
          </div>
        </div>
      ))}
    </div>
    <button onClick={()=>onExport(mockProspects.map(p=>({ creator:p.creator, followers:p.followers, fit:p.fit })), 'prospects.csv')} style={{ marginTop:12, padding:'8px 12px', borderRadius:999, border:'1px solid var(--line)', background:'var(--ink)', color:'var(--bg)', fontWeight:700, cursor:'pointer' }}>Export CSV</button>
  </div>
}

function AudienceResearch(){
  return <div>
    <SectionTitle kicker="Audience Research — who follows who + geo/demographic signals" title="Fit: indie hackers + B2B founders dominate" sub="Endpoints: /v1/tiktok/profile + /v1/youtube/channel + /v1/twitter/profile · confidence: high/medium/low" />
    <div style={{ display:'grid', gap:10 }}>
      {mockAudience.map(a=>(
        <div key={a.segment} style={{ padding:12, borderRadius:12, background:'var(--panel)', border:'1px solid var(--line)' }}>
          <div style={{ display:'flex', gap:8, alignItems:'center', flexWrap:'wrap' }}>
            <span style={{ fontWeight:700 }}>{a.segment}</span>
            <span className="mono" style={{ padding:'2px 8px', borderRadius:999, background: a.confidence==='high' ? '#30d158' : '#ff9f0a', color:'#fff' }}>{a.confidence} confidence</span>
            <span className="mono" style={{ color:'var(--dim)' }}>{a.size} of audience</span>
          </div>
          <div style={{ marginTop:8, display:'flex', gap:6, flexWrap:'wrap' }}>{a.signals.map(s=> <span key={s} className="chip" style={{ fontSize:10 }}>{s}</span>)}</div>
        </div>
      ))}
    </div>
  </div>
}

function ListeningBrief(){
  return <div>
    <SectionTitle kicker="Social Listening Brief — multi-source · Reddit + Threads + LinkedIn + X" title="What people say about “outlier finder”" sub="Endpoints: /v1/reddit/search + /v1/threads/user/posts · cited examples, sentiment caveats" />
    <div style={{ display:'grid', gap:8 }}>
      {mockListening.map(t=>(
        <div key={t.theme} style={{ padding:12, borderRadius:12, background:'var(--panel)', border:'1px solid var(--line)' }}>
          <div style={{ display:'flex', gap:8, alignItems:'center', flexWrap:'wrap' }}>
            <span style={{ fontWeight:700 }}>{t.theme}</span>
            <span className="mono" style={{ color:'var(--dim)' }}>{t.mentions} mentions</span>
            <span className="mono" style={{ padding:'2px 8px', borderRadius:999, background:t.sentiment==='positive'?'#30d158':t.sentiment==='negative'?'#ff3b30':'var(--line)', color:'#fff' }}>{t.sentiment}</span>
          </div>
          <div className="mono" style={{ color:'var(--muted)', marginTop:4 }}>e.g. “{t.example}”</div>
          <div className="chip" style={{ marginTop:8 }}><b>Action</b> {t.action}</div>
        </div>
      ))}
    </div>
  </div>
}

function DemandResearch(){
  return <div>
    <SectionTitle kicker="Product Demand Research — pains, objections, language → ideas" title="From “saves ≠ sales” to product angles" sub="Endpoints: /v1/reddit/subreddit + /v1/youtube/video/comments → demand signals" />
    <div style={{ display:'grid', gap:8 }}>
      {mockDemand.map(d=>(
        <div key={d.pain} style={{ padding:12, borderRadius:12, background:'var(--panel)', border:'1px solid var(--line)' }}>
          <div style={{ fontWeight:700 }}>“{d.pain}” <span className="mono" style={{ color:'var(--dim)' }}>· {d.freq} mentions · {d.intent} intent</span></div>
          <div className="mono" style={{ color:'var(--muted)', marginTop:4 }}>Exact: “{d.language}”</div>
          <div className="chip" style={{ marginTop:8 }}><b>Opportunity</b> {d.opp}</div>
        </div>
      ))}
    </div>
  </div>
}

function CreatorTeardown(){
  const c = mockCreator
  return <div>
    <SectionTitle kicker={`Creator Profile Teardown — ${c.handle} · ${fmtNum(c.followers)} followers`} title={c.positioning} sub="Why this account works: pillars, outliers, playbook · Endpoints: /v1/tiktok/profile + feed + outlier" />
    <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:12 }}>
      <div style={{ padding:12, borderRadius:12, background:'var(--panel)', border:'1px solid var(--line)' }}>
        <div className="mono">Bio</div>
        <div style={{ marginTop:6, color:'var(--muted)' }}>{c.bio}</div>
        <div className="mono" style={{ marginTop:12 }}>Content pillars</div>
        <div style={{ display:'flex', gap:6, flexWrap:'wrap', marginTop:6 }}>{c.pillars.map(p=> <span key={p} className="chip">{p}</span>)}</div>
      </div>
      <div style={{ padding:12, borderRadius:12, background:'var(--panel)', border:'1px solid var(--line)' }}>
        <div className="mono">Outliers you can steal</div>
        <ul style={{ margin:'8px 0 0', paddingLeft:16, color:'var(--muted)' }}>
          {c.outliers.map(o=> <li key={o.id}><a href={o.url} target="_blank" style={{ color:'var(--ink)' }}>{o.title}</a> — {o.lift.toFixed(1)}× · {o.hook}</li>)}
        </ul>
      </div>
    </div>
    <div style={{ marginTop:12, padding:12, borderRadius:12, background:'var(--panel-2)', border:'1px solid var(--line)' }}>
      <div className="mono">Playbook to copy</div>
      <ol style={{ margin:'8px 0 0', paddingLeft:16, color:'var(--muted)' }}>
        {c.playbook.map((p,i)=> <li key={i}>{p}</li>)}
      </ol>
    </div>
  </div>
}

function Repurpose(){
  const r = mockRepurpose[0]
  return <div>
    <SectionTitle kicker="Content Repurposing — video → LinkedIn / X / newsletter / script" title="Turn 1 video into 4 assets" sub="Input: transcript + hooks + claims → content atoms" />
    <div style={{ padding:12, borderRadius:12, background:'var(--panel)', border:'1px solid var(--line)', marginBottom:12 }}>
      <div className="mono">Source</div>
      <div style={{ marginTop:6 }}>{r.source}</div>
    </div>
    <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:12 }}>
      <div style={{ padding:12, borderRadius:12, background:'var(--panel)', border:'1px solid var(--line)' }}>
        <div className="mono">LinkedIn post</div>
        <div style={{ marginTop:6, color:'var(--muted)' }}>{r.linkedin}</div>
      </div>
      <div style={{ padding:12, borderRadius:12, background:'var(--panel)', border:'1px solid var(--line)' }}>
        <div className="mono">X thread (3 tweets)</div>
        <ol style={{ margin:'8px 0 0', paddingLeft:16, color:'var(--muted)' }}>{r.xThread.map((t,i)=> <li key={i}>{t}</li>)}</ol>
      </div>
      <div style={{ padding:12, borderRadius:12, background:'var(--panel)', border:'1px solid var(--line)' }}>
        <div className="mono">Newsletter / blog idea</div>
        <div style={{ marginTop:6, color:'var(--muted)' }}>{r.newsletter}</div>
      </div>
      <div style={{ padding:12, borderRadius:12, background:'var(--panel)', border:'1px solid var(--line)' }}>
        <div className="mono">Script (next video)</div>
        <div style={{ marginTop:6, color:'var(--muted)' }}>{r.script}</div>
      </div>
    </div>
  </div>
}

function ApiRouter(){
  const endpoints = [
    { platform:'TikTok', path:'/v1/tiktok/profile', param:'handle=stoolpresidente', ex:'https://api.scrapecreators.com/v1/tiktok/profile?handle=charlidamelio' },
    { platform:'YouTube', path:'/v1/youtube/channel-videos', param:'handle/channelId/url', ex:'https://api.scrapecreators.com/v1/youtube/channel-videos?handle=ThePatMcAfeeShow' },
    { platform:'Instagram', path:'/v2/instagram/user/posts', param:'handle=jane', ex:'https://api.scrapecreators.com/v2/instagram/user/posts?handle=jane' },
    { platform:'X', path:'/v1/twitter/user-tweets', param:'handle=elonmusk', ex:'https://api.scrapecreators.com/v1/twitter/user-tweets?handle=elonmusk' },
    { platform:'Reddit', path:'/v1/reddit/subreddit', param:'subreddit=AskReddit', ex:'https://api.scrapecreators.com/v1/reddit/subreddit?subreddit=AskReddit' },
    { platform:'LinkedIn', path:'/v1/linkedin/company', param:'url=.../company/shopify', ex:'https://api.scrapecreators.com/v1/linkedin/company?url=https://linkedin.com/company/shopify' },
  ]
  return <div>
    <SectionTitle kicker="ScrapeCreators API — 27+ platforms, 110 endpoints" title="Raw data layer for all workflows" sub="Base: https://api.scrapecreators.com · header: x-api-key · GET with query params" />
    <div style={{ padding:12, borderRadius:12, background:'#0f0f12', border:'1px solid var(--line)', fontFamily:'Fragment Mono, monospace', fontSize:11, color:'#9a9aaa' }}>
      <div style={{ color:'#30d158' }}>curl -s "https://api.scrapecreators.com/v1/tiktok/profile?handle=charlidamelio" \</div>
      <div>  -H "x-api-key: $SCRAPECREATORS_API_KEY" | jq</div>
      <div style={{ marginTop:8, color:'var(--muted)' }}>Per-endpoint OpenAPI: https://docs.scrapecreators.com/{"{path}"}/openapi.json · Full spec: https://docs.scrapecreators.com/openapi.json</div>
    </div>
    <div style={{ display:'grid', gap:8, marginTop:12 }}>
      {endpoints.map(e=>(
        <div key={e.path} style={{ padding:12, borderRadius:12, background:'var(--panel)', border:'1px solid var(--line)', display:'grid', gridTemplateColumns:'100px 1fr', gap:12, alignItems:'center' }}>
          <span className="mono" style={{ background:'var(--panel-2)', padding:'4px 8px', borderRadius:6, border:'1px solid var(--line)', textAlign:'center' }}>{e.platform}</span>
          <div>
            <div className="mono" style={{ color:'var(--ink)' }}>{e.path} · <span style={{ color:'var(--muted)' }}>{e.param}</span></div>
            <div className="mono" style={{ color:'var(--dim)', fontSize:10, marginTop:4, wordBreak:'break-all' }}>{e.ex}</div>
          </div>
        </div>
      ))}
    </div>
    <div className="mono" style={{ marginTop:12, color:'var(--dim)' }}>Agent skill routing: user intent → workflow skill (outlier/comment/etc.) → scrapecreators-api for endpoint params → fetch → normalize → baseline → artifact with citations.</div>
  </div>
}
