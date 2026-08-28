# -*- coding: utf-8 -*-
import re, json, os
from bs4 import BeautifulSoup

SEV_ORDER = {'Critical': 4, 'High': 3, 'Medium': 2, 'Low': 1, '': 0, None: 0}
PTF_RE   = re.compile(r'\b(?!SF99)[SM][A-Z]\d{5}\b')
GRP_RE   = re.compile(r'\bSF99\d{3}\b')
IVER_RE  = re.compile(r'(?<![\d.])([4-7]\.\d(?:\.\d)?)(?![\d.])')  # IBM i リリース
OVER_RE  = re.compile(r'\bV\d+R\d+(?:M\d+)?\b')                   # 旧表記 V5R4 等
PVER_RE  = re.compile(r'(?<![\d.])(\d+(?:\.\d+){1,3})(?![\d.])')  # 製品バージョン
LPP_RE   = re.compile(r'\b(5(?:7\d{2}|733|798|76\d))[- ]?([A-Z0-9]{3})\b')


def norm(s):
    return re.sub(r'\s+', ' ', s.replace(' ', ' ')).strip()


def is_link(c):
    return bool(re.match(r'https?://', c) or re.search(r'(ibm\.com|fixcentral|fix-information)', c, re.I))


def grid(tbl):
    """rowspan/colspan を展開して矩形グリッド化"""
    g, occupied = [], {}
    trs = [tr for tr in tbl.find_all('tr') if tr.find_parent('table') is tbl]
    for ri, tr in enumerate(trs):
        while len(g) <= ri:
            g.append({})
        ci = 0
        for cell in tr.find_all(['td', 'th']):
            while (ri, ci) in occupied:
                ci += 1
            txt = norm(cell.get_text(' '))
            rs = int(cell.get('rowspan') or 1)
            cs = int(cell.get('colspan') or 1)
            for dr in range(rs):
                for dc in range(cs):
                    occupied[(ri + dr, ci + dc)] = True
                    while len(g) <= ri + dr:
                        g.append({})
                    g[ri + dr][ci + dc] = txt
            ci += cs
    width = max((max(r) + 1 if r else 0) for r in g) if g else 0
    return [[r.get(i, '') for i in range(width)] for r in g]


VERHEAD_RE = re.compile(r'^(?:IBM i\s*)?([4-7]\.\d(?:\.\d)?|V\d+R\d+(?:M\d+)?)$', re.I)


def col_roles(header):
    """列インデックス -> 役割（'vc:7.4' はその列自体が特定リリースの PTF 列）"""
    roles = {}
    for i, h in enumerate(header):
        hl = h.lower()
        if not hl:
            continue
        mv = VERHEAD_RE.match(h.strip())
        if mv:                      # 見出しがリリースそのもの（CVE×リリースの表）
            roles[i] = 'vc:' + mv.group(1)
        elif re.search(r'download|link', hl):
            roles[i] = 'link'
        elif re.search(r'ibm i (release|version)|^release$|^ibm i$', hl):
            roles[i] = 'ibmi'
        elif re.search(r'ptf|fix number|fix pack|remediation|level', hl):
            roles[i] = 'ptf'
        elif re.search(r'release|version', hl):
            roles[i] = 'prodver'
        elif re.search(r'product|component|offering', hl):
            roles[i] = 'product'
    return roles


def promote_ibmi(roles, rows, header):
    """IBM i リリース列が無い表では、実際に 7.x を含む Version 列だけを昇格する"""
    if 'ibmi' in roles.values():
        return roles
    for i, r in sorted(roles.items()):
        if r != 'prodver':
            continue
        vals = [row[i] for row in rows if row is not header and i < len(row)]
        if any(IVER_RE.search(c) or OVER_RE.search(c) for c in vals):
            roles[i] = 'ibmi'
            break
    return roles


def scan_table(tbl):
    rows = [r for r in grid(tbl) if any(r)]
    if not rows:
        return []
    header = None
    for r in rows:
        j = ' '.join(r)
        if PTF_RE.search(j) or GRP_RE.search(j):
            continue
        # 通常の見出し行、または「IBM i 7.4 | IBM i 7.3 …」のようなリリース見出し行
        if re.search(r'PTF|Release|Version|Product|Fix', j, re.I) \
           or sum(1 for c in r if VERHEAD_RE.match(c.strip())) >= 2:
            header = r
            break
    roles = promote_ibmi(col_roles(header), rows, header) if header else {}
    ver_cols = {i: v[3:] for i, v in roles.items() if v.startswith('vc:')}
    ptf_cols = [i for i, r in roles.items() if r == 'ptf'] + list(ver_cols)
    # 表全体が対象としている IBM i リリース（空欄行の補完に使う）
    ibmi_col = next((i for i, v in roles.items() if v == 'ibmi'), None)
    table_rels = []
    if ibmi_col is not None:
        for r in rows:
            if r is header or ibmi_col >= len(r):
                continue
            table_rels += IVER_RE.findall(r[ibmi_col]) + OVER_RE.findall(r[ibmi_col])
        table_rels = list(dict.fromkeys(table_rels))
    out = []
    for r in rows:
        if r is header:
            continue
        j = ' '.join(r)
        if not (PTF_RE.search(j) or GRP_RE.search(j)):
            continue
        ibmi, pver, prod = [], [], None
        for i, c in enumerate(r):
            role = roles.get(i)
            if role == 'ibmi':
                ibmi += IVER_RE.findall(c) + OVER_RE.findall(c)
            elif role == 'prodver':
                pver += PVER_RE.findall(c) + OVER_RE.findall(c)
            elif role == 'product':
                prod = c or prod
        if not roles:            # ヘッダー無し: 行内の非PTF・非リンクセルから推測
            for c in r:
                if is_link(c) or PTF_RE.search(c) or GRP_RE.search(c):
                    continue
                ibmi += IVER_RE.findall(c) + OVER_RE.findall(c)
                if prod is None and re.search(r'IBM|Db2|WebSphere|Java|HTTP|Access', c, re.I) \
                   and not IVER_RE.search(c):
                    prod = c
        cand = ptf_cols if ptf_cols else [i for i in range(len(r)) if roles.get(i) != 'link']
        for i in cand:
            c = r[i] if i < len(r) else ''
            if is_link(c):
                continue
            lbl = header[i] if header and i < len(header) else ''
            iv = [ver_cols[i]] if i in ver_cols else list(dict.fromkeys(ibmi))
            src = ''
            if not iv and table_rels:    # 行のリリース欄が空 -> 同じ表の他行の範囲で補完
                iv, src = list(table_rels), '同じ表の他行から補完'
            pv = list(dict.fromkeys(pver))
            for m in PTF_RE.findall(c):
                out.append([prod, iv, pv, m, lbl, 'PTF', src])
            for m in GRP_RE.findall(c):
                out.append([prod, iv, pv, m, lbl, 'GROUP', src])
    return out


URL_RE = re.compile(r'(?:https?|ftp)://\S+')
REL_KW = re.compile(r'\bReleases?\s*[:\-]?\s*(?=[\dV])', re.I)
RNUM_RE = re.compile(r'\bR(\d)(\d)(\d)\b')          # R720 -> 7.2 / R540 -> 5.4
NOISE = re.compile(r'^[\s\-–—=*_.]+$')
# 見出し行から製品を判定する（明示的な製品番号が無い旧形式向け）
LPP_KEYWORD = [
    (re.compile(r'Access Client Solutions', re.I), '5733-XJ1'),
    (re.compile(r'Access for Windows', re.I), '5770-XE1'),
    (re.compile(r'\bJava', re.I), '5770-JV1'),
    (re.compile(r'HTTP\s+server', re.I), '5770-DG1'),
    (re.compile(r'Web Query', re.I), '5733-WQX'),
    (re.compile(r'OmniFind', re.I), '5733-OMF'),
    (re.compile(r'OpenSSH|OpenSSL|PASE', re.I), '5733-SC1'),
    (re.compile(r'\bOS\b|Operating System|Licensed Internal Code|\bLIC\b'), '5770-SS1'),
]


def releases_in(line):
    """行に現れる IBM i リリース表記を拾う"""
    out = []
    for m in RNUM_RE.finditer(line):
        a, b, c = m.groups()
        out.append('%s.%s' % (a, b) if c == '0' else '%s.%s.%s' % (a, b, c))
    out += IVER_RE.findall(line) + OVER_RE.findall(line)
    return list(dict.fromkeys(out))


def scan_text(raw):
    """
    旧形式の自由記述を状態を持って走査する。
      - 製品見出し（例: "IBM i Java:" / "5770DG1"）で LPP 文脈を切り替える
      - "Release 7.1 -" のようにリリースだけの行は、後続の PTF 行に適用する
    """
    entries = []
    cur_lpp, pending = None, []
    for raw_line in raw.replace(' ', ' ').split('\n'):
        full = norm(raw_line)
        line = norm(URL_RE.sub(' ', raw_line))   # 見出し/リリース判定は URL を除いた行
        if not full or NOISE.match(full):
            continue
        # PTF 番号が URL のパス内に書かれている場合があるため元の行から拾う
        ptfs, grps = PTF_RE.findall(full), GRP_RE.findall(full)
        # --- LPP 文脈の更新 ---
        lpps = ['%s-%s' % m for m in LPP_RE.findall(line)]
        if lpps:
            cur_lpp = next((x for x in lpps if x.startswith('5770')), lpps[0])
        elif not (ptfs or grps) and len(line) <= 70:
            for pat, code in LPP_KEYWORD:      # 短い見出し行のみ製品判定に使う
                if pat.search(line):
                    cur_lpp = code
                    break
        rels = releases_in(REL_KW.sub('', line))
        if not (ptfs or grps):
            if rels and len(line) < 220:
                pending = rels          # リリースのみの行 -> 後続 PTF の文脈
            continue
        use = rels or pending
        lbl = ('本文 ' + cur_lpp) if cur_lpp else ''
        for m in ptfs:
            entries.append([None, list(use), [], m, lbl, 'PTF', ''])
        for m in grps:
            entries.append([None, list(use), [], m, lbl, 'GROUP', ''])
    return entries


def scan_div(div):
    if div is None:
        return [], []
    for t in div.find_all('h2'):
        t.decompose()
    entries, ctx = [], []
    for tbl in div.find_all('table'):
        if tbl.find('table'):        # 入れ子の外側表 -> 製品/バージョンの文脈のみ採取
            for r in grid(tbl):
                j = ' '.join(r)
                if len(r) >= 2 and r[0] and r[1] and not PTF_RE.search(j) \
                   and not re.search(r'Product\(s\)|Version\(s\)|PTF|Release', ' '.join(r[:2]), re.I) \
                   and re.match(r'^[\dVv][\d.RrMm –—-]*$', r[1]):
                    ctx.append((r[0], r[1]))
            continue
        entries += scan_table(tbl)
    if not entries:                  # 表が無い -> 行テキストを文脈付きで走査
        entries += scan_text(div.get_text('\n', strip=True))
    return entries, ctx


def taxonomy_releases(soup):
    """ページ末尾の製品タクソノミー（IBM 自身の分類）から IBM i リリースを取る"""
    div = soup.find(id='taxonomy-source')
    if div is None:
        return []
    try:
        items = json.loads(div.get_text())
    except Exception:
        return []
    out = []
    for it in items if isinstance(items, list) else []:
        plat = ' '.join(p.get('label', '') for p in (it.get('Platform') or [])
                        if isinstance(p, dict))
        prod = (it.get('Product') or {}).get('label', '') if isinstance(it.get('Product'), dict) else ''
        if 'IBM i' not in plat and 'IBM i' not in prod:
            continue
        for tok in re.split(r'[,\s]+', it.get('Version') or ''):
            if IVER_RE.fullmatch(tok) or OVER_RE.fullmatch(tok):
                out.append(tok)
    return sorted(set(out), reverse=True)


def strip_head(t, head):
    t = norm(t)
    return norm(t[len(head):]) if t.lower().startswith(head.lower()) else t


def parse_page(nid):
    p = 'pages/%s.html' % nid
    if not os.path.exists(p):
        return '', '', [], [], '', []
    s = BeautifulSoup(open(p, encoding='utf-8', errors='replace').read(), 'lxml')
    tax = taxonomy_releases(s)
    secs = {}
    for cls, tag in (('field--name-field-remediation-fixes', 'Remediation'),
                     ('field--name-field-workarounds-and-mitigation', 'Workarounds')):
        div = s.find('div', class_=cls)
        secs[tag] = (norm(div.get_text(' ')) if div is not None else '',) + tuple(scan_div(div))
    rem = strip_head(secs['Remediation'][0], 'Remediation/Fixes')
    wa = strip_head(secs['Workarounds'][0], 'Workarounds and Mitigations')
    rem = '' if rem.lower() in ('none', 'none.') else rem
    wa = '' if wa.lower() in ('none', 'none.', '') else wa
    for tag in ('Remediation', 'Workarounds'):
        if secs[tag][1]:
            return rem, wa, secs[tag][1], secs[tag][2], tag, tax
    # 最終手段: Summary / Vulnerability Details に PTF が書かれている旧速報
    for cls, tag in (('field--name-field-summary', 'Summary'),
                     ('field--name-field-vulnerability-details', 'Vulnerability Details')):
        div = s.find('div', class_=cls)
        if div is None:
            continue
        e = scan_text(div.get_text('\n', strip=True))
        if e:
            return rem, wa, e, secs['Remediation'][2], tag, tax
    return rem, wa, [], secs['Remediation'][2] + secs['Workarounds'][2], '', tax


# ---- API データ ----
api = json.load(open('api_search.txt', encoding='utf-8'))
bulletins = {}
for r in api['results']:
    b = bulletins.setdefault(r['nid'], {
        'nid': r['nid'], 'title': norm(r['title']), 'url': r['field_published_url'],
        'pub_date': r['field_pub_date'], 'modified': r['modified_date'],
        'pid': r['field_offering_pid_number'], 'cves': {},
        '_aff': r.get('field_affected_products') or '',
    })
    b['cves'][r['field_cve_id']] = r['field_cvss_base_score']


def parse_affected(html):
    prods = []
    if not html:
        return prods
    s = BeautifulSoup(html, 'lxml')
    for tr in s.find_all('tr'):
        cells = [norm(td.get_text(' ')) for td in tr.find_all(['td', 'th'])]
        if len(cells) >= 2 and not re.search(r'Affected Product|Version\(s\)', ' '.join(cells), re.I):
            for v in re.split(r'[,、/]|\band\b', cells[1]):
                if v.strip():
                    prods.append((cells[0], v.strip()))
    if not prods:
        t = norm(s.get_text(' '))
        m = re.search(r'of\s+(IBM [A-Za-z0-9 ®™]+?)\s+(?:are|is)\b', t)
        pname = norm(m.group(1)) if m else 'IBM i'
        for v in dict.fromkeys(IVER_RE.findall(t) + OVER_RE.findall(t)):
            prods.append((pname, v))
    return prods


for nid, b in bulletins.items():
    b['affected'] = parse_affected(b.pop('_aff'))
    b['severity'] = max(b['cves'].values(), key=lambda s: SEV_ORDER.get(s, 0)) if b['cves'] else ''
    rem, wa, entries, ctx, src, tax = parse_page(nid)
    seen, uniq = set(), []
    for e in entries:
        k = (e[3], tuple(e[1]), tuple(e[2]), e[4])
        if k not in seen:
            seen.add(k)
            uniq.append(e)
    b.update(remediation_text=rem, workaround_text=wa, entries=uniq, ctx=ctx, source=src, tax=tax,
             lpps=sorted({'%s-%s' % (a, c) for a, c in LPP_RE.findall(rem or '')}))

json.dump(bulletins, open('bulletins.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
no = [b for b in bulletins.values() if not b['entries']]
print('速報:', len(bulletins), '/ PTF抽出なし:', len(no))
for b in no:
    print('  ', b['nid'], b['pub_date'], b['title'][:55], '|',
          (b['remediation_text'] or b['workaround_text'])[:70])
