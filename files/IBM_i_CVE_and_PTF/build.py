# -*- coding: utf-8 -*-
import json, re, csv, collections

LPP_RE = re.compile(r'\b(5(?:7\d{2}|733|798|76\d))[- ]?([A-Z0-9]{3})\b')
SEV_ORDER = {'Critical': 4, 'High': 3, 'Medium': 2, 'Low': 1, '': 0}
LPP_NAME = {
    '5770-SS1': 'IBM i オペレーティングシステム',
    '5770-999': 'Licensed Internal Code',
    '5770-JV1': 'IBM Developer Kit for Java',
    '5760-JV1': 'IBM Developer Kit for Java',
    '5761-JV1': 'IBM Developer Kit for Java',
    '5770-DG1': 'IBM HTTP Server for i',
    '5733-SC1': 'IBM Portable Utilities for i (OpenSSH/OpenSSL)',
    '5770-SC1': 'IBM Portable Utilities for i',
    '5770-DBM': 'IBM Db2 Mirror for i',
    '5733-WQX': 'IBM Db2 Web Query for i',
    '5770-TC1': 'TCP/IP Connectivity Utilities for i',
    '5770-PT1': 'IBM Performance Tools for i',
    '5798-FAX': 'IBM Facsimile Support for i',
    '5733-ARE': 'IBM Administration Runtime Expert for i',
    '5770-WDS': 'IBM Rational Development Studio for i',
    '5733-OMF': 'OmniFind Text Search Server for Db2 for i',
    '5770-MG1': 'IBM Managed System Services for i',
    '5770-BR1': 'Backup Recovery and Media Services for i',
    '5733-CY3': 'IBM Cryptographic Device Manager',
    '5770-TS1': 'IBM Transform Services for i',
    '5770-SM1': 'IBM System Manager for i',
    '5770-HAS': 'IBM PowerHA SystemMirror for i',
    '5770-JS1': 'IBM Advanced Job Scheduler for i',
    '5770-UME': 'Universal Manageability Enablement for i',
    '5770-XE1': 'IBM i Access for Windows',
    '5733-XJ1': 'IBM Toolbox for Java',
    '5770-XW1': 'IBM i Access Family',
    '5733-OPS': 'IBM i Open Source Solutions',
    '5770-NAE': 'IBM Network Authentication Enablement for i',
}
# 速報タイトル／本文からのフォールバック推定
TITLE_HINT = [
    (r'Java SDK|Java Technology|IBM SDK, Java', '5770-JV1'),
    (r'HTTP Server', '5770-DG1'),
    (r'OpenSSH|OpenSSL|Portable Utilities|zlib', '5733-SC1'),
    (r'Db2 Web Query|Web Query', '5733-WQX'),
    (r'Db2 Mirror', '5770-DBM'),
    (r'OmniFind', '5733-OMF'),
    (r'Administration Runtime Expert|Application Runtime Expert', '5733-ARE'),
    (r'Licensed Internal Code|firmware', '5770-999'),
]
IVER_OK = re.compile(r'^(?:[4-7]\.\d(?:\.\d)?|V\d+R\d+(?:M\d+)?)$')

b = json.load(open('bulletins.json', encoding='utf-8'))
rows = []
for nid, v in b.items():
    cves = sorted(v['cves'])
    cve_sev = '; '.join('%s (%s)' % (c, v['cves'][c]) for c in cves)
    aff_names = list(dict.fromkeys(p for p, _ in v['affected'])) or ['IBM i']
    aff_vers = list(dict.fromkeys(x for _, x in v['affected']))
    ctx_prod = v['ctx'][0][0] if v.get('ctx') else ''
    ctx_ver = v['ctx'][0][1] if v.get('ctx') else ''
    # 同一速報内で同じ PTF にリリース付きの記載があれば、リリース無しの重複は捨てる
    known = collections.defaultdict(set)
    for e in v['entries']:
        ivs, ptf = e[1], e[3]
        known[ptf] |= {x for x in ivs if IVER_OK.match(x)}
    # どこにもリリースが無い PTF は Affected Products の記載で補う
    aff_rel = [x for _, x in v['affected'] if IVER_OK.match(x)]
    # 最終手段: ページ末尾の製品タクソノミー（IBM 自身の分類）
    tax_rel = [re.sub(r'^([4-7]\.\d)\.0$', r'', x) for x in v.get('tax') or []]
    tax_rel = [x for x in tax_rel if IVER_OK.match(x)]
    for prod, ivers, pvers, ptf, lbl, kind, rel_src in v['entries']:
        valid = [x for x in ivers if IVER_OK.match(x)]
        if not valid and known[ptf]:
            continue                       # リリース付きの行が別にある
        rel_basis = rel_src
        if not valid and aff_rel:
            ivers, rel_basis = aff_rel, '影響製品欄から補完'
        elif not valid and tax_rel:
            ivers, rel_basis = tax_rel, '製品タクソノミーから補完'
        m = LPP_RE.search(lbl or '')
        basis = '本文の製品見出し' if (lbl or '').startswith('本文 ') else '表内表記'
        if m:
            lpp = '%s-%s' % m.groups()
        elif len(v['lpps']) == 1:
            lpp, basis = v['lpps'][0], '本文表記'
        else:
            lpp, basis = '', ''
            for pat, code in TITLE_HINT:
                if re.search(pat, v['title'], re.I):
                    lpp, basis = code, '製品名から推定'
                    break
            if not lpp and re.search(r"PTF.{0,30}to (the )?IBM i",
                                     (v['remediation_text'] or '') + ' ' + (v.get('workaround_text') or ''),
                                     re.I):
                lpp, basis = '5770-SS1', 'OS向けPTFと推定'
            if not lpp and ptf.startswith('M'):
                lpp, basis = '5770-999', 'PTF接頭辞から推定'
            if not lpp and ptf.startswith('SI'):
                lpp, basis = '5770-SS1', 'PTF接頭辞から推定'
        opt = ''
        mo = re.search(r'Option\s*(\d+)', lbl or '')
        if mo:
            opt = 'Option %s' % mo.group(1)
        vs = [x for x in ivers if IVER_OK.match(x)] or ['(記載なし)']
        pname = prod or ctx_prod or (aff_names[0] if aff_names else 'IBM i')
        pv = ', '.join(pvers) or ctx_ver
        for ver in vs:
            rows.append({
                'IBM i リリース': ver,
                '対象プロダクト': pname,
                '製品バージョン': pv,
                'ライセンスプログラム': lpp,
                'ライセンスプログラム名': LPP_NAME.get(lpp, ''),
                'LPP判定根拠': basis,
                'リリース補完': rel_basis,
                'オプション': opt,
                'PTF番号': ptf,
                'PTF種別': 'グループPTF' if kind == 'GROUP' else '個別PTF',
                'Severity': v['severity'],
                'CVE': ', '.join(cves),
                'CVE別Severity': cve_sev,
                'Publish Date': v['pub_date'],
                '最終更新': v['modified'],
                '速報タイトル': v['title'],
                'URL': v['url'],
                '影響バージョン(速報記載)': ', '.join(aff_vers),
                'Workarounds and Mitigations': v.get('workaround_text', ''),
                'Remediation原文': v['remediation_text'],
                'nid': nid,
            })

seen, uniq = set(), []
for r in rows:
    k = (r['IBM i リリース'], r['PTF番号'], r['nid'], r['ライセンスプログラム'])
    if k not in seen:
        seen.add(k)
        uniq.append(r)
rows = sorted(uniq, key=lambda r: (r['Publish Date'], r['nid'], r['IBM i リリース'], r['PTF番号']),
              reverse=True)

with open('ibmi_ptf_severity.csv', 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)
json.dump(rows, open('rows.json', 'w', encoding='utf-8'), ensure_ascii=False)

# ---- 集計: ライセンスプログラム × IBM i リリース ----
VORDER = ['7.6', '7.5', '7.4', '7.3', '7.2', '7.1', '6.1', '5.4', '(記載なし)']


def vkey(x):
    return VORDER.index(x) if x in VORDER else len(VORDER)


agg = collections.defaultdict(lambda: collections.Counter())
ptfset = collections.defaultdict(set)
nidset = collections.defaultdict(set)
sevbyptf = collections.defaultdict(dict)
for r in rows:
    key = (r['ライセンスプログラム'] or '(不明)', r['IBM i リリース'])
    ptfset[key].add(r['PTF番号'])
    nidset[key].add(r['nid'])
    prev = sevbyptf[key].get(r['PTF番号'], '')
    if SEV_ORDER[r['Severity']] > SEV_ORDER[prev]:
        sevbyptf[key][r['PTF番号']] = r['Severity']
for key, d in sevbyptf.items():
    for sev in d.values():
        agg[key][sev] += 1

summary = []
for (lpp, ver), c in agg.items():
    summary.append({
        'ライセンスプログラム': lpp, 'ライセンスプログラム名': LPP_NAME.get(lpp, ''),
        'IBM i リリース': ver, 'PTF数': len(ptfset[(lpp, ver)]),
        '速報件数': len(nidset[(lpp, ver)]),
        'Critical': c['Critical'], 'High': c['High'], 'Medium': c['Medium'], 'Low': c['Low'],
    })
summary.sort(key=lambda s: (-s['PTF数'], s['ライセンスプログラム'], vkey(s['IBM i リリース'])))
with open('summary_lpp_version.csv', 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(summary[0].keys()))
    w.writeheader()
    w.writerows(summary)
json.dump(summary, open('summary.json', 'w', encoding='utf-8'), ensure_ascii=False)

print('明細行:', len(rows), '/ ユニークPTF:', len({r['PTF番号'] for r in rows}),
      '/ 速報:', len({r['nid'] for r in rows}))
print()
hdr = '%-11s %-42s %-9s %5s %4s %4s %4s %4s' % (
    'LPP', '製品名', 'リリース', 'PTF数', 'Cri', 'Hi', 'Med', 'Low')
print(hdr)
print('-' * len(hdr))
for s in sorted(summary, key=lambda s: (s['ライセンスプログラム'], vkey(s['IBM i リリース']))):
    print('%-11s %-42s %-9s %5d %4d %4d %4d %4d' % (
        s['ライセンスプログラム'], s['ライセンスプログラム名'][:40], s['IBM i リリース'],
        s['PTF数'], s['Critical'], s['High'], s['Medium'], s['Low']))
