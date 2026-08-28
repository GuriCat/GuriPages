# -*- coding: utf-8 -*-
import json, collections, html, io

rows = json.load(open('rows.json', encoding='utf-8'))
summary = json.load(open('summary.json', encoding='utf-8'))
bul = json.load(open('bulletins.json', encoding='utf-8'))

SEV = ['Critical', 'High', 'Medium', 'Low']
VORDER = ['7.6', '7.5', '7.4', '7.3', '7.2', '7.1', '6.1']


def vkey(x):
    return VORDER.index(x) if x in VORDER else len(VORDER) + (0 if x[0].isdigit() else 1)


# --- 速報テーブル（本文は重複するので正規化） ---
bmap = {}
for nid in {r['nid'] for r in rows}:
    v = bul[nid]
    bmap[nid] = [v['title'], v['url'], v['pub_date'], v['severity'],
                 '; '.join('%s (%s)' % (c, v['cves'][c]) for c in sorted(v['cves'])),
                 v.get('workaround_text', '')[:4000], v['remediation_text'][:1500]]

lpp_name = {}
for r in rows:
    lpp_name[r['ライセンスプログラム']] = r['ライセンスプログラム名']

data = [[r['IBM i リリース'], r['ライセンスプログラム'], r['PTF番号'],
         'G' if r['PTF種別'] == 'グループPTF' else 'P', r['nid'],
         r['製品バージョン'], r['対象プロダクト'], r['オプション'], r['LPP判定根拠'],
         r['リリース補完']]
        for r in rows]

# --- 集計マトリクス ---
vers = sorted({r['IBM i リリース'] for r in rows}, key=vkey)
lpps = sorted({r['ライセンスプログラム'] for r in rows})
cell = collections.defaultdict(lambda: {'ptf': set(), 'sev': collections.Counter(), 'nid': set()})
for r in rows:
    c = cell[(r['ライセンスプログラム'], r['IBM i リリース'])]
    c['ptf'].add(r['PTF番号'])
    c['nid'].add(r['nid'])
    c['sev'][r['Severity']] += 1
matrix = {'%s|%s' % k: {'ptf': len(v['ptf']), 'nid': len(v['nid']), 'sev': dict(v['sev'])}
          for k, v in cell.items()}

lpp_total = {l: len({r['PTF番号'] for r in rows if r['ライセンスプログラム'] == l}) for l in lpps}
lpps.sort(key=lambda l: -lpp_total[l])

sev_total = collections.Counter()
for nid in bmap:
    sev_total[bul[nid]['severity']] += 1

payload = {
    'rows': data, 'bul': bmap, 'lppName': lpp_name, 'vers': vers, 'lpps': lpps,
    'matrix': matrix, 'sevTotal': dict(sev_total),
    'stats': {'ptf': len({r['PTF番号'] for r in rows}), 'rows': len(rows),
              'bulletins': len(bmap), 'cves': len({c for nid in bmap for c in bul[nid]['cves']}),
              'from': min(v[2] for v in bmap.values()), 'to': max(v[2] for v in bmap.values())},
}

CSS = """
:root{
  --ground:#eaeef1; --surface:#ffffff; --surface-2:#f3f6f8; --line:#d3dbe1;
  --ink:#111a20; --ink-2:#3f5260; --muted:#6b8091;
  --accent:#0d6e80; --accent-soft:#d9edf1; --accent-ink:#0a5361;
  --crit:#a8123c; --high:#c9541b; --med:#96700a; --low:#4a7a96;
  --crit-bg:#fbe4ea; --high-bg:#fceade; --med-bg:#f8f0d8; --low-bg:#e5eef4;
  --shadow:0 1px 2px rgba(16,32,44,.06),0 8px 24px -16px rgba(16,32,44,.28);
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    --ground:#0c1216; --surface:#141d23; --surface-2:#1b262e; --line:#2a3941;
    --ink:#e3ecf1; --ink-2:#a9bcc7; --muted:#7c94a1;
    --accent:#4cb8cd; --accent-soft:#123138; --accent-ink:#8ad6e5;
    --crit:#ff7d9e; --high:#ffa269; --med:#e0bd52; --low:#8fbdd6;
    --crit-bg:#3a1420; --high-bg:#3a2113; --med-bg:#332a10; --low-bg:#152833;
    --shadow:0 1px 2px rgba(0,0,0,.4),0 8px 24px -16px rgba(0,0,0,.8);
  }
}
:root[data-theme="dark"]{
  --ground:#0c1216; --surface:#141d23; --surface-2:#1b262e; --line:#2a3941;
  --ink:#e3ecf1; --ink-2:#a9bcc7; --muted:#7c94a1;
  --accent:#4cb8cd; --accent-soft:#123138; --accent-ink:#8ad6e5;
  --crit:#ff7d9e; --high:#ffa269; --med:#e0bd52; --low:#8fbdd6;
  --crit-bg:#3a1420; --high-bg:#3a2113; --med-bg:#332a10; --low-bg:#152833;
  --shadow:0 1px 2px rgba(0,0,0,.4),0 8px 24px -16px rgba(0,0,0,.8);
}
*{box-sizing:border-box}
body{
  margin:0; background:var(--ground); color:var(--ink);
  font-family:"IBM Plex Sans","Hiragino Kaku Gothic ProN","Yu Gothic",system-ui,sans-serif;
  font-size:15px; line-height:1.6; -webkit-font-smoothing:antialiased;
}
.wrap{max-width:1360px; margin:0 auto; padding:28px 24px 72px; display:flex; flex-direction:column; gap:28px}
code,.mono{font-family:"IBM Plex Mono",ui-monospace,SFMono-Regular,monospace}

/* ---- header ---- */
header{display:flex; flex-direction:column; gap:14px}
.eyebrow{
  font-size:11px; letter-spacing:.16em; text-transform:uppercase;
  color:var(--accent-ink); font-weight:600;
}
h1{
  margin:0; font-size:clamp(26px,3.4vw,38px); line-height:1.15; font-weight:600;
  letter-spacing:-.02em; text-wrap:balance;
}
.lede{margin:0; max-width:66ch; color:var(--ink-2)}
.lede a{color:var(--accent-ink)}
.statbar{
  display:flex; flex-wrap:wrap; gap:1px; background:var(--line);
  border:1px solid var(--line); border-radius:3px; overflow:hidden; box-shadow:var(--shadow);
}
.stat{background:var(--surface); padding:12px 18px; flex:1 1 130px; min-width:130px}
.stat b{display:block; font-size:24px; font-weight:600; font-variant-numeric:tabular-nums; letter-spacing:-.01em}
.stat span{font-size:11px; letter-spacing:.1em; text-transform:uppercase; color:var(--muted)}

/* ---- sections ---- */
section{display:flex; flex-direction:column; gap:12px}
h2{
  margin:0; font-size:13px; font-weight:600; letter-spacing:.14em; text-transform:uppercase;
  color:var(--muted); display:flex; align-items:baseline; gap:10px;
}
h2::after{content:""; flex:1; height:1px; background:var(--line)}
.note{margin:0; font-size:13px; color:var(--muted); max-width:76ch}

/* ---- matrix ---- */
.scroll{overflow-x:auto; border:1px solid var(--line); border-radius:3px; background:var(--surface); box-shadow:var(--shadow)}
table{border-collapse:collapse; width:100%; font-size:13.5px}
th,td{text-align:left; padding:9px 12px; border-bottom:1px solid var(--line); vertical-align:top}
thead th{
  position:sticky; top:0; z-index:2; background:var(--surface-2); color:var(--ink-2);
  font-size:11px; letter-spacing:.09em; text-transform:uppercase; font-weight:600; white-space:nowrap;
}
tbody tr:last-child td{border-bottom:0}
.mx td,.mx th{border-right:1px solid var(--line)}
.mx td:last-child,.mx th:last-child{border-right:0}
.mx .num{text-align:right; font-variant-numeric:tabular-nums; white-space:nowrap}
.mx .lppcell{white-space:nowrap}
.mx .lppcell b{font-weight:600}
.mx .lppcell small{display:block; color:var(--muted); font-size:11.5px; font-weight:400}
.mx tbody tr:hover td{background:var(--surface-2)}
.bar{display:flex; height:4px; margin-top:5px; border-radius:2px; overflow:hidden; background:var(--line)}
.bar i{display:block; height:100%}
.bar .c{background:var(--crit)} .bar .h{background:var(--high)}
.bar .m{background:var(--med)} .bar .l{background:var(--low)}
.zero{color:var(--muted); opacity:.45}

/* ---- filters ---- */
.filters{
  display:flex; flex-wrap:wrap; gap:10px 14px; align-items:flex-end;
  background:var(--surface); border:1px solid var(--line); border-radius:3px;
  padding:14px 16px; box-shadow:var(--shadow);
}
.field{display:flex; flex-direction:column; gap:5px}
.field label{font-size:10.5px; letter-spacing:.11em; text-transform:uppercase; color:var(--muted); font-weight:600}
select,input[type=search]{
  font:inherit; font-size:13.5px; color:var(--ink); background:var(--surface-2);
  border:1px solid var(--line); border-radius:2px; padding:6px 9px; min-width:160px;
}
input[type=search]{min-width:230px}
select:focus-visible,input:focus-visible,button:focus-visible,summary:focus-visible{
  outline:2px solid var(--accent); outline-offset:2px;
}
.chips{display:flex; gap:6px; flex-wrap:wrap}
.chip{
  font:inherit; font-size:12px; cursor:pointer; padding:5px 11px; border-radius:999px;
  border:1px solid var(--line); background:var(--surface-2); color:var(--ink-2);
}
.chip[aria-pressed="true"]{background:var(--accent-soft); border-color:var(--accent); color:var(--accent-ink); font-weight:600}
.spacer{flex:1}
.count{font-size:12.5px; color:var(--muted); font-variant-numeric:tabular-nums; white-space:nowrap}

/* ---- detail table ---- */
.dt{font-size:13.5px}
.dt td{border-bottom:1px solid var(--line)}
.dt tbody tr:hover td{background:var(--surface-2)}
.ptf{font-family:"IBM Plex Mono",monospace; font-weight:500; white-space:nowrap}
.rel{font-variant-numeric:tabular-nums; font-weight:600; white-space:nowrap}
.est{
  display:block; margin-top:2px; font-size:10px; font-weight:400; letter-spacing:.04em;
  color:var(--muted); border-bottom:1px dotted var(--line); cursor:help; width:max-content;
}
.date{font-variant-numeric:tabular-nums; color:var(--ink-2); white-space:nowrap; font-size:13px}
.lpp{white-space:nowrap; font-family:"IBM Plex Mono",monospace; font-size:12.5px}
.lpp small{display:block; font-family:"IBM Plex Sans",sans-serif; color:var(--muted); font-size:11.5px}
.title{max-width:44ch}
.title a{color:inherit; text-decoration:none; border-bottom:1px solid var(--line)}
.title a:hover{border-bottom-color:var(--accent); color:var(--accent-ink)}
.cve{display:block; font-size:11.5px; color:var(--muted); font-family:"IBM Plex Mono",monospace; margin-top:3px}
.sev{
  display:inline-flex; align-items:center; gap:6px; font-size:11.5px; font-weight:600;
  padding:2px 9px 2px 7px; border-radius:2px; white-space:nowrap;
}
.sev::before{content:""; width:3px; height:11px; border-radius:1px; background:currentColor}
.sev-Critical{color:var(--crit); background:var(--crit-bg)}
.sev-High{color:var(--high); background:var(--high-bg)}
.sev-Medium{color:var(--med); background:var(--med-bg)}
.sev-Low{color:var(--low); background:var(--low-bg)}
.kind{font-size:11px; color:var(--muted); letter-spacing:.04em}
.wa{
  margin-top:6px; border-top:1px dashed var(--line); padding-top:6px;
}
.wa summary{
  cursor:pointer; font-size:11.5px; font-weight:600; color:var(--accent-ink);
  letter-spacing:.04em; list-style:none;
}
.wa summary::-webkit-details-marker{display:none}
.wa summary::before{content:"▸ "; }
.wa[open] summary::before{content:"▾ "}
.wa p{margin:6px 0 0; font-size:12.5px; color:var(--ink-2); max-width:78ch;
  max-height:240px; overflow-y:auto; padding-right:6px}
.wa .lbl{font-size:10.5px; letter-spacing:.1em; text-transform:uppercase; color:var(--muted); font-weight:600; display:block; margin-top:8px}
.more{display:flex; justify-content:center; padding:14px}
button.load{
  font:inherit; font-size:13px; font-weight:600; cursor:pointer; padding:8px 20px;
  border:1px solid var(--accent); border-radius:2px; background:var(--accent-soft); color:var(--accent-ink);
}
/* ---- PTF 抽出ダイアログ ---- */
.mx td[data-cell]{cursor:pointer}
.mx td[data-cell]:hover{background:var(--accent-soft)}
.mx td[data-cell]:focus-visible{outline:2px solid var(--accent); outline-offset:-2px}
#pk[hidden]{display:none}
#pk{
  position:fixed; inset:0; z-index:50; display:flex; align-items:center; justify-content:center;
  padding:20px; pointer-events:none;      /* 背面の表を操作できるフローティング窓 */
}
.pk-card{
  pointer-events:auto;
  background:var(--surface); border:1px solid var(--line); border-radius:3px;
  box-shadow:0 24px 64px -18px rgba(6,14,20,.55), 0 0 0 1px rgba(6,14,20,.06);
  width:min(720px,100%);
  max-height:90vh; overflow-y:auto; display:flex; flex-direction:column; gap:16px; padding:0 22px 22px;
}
.pk-head{
  display:flex; align-items:flex-start; gap:14px; cursor:grab; user-select:none;
  position:sticky; top:0; z-index:1; background:var(--surface);
  margin:0 -22px; padding:16px 22px 12px; border-bottom:1px solid var(--line);
}
.pk-card.dragging .pk-head{cursor:grabbing}
.pk-grip{
  flex:none; margin-top:5px; width:11px; color:var(--line);
  display:grid; grid-template-columns:repeat(2,3px); gap:2px;
}
.pk-grip i{width:3px; height:3px; border-radius:50%; background:currentColor}
.pk-head:hover .pk-grip{color:var(--muted)}
.pk-head h3{margin:0; font-size:17px; font-weight:600; letter-spacing:-.01em}
.pk-head p{margin:3px 0 0; font-size:12.5px; color:var(--muted); font-family:"IBM Plex Mono",monospace}
.pk-x{
  margin-left:auto; font:inherit; font-size:20px; line-height:1; cursor:pointer; padding:2px 8px 5px;
  border:1px solid var(--line); border-radius:2px; background:var(--surface-2); color:var(--ink-2);
}
.pk-row{display:flex; flex-wrap:wrap; gap:10px 16px; align-items:center}
.pk-row > .lbl{font-size:10.5px; letter-spacing:.11em; text-transform:uppercase; color:var(--muted); font-weight:600}
#pk-sev .chip .n{
  display:inline-block; margin-left:6px; font-variant-numeric:tabular-nums;
  font-size:11px; color:var(--muted);
}
#pk-sev .chip[aria-pressed="true"] .n{color:inherit}
.pk-check{display:flex; align-items:center; gap:6px; font-size:12.5px; color:var(--ink-2); cursor:pointer}
#pk-out{
  font-family:"IBM Plex Mono",monospace; font-size:13px; line-height:1.7; color:var(--ink);
  background:var(--surface-2); border:1px solid var(--line); border-radius:2px;
  padding:11px 12px; width:100%; min-height:190px; resize:vertical;
}
.pk-foot{display:flex; flex-wrap:wrap; gap:10px; align-items:center}
.pk-foot .n{font-size:12.5px; color:var(--muted); font-variant-numeric:tabular-nums}
.pk-btn{
  font:inherit; font-size:13px; font-weight:600; cursor:pointer; padding:8px 18px;
  border:1px solid var(--accent); border-radius:2px; background:var(--accent); color:var(--surface);
}
.pk-btn[disabled]{opacity:.45; cursor:not-allowed}
.pk-btn.ghost{background:var(--surface-2); color:var(--accent-ink)}
.pk-msg{font-size:12.5px; color:var(--accent-ink); font-weight:600}
footer{font-size:12.5px; color:var(--muted); border-top:1px solid var(--line); padding-top:16px; max-width:80ch}
footer a{color:var(--accent-ink)}
.empty{padding:36px; text-align:center; color:var(--muted)}
@media (max-width:720px){
  .wrap{padding:20px 14px 56px}
  .title{max-width:none}
}
"""

JS = r"""
const D = window.__DATA__;
const R=D.rows, B=D.bul, LN=D.lppName;
const SEVK={Critical:'c',High:'h',Medium:'m',Low:'l'};
const esc=s=>String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));

const $=id=>document.getElementById(id);
function cveline(s){
  const a=s.split('; ');
  if(a.length<=5) return esc(s);
  return esc(a.slice(0,5).join('; '))+' <span style="opacity:.7">他 '+(a.length-5)+' 件</span>';
}
let state={rel:'',lpp:'',sev:new Set(),kind:'',q:'',limit:200};

function match(r){
  const b=B[r[4]];
  if(state.rel && r[0]!==state.rel) return false;
  if(state.lpp && r[1]!==state.lpp) return false;
  if(state.sev.size && !state.sev.has(b[3])) return false;
  if(state.kind && r[3]!==state.kind) return false;
  if(state.q){
    const q=state.q.toLowerCase();
    if(!(r[2].toLowerCase().includes(q) || r[1].toLowerCase().includes(q) ||
         b[0].toLowerCase().includes(q) || b[4].toLowerCase().includes(q) ||
         (LN[r[1]]||'').toLowerCase().includes(q))) return false;
  }
  return true;
}

function render(){
  const hits=R.filter(match);
  $('count').textContent=hits.length.toLocaleString('ja-JP')+' 件 / 全 '+R.length.toLocaleString('ja-JP')+' 件';
  const show=hits.slice(0,state.limit);
  if(!show.length){ $('tbody').innerHTML='<tr><td colspan="6" class="empty">条件に一致する PTF はありません</td></tr>'; $('more').innerHTML=''; return; }
  $('tbody').innerHTML=show.map(r=>{
    const b=B[r[4]];
    const wa=b[5]? '<span class="lbl">Workarounds and Mitigations</span><p>'+esc(b[5])+'</p>':'';
    const rem=b[6]? '<span class="lbl">Remediation/Fixes（原文抜粋）</span><p>'+esc(b[6])+'</p>':'';
    const det=(wa||rem)? '<details class="wa"><summary>'+(b[5]?'回避策あり・詳細':'詳細')+'</summary>'+wa+rem+'</details>':'';
    return '<tr>'+
      '<td class="rel">'+esc(r[0])+(r[9]?'<span class="est" title="'+esc(r[9])+'">補完</span>':'')+'</td>'+
      '<td class="lpp">'+esc(r[1])+'<small>'+esc(LN[r[1]]||'')+(r[7]?' / '+esc(r[7]):'')+(r[5]?' / v'+esc(r[5]):'')+'</small></td>'+
      '<td class="ptf">'+esc(r[2])+'<div class="kind">'+(r[3]==='G'?'グループPTF':'個別PTF')+'</div></td>'+
      '<td><span class="sev sev-'+esc(b[3])+'">'+esc(b[3])+'</span></td>'+
      '<td class="date">'+esc(b[2])+'</td>'+
      '<td class="title"><a href="'+esc(b[1])+'" target="_blank" rel="noopener noreferrer">'+esc(b[0])+'</a>'+
      '<span class="cve">'+cveline(b[4])+'</span>'+det+'</td>'+
    '</tr>';
  }).join('');
  $('more').innerHTML = hits.length>state.limit
    ? '<div class="more"><button class="load" id="loadmore">さらに '+Math.min(400,hits.length-state.limit)+' 件を表示（残り '+(hits.length-state.limit).toLocaleString('ja-JP')+' 件）</button></div>'
    : '';
  const lm=$('loadmore');
  if(lm) lm.onclick=()=>{state.limit+=400; render();};
}

function reset(){ state.limit=200; render(); }

$('f-rel').onchange=e=>{state.rel=e.target.value; reset();};
$('f-lpp').onchange=e=>{state.lpp=e.target.value; reset();};
$('f-kind').onchange=e=>{state.kind=e.target.value; reset();};
$('f-q').oninput=e=>{state.q=e.target.value.trim(); reset();};
document.querySelectorAll('.chip[data-sev]').forEach(btn=>{
  btn.onclick=()=>{
    const s=btn.dataset.sev;
    if(state.sev.has(s)) state.sev.delete(s); else state.sev.add(s);
    btn.setAttribute('aria-pressed', state.sev.has(s));
    reset();
  };
});
$('f-clear').onclick=()=>{
  state={rel:'',lpp:'',sev:new Set(),kind:'',q:'',limit:200};
  $('f-rel').value=''; $('f-lpp').value=''; $('f-kind').value=''; $('f-q').value='';
  document.querySelectorAll('.chip[data-sev]').forEach(b=>b.setAttribute('aria-pressed','false'));
  render();
};
/* ===== PTF 抽出ダイアログ ===== */
const SEV_RANK={Critical:4,High:3,Medium:2,Low:1};
let pick={lpp:'',rel:'',sev:'',group:true};

function ptfsFor(lpp,rel){
  // セル内の PTF を集約。Severity は同一 PTF の最大値（マトリクスの帯と同じ基準）
  const map=new Map();
  for(const r of R){
    if(r[1]!==lpp) continue;
    if(rel && r[0]!==rel) continue;
    const sev=B[r[4]][3];
    const cur=map.get(r[2]);
    if(!cur || SEV_RANK[sev]>SEV_RANK[cur.sev]) map.set(r[2],{ptf:r[2],sev:sev,kind:r[3]});
  }
  return [...map.values()];
}

function renderPick(){
  const all=ptfsFor(pick.lpp,pick.rel);
  const cnt={Critical:0,High:0,Medium:0,Low:0};
  all.forEach(x=>{cnt[x.sev]=(cnt[x.sev]||0)+1;});
  document.querySelectorAll('#pk-sev .chip').forEach(b=>{
    const s=b.dataset.pv;
    b.setAttribute('aria-pressed', String(pick.sev===s));
    b.querySelector('.n').textContent = s? (cnt[s]||0) : all.length;
  });
  const list=all
    .filter(x=>!pick.sev || x.sev===pick.sev)
    .filter(x=>pick.group || x.kind!=='G')
    .map(x=>x.ptf)
    .sort();                                   // MF → SE → SF → SI → SJ → SV の昇順
  $('pk-out').value=list.join(', ');
  $('pk-n').textContent=list.length+' 件';
  $('pk-copy').disabled=!list.length;
}

function openPick(lpp,rel){
  pick={lpp:lpp,rel:rel,sev:'',group:true};
  $('pk-title2').textContent=lpp+(LN[lpp]?'  '+LN[lpp]:'')+'  /  IBM i '+(rel||'全リリース');
  $('pk-group').checked=true;
  $('pk-msg').textContent='';
  renderPick();
  $('pk').hidden=false;
  clampCard();
  $('pk-close').focus({preventScroll:true});
}
function closePick(){ $('pk').hidden=true; }

/* --- ヘッダーをつかんで移動 --- */
const card=document.querySelector('.pk-card');
const head=document.querySelector('.pk-head');
let drag=null, placed=null;

function place(x,y){
  const r=card.getBoundingClientRect();
  const nx=Math.min(Math.max(8, x), Math.max(8, innerWidth - r.width - 8));
  const ny=Math.min(Math.max(8, y), Math.max(8, innerHeight - r.height - 8));
  card.style.position='fixed';
  card.style.margin='0';
  card.style.left=nx+'px';
  card.style.top=ny+'px';
  placed={x:nx,y:ny};
}
function clampCard(){ if(placed) place(placed.x, placed.y); }

head.addEventListener('pointerdown', e=>{
  if(e.target.closest('button')) return;      // 閉じるボタンはドラッグしない
  const r=card.getBoundingClientRect();
  drag={dx:e.clientX-r.left, dy:e.clientY-r.top};
  place(r.left, r.top);
  card.classList.add('dragging');
  head.setPointerCapture(e.pointerId);
  e.preventDefault();
});
head.addEventListener('pointermove', e=>{
  if(drag) place(e.clientX-drag.dx, e.clientY-drag.dy);
});
function endDrag(e){
  if(!drag) return;
  drag=null;
  card.classList.remove('dragging');
  try{ head.releasePointerCapture(e.pointerId); }catch(err){}
}
head.addEventListener('pointerup', endDrag);
head.addEventListener('pointercancel', endDrag);
addEventListener('resize', clampCard);

document.querySelectorAll('#pk-sev .chip').forEach(b=>{
  b.onclick=()=>{ pick.sev=b.dataset.pv; renderPick(); };
});
$('pk-group').onchange=e=>{ pick.group=e.target.checked; renderPick(); };
$('pk-close').onclick=closePick;
document.addEventListener('keydown',e=>{ if(e.key==='Escape' && !$('pk').hidden) closePick(); });
$('pk-copy').onclick=async()=>{
  const t=$('pk-out');
  try{ await navigator.clipboard.writeText(t.value); }
  catch(err){ t.select(); document.execCommand('copy'); }
  $('pk-msg').textContent='クリップボードにコピーしました';
  setTimeout(()=>{ $('pk-msg').textContent=''; },2500);
};
$('pk-filter').onclick=()=>{
  state.lpp=pick.lpp; state.rel=pick.rel; state.limit=200;
  state.sev = pick.sev? new Set([pick.sev]) : new Set();
  $('f-lpp').value=pick.lpp; $('f-rel').value=pick.rel;
  document.querySelectorAll('.chip[data-sev]').forEach(b=>
    b.setAttribute('aria-pressed', String(state.sev.has(b.dataset.sev))));
  closePick(); render();
  $('detail').scrollIntoView({behavior:'smooth',block:'start'});
};

document.querySelectorAll('td[data-cell]').forEach(td=>{
  td.tabIndex=0;
  td.setAttribute('role','button');
  const [lpp,rel]=td.dataset.cell.split('|');
  td.setAttribute('aria-label', lpp+' '+(rel||'全リリース')+' の PTF を一覧');
  const go=()=>openPick(lpp, rel);
  td.onclick=go;
  td.onkeydown=e=>{ if(e.key==='Enter'||e.key===' '){ e.preventDefault(); go(); } };
});
render();
"""


def sev_bar(sev):
    tot = sum(sev.get(s, 0) for s in SEV)
    if not tot:
        return ''
    seg = ''.join('<i class="%s" style="width:%.4f%%"></i>' % (SEVK[s], 100.0 * sev.get(s, 0) / tot)
                  for s in SEV if sev.get(s))
    return '<div class="bar">%s</div>' % seg


SEVK = {'Critical': 'c', 'High': 'h', 'Medium': 'm', 'Low': 'l'}

out = io.StringIO()
w = out.write
st = payload['stats']
w('<title>IBM i PTF セキュリティ台帳</title>\n')
w('<link rel="preconnect" href="https://fonts.googleapis.com">\n')
w('<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n')
w('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
  'family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;600&display=swap">\n')
w('<style>%s</style>\n' % CSS)
w('<div class="wrap">\n')

w('<header>\n')
w('<div class="eyebrow">IBM Product Security Incident Response · Security Bulletins</div>\n')
w('<h1>IBM i セキュリティ速報 PTF 台帳</h1>\n')
w('<p class="lede">IBM の <a href="https://www.ibm.com/support/pages/bulletin/search?q=IBM%%20i" '
  'target="_blank" rel="noopener noreferrer">Security Bulletin 検索</a>で「IBM i」に該当する '
  '%d 件の速報から、対象ライセンスプログラムと IBM i リリースごとの PTF 番号・Severity・公開日を '
  '抽出しました（%s 〜 %s 公開分）。</p>\n' % (st['bulletins'], st['from'], st['to']))
w('<div class="statbar">\n')
for label, val in (('速報', st['bulletins']), ('PTF 番号（ユニーク）', st['ptf']),
                   ('CVE', st['cves']), ('明細行', st['rows'])):
    w('<div class="stat"><b>%s</b><span>%s</span></div>\n' % (format(val, ','), label))
sv = payload['sevTotal']
for s in SEV:
    w('<div class="stat"><b>%s</b><span>%s の速報</span></div>\n' % (sv.get(s, 0), s))
w('</div>\n</header>\n')

# --- マトリクス ---
w('<section>\n<h2>ライセンスプログラム × IBM i リリース</h2>\n')
w('<p class="note">セル上段はユニーク PTF 数、下段の帯は該当 PTF の Severity 構成（'
  '<span style="color:var(--crit)">Critical</span> / <span style="color:var(--high)">High</span> / '
  '<span style="color:var(--med)">Medium</span> / <span style="color:var(--low)">Low</span>）。'
  'セルをクリックすると、そのライセンスプログラム／リリースに適用すべき PTF 番号を '
  'Severity 別に取り出せます。右端の「計」はリリース横断で重複を除いた'
  'ユニーク PTF 数のため、行内の合計とは一致しません。'
  'リリース欄の「補完」は速報にリリースの明記が無く、同じ表の他行や製品タクソノミーから'
  '補ったものです。</p>\n')
w('<div class="scroll"><table class="mx"><thead><tr><th>ライセンスプログラム</th>')
for v in payload['vers']:
    w('<th class="num">%s</th>' % html.escape(v))
w('<th class="num">計</th></tr></thead><tbody>\n')
for l in payload['lpps']:
    w('<tr><td class="lppcell"><b>%s</b><small>%s</small></td>' % (
        html.escape(l), html.escape(payload['lppName'].get(l, ''))))
    for v in payload['vers']:
        m = payload['matrix'].get('%s|%s' % (l, v))
        if not m:
            w('<td class="num zero">–</td>')
        else:
            w('<td class="num" data-cell="%s|%s">%d%s</td>' % (
                html.escape(l), html.escape(v), m['ptf'], sev_bar(m['sev'])))
    w('<td class="num" data-cell="%s|"><b>%d</b></td></tr>\n' % (html.escape(l), lpp_total[l]))
w('</tbody></table></div>\n</section>\n')

# --- 明細 ---
w('<section id="detail">\n<h2>PTF 明細</h2>\n')
w('<div class="filters">\n')
w('<div class="field"><label for="f-rel">IBM i リリース</label><select id="f-rel"><option value="">すべて</option>')
for v in payload['vers']:
    w('<option value="%s">%s</option>' % (html.escape(v), html.escape(v)))
w('</select></div>\n')
w('<div class="field"><label for="f-lpp">ライセンスプログラム</label><select id="f-lpp"><option value="">すべて</option>')
for l in sorted(payload['lpps']):
    w('<option value="%s">%s %s</option>' % (html.escape(l), html.escape(l),
                                             html.escape(payload['lppName'].get(l, ''))))
w('</select></div>\n')
w('<div class="field"><label for="f-kind">PTF 種別</label><select id="f-kind">'
  '<option value="">すべて</option><option value="P">個別 PTF</option>'
  '<option value="G">グループ PTF</option></select></div>\n')
w('<div class="field"><label>Severity</label><div class="chips">')
for s in SEV:
    w('<button class="chip" type="button" data-sev="%s" aria-pressed="false">%s</button>' % (s, s))
w('</div></div>\n')
w('<div class="field"><label for="f-q">検索（PTF / CVE / 製品 / 表題）</label>'
  '<input type="search" id="f-q" placeholder="SJ11027, CVE-2026-64958, OpenSSH …"></div>\n')
w('<div class="field"><label>&nbsp;</label><button class="chip" type="button" id="f-clear">条件をクリア</button></div>\n')
w('<div class="spacer"></div><div class="count" id="count"></div>\n')
w('</div>\n')
w('<div class="scroll"><table class="dt"><thead><tr>'
  '<th>リリース</th><th>ライセンスプログラム</th><th>PTF 番号</th>'
  '<th>Severity</th><th>Publish Date</th><th>速報 / CVE</th>'
  '</tr></thead><tbody id="tbody"></tbody></table></div>\n')
w('<div id="more"></div>\n</section>\n')

# --- PTF 抽出ダイアログ ---
w('<div id="pk" hidden role="dialog" aria-labelledby="pk-title">\n')
w('<div class="pk-card">\n')
w('<div class="pk-head" title="ここをドラッグして移動できます">'
  '<span class="pk-grip" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i><i></i></span>'
  '<div><h3 id="pk-title">リストする PTF の選択</h3><p id="pk-title2"></p></div>'
  '<button class="pk-x" type="button" id="pk-close" aria-label="閉じる">&times;</button></div>\n')
w('<div class="pk-row" id="pk-sev"><span class="lbl">Severity</span>')
for s, lab in (('', 'すべて'), ('Critical', 'Critical'), ('High', 'High'),
               ('Medium', 'Medium'), ('Low', 'Low')):
    w('<button class="chip" type="button" data-pv="%s" aria-pressed="%s">%s'
      '<span class="n"></span></button>' % (s, 'true' if s == '' else 'false', lab))
w('</div>\n')
w('<div class="pk-row"><label class="pk-check">'
  '<input type="checkbox" id="pk-group" checked>グループ PTF（SF99xxx）を含める</label>'
  '<span class="lbl" style="margin-left:auto">昇順・カンマ区切り</span></div>\n')
w('<textarea id="pk-out" readonly spellcheck="false" '
  'aria-label="抽出した PTF 番号の一覧"></textarea>\n')
w('<div class="pk-foot">'
  '<button class="pk-btn" type="button" id="pk-copy">コピー</button>'
  '<button class="pk-btn ghost" type="button" id="pk-filter">この条件で明細を絞り込む</button>'
  '<span class="n" id="pk-n"></span>'
  '<span class="pk-msg" id="pk-msg" role="status"></span></div>\n')
w('<p class="note">Severity は同一 PTF が複数の速報に現れる場合、最も高い値で分類しています'
  '（マトリクスの帯と同じ基準）。上位の Severity に分類された PTF は下位の一覧には現れません。</p>\n')
w('</div>\n</div>\n')

w('<footer>\n')
w('<p>出典: IBM Security Bulletin 検索 API（<code>/support/pages/securityapp/api/search?q=IBM i</code>）'
  'および各速報ページの Remediation/Fixes・Workarounds and Mitigations セクション。'
  'Severity は速報に含まれる CVE のうち最も高い値を採用しています。'
  'ライセンスプログラムは表の見出し表記を優先し、記載が無い場合は本文・製品名・PTF 接頭辞から推定した'
  '旨をライセンスプログラム欄に併記しています。'
  '速報の表でその行の IBM i リリース欄が空欄の場合（Db2 Web Query など製品バージョンが主軸の表）は、'
  '同じ表の他行が示すリリース範囲、またはページ末尾の製品タクソノミー（IBM 自身の分類）で補完し、'
  'リリース欄に「補完」と表示しています（ホバーで根拠が出ます）。'
  '取得日: %s。適用前に必ず各速報の原文を確認してください。</p>\n' % st['to'])
w('</footer>\n')

w('<script>window.__DATA__=%s;</script>\n' % json.dumps(payload, ensure_ascii=False, separators=(',', ':')))
w('<script>%s</script>\n' % JS)
w('</div>\n')

body = out.getvalue()
open('ibmi_ptf.html', 'w', encoding='utf-8').write(body)

# ブラウザで直接開ける単体版
STANDALONE = ('<!doctype html>\n<html lang="ja">\n<head>\n<meta charset="utf-8">\n'
              '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
              '</head>\n<body>\n%s\n</body>\n</html>\n')
open('preview.html', 'w', encoding='utf-8').write(STANDALONE % body)
print('wrote ibmi_ptf.html / preview.html  (%.1f KB)' % (len(body) / 1024))
