# -*- coding: utf-8 -*-
"""
IBM i セキュリティ速報 PTF 台帳を最新化する。

  python refresh.py            速報一覧を取得し、新規・更新分のページだけ再取得して再生成
  python refresh.py --full     キャッシュを無視して全速報ページを取り直す
  python refresh.py --offline  ダウンロードせず、手元のキャッシュだけで再生成

生成物:
  ibmi_ptf.html            公開用の静的 HTML（データを埋め込んだ単一ファイル）
  ibmi_ptf_severity.csv    PTF 明細
  summary_lpp_version.csv  ライセンスプログラム × リリース集計
"""
import json, os, sys, runpy, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)

SEARCH_API = 'https://www.ibm.com/support/pages/securityapp/api/search?q=IBM%20i'
NODE_URL = 'https://www.ibm.com/support/pages/node/%s'
UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36')
PAGES, CACHE, SEARCH = 'pages', 'cache.json', 'api_search.txt'

full = '--full' in sys.argv
offline = '--offline' in sys.argv


def get(url, timeout=120):
    req = urllib.request.Request(url, headers={
        'User-Agent': UA,
        'Accept': 'text/html,application/json,*/*',
        'Referer': 'https://www.ibm.com/support/pages/bulletin/search?q=IBM%20i',
    })
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode('utf-8', 'replace')


# ---- 1. 速報一覧（Vue 版検索画面が使っている JSON API）----
if offline:
    print('[1/4] 速報一覧: キャッシュを使用')
else:
    print('[1/4] 速報一覧を取得中 ...', end=' ', flush=True)
    body = get(SEARCH_API)
    json.loads(body)                      # 壊れていたらここで落とす
    open(SEARCH, 'w', encoding='utf-8').write(body)
    print('OK')

api = json.load(open(SEARCH, encoding='utf-8'))
latest = {}
for r in api['results']:
    latest[r['nid']] = r.get('modified_date') or r.get('field_pub_date') or ''
print('      速報 %d 件 / CVE 行 %d 件' % (len(latest), len(api['results'])))

# ---- 2. 更新分の速報ページだけ取得 ----
os.makedirs(PAGES, exist_ok=True)
cache = {}
if os.path.exists(CACHE) and not full:
    cache = json.load(open(CACHE, encoding='utf-8'))

todo = []
for nid, mod in latest.items():
    path = os.path.join(PAGES, nid + '.html')
    stale = (not os.path.exists(path)) or os.path.getsize(path) < 5000 or cache.get(nid) != mod
    if stale:
        todo.append((nid, mod))

if offline:
    missing = [n for n, _ in todo if not os.path.exists(os.path.join(PAGES, n + '.html'))]
    print('[2/4] ページ取得: スキップ（未取得 %d 件）' % len(missing))
else:
    print('[2/4] ページ取得: %d 件（キャッシュ流用 %d 件）' % (len(todo), len(latest) - len(todo)))
    ok, ng = [], []

    def fetch(item):
        nid, mod = item
        try:
            html = get(NODE_URL % nid)
            if len(html) < 5000:
                raise ValueError('too short: %d bytes' % len(html))
            open(os.path.join(PAGES, nid + '.html'), 'w', encoding='utf-8').write(html)
            return nid, mod, None
        except Exception as e:                                   # noqa: BLE001
            return nid, mod, e

    if todo:
        with ThreadPoolExecutor(max_workers=6) as ex:
            for i, (nid, mod, err) in enumerate(ex.map(fetch, todo), 1):
                if err:
                    ng.append((nid, err))
                else:
                    ok.append(nid)
                    cache[nid] = mod
                if i % 25 == 0 or i == len(todo):
                    print('      %d/%d' % (i, len(todo)), end='\r', flush=True)
        print()
    json.dump(cache, open(CACHE, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    if ng:
        print('      取得失敗 %d 件:' % len(ng))
        for nid, err in ng[:10]:
            print('        %s %s' % (nid, err))

# ---- 3. 解析 → 4. HTML 生成 ----
print('[3/4] 速報ページを解析中 ...')
runpy.run_path('extract.py', run_name='__main__')
runpy.run_path('build.py', run_name='__main__')
print('[4/4] HTML を生成中 ...')
runpy.run_path('gen_html.py', run_name='__main__')

print()
for f in ('ibmi_ptf.html', 'ibmi_ptf_severity.csv', 'summary_lpp_version.csv'):
    if os.path.exists(f):
        print('  %8.1f KB  %s' % (os.path.getsize(f) / 1024, os.path.join(HERE, f)))
