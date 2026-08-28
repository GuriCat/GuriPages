# IBM i セキュリティ速報 PTF 台帳

IBM の [IBM Product Security Central](https://www.ibm.com/support/pages/bulletin/) で公開されている
セキュリティ速報のうち「IBM i」に該当するものを収集し、**ライセンスプログラム（LPP）と IBM i リリースごとに
適用すべき PTF 番号を一覧できる HTML** を生成する Python ツールです。

IBM のサイトは CVE 単位・速報単位で情報が並んでいるため、「うちの 7.5 の 5770-SS1 に当てるべき PTF は何か」
という運用側の問いには答えにくいのですが、そこを埋めることを目的にしています。

---

## まず見る

**`preview.html`** をブラウザで開いてください。サーバーも通信も不要な単体の HTML です。

- 上段が **ライセンスプログラム × IBM i リリース**のマトリクス。数字はユニーク PTF 数、下の帯は Severity の構成
- **数字のあるセルをクリック**すると「リストする PTF の選択」ウインドウが開きます
  - Severity（すべて / Critical / High / Medium / Low）を選ぶと、該当する PTF 番号が**昇順・カンマ区切り**で表示されます
  - 「コピー」ボタンでクリップボードへ。そのまま WRKPTFGRP の確認リストや発注メモに貼れます
  - グループ PTF（SF99xxx）を含めるかどうかも切り替えできます
  - タイトルバーをドラッグすればウインドウを移動でき、開いたまま別のセルをクリックできます
- 右端の「計」列はリリース横断の合計。クリックすると全リリース分をまとめて抽出します
- 下段は PTF の明細。リリース / LPP / PTF 種別 / Severity / 全文検索で絞り込め、各行から速報の原文（Remediation および Workarounds and Mitigations）を開けます

CSV も同梱しています。

| ファイル | 内容 |
|---|---|
| `ibmi_ptf_severity.csv` | PTF 明細（CVE、Publish Date、速報 URL、回避策の原文まで含む全 21 列） |
| `summary_lpp_version.csv` | ライセンスプログラム × リリースの集計 |

---

## 最新化する

```
python refresh.py            速報一覧を取得 → 新規・更新分の速報ページだけ再取得 → 再生成
python refresh.py --full     キャッシュを無視して全速報ページを取り直す
python refresh.py --offline  ダウンロードせず手元のキャッシュだけで再生成
```

必要なもの: Python 3.9 以降と、`pip install beautifulsoup4 lxml`

初回は速報ページを 347 件ほどダウンロードするため数分かかります。2 回目以降は各速報の
`modified_date` を `cache.json` と突き合わせ、更新されたものだけ取り直すので数秒で終わります。

ダウンロードした速報ページは `pages/`（約 21MB）に置かれます。IBM のコンテンツなので再配布はせず、
手元でのキャッシュとして扱ってください。

---

## 構成

| ファイル | 役割 |
|---|---|
| `refresh.py` | 速報一覧の取得、差分ダウンロード、以下 3 本の実行 |
| `extract.py` | 速報 HTML から PTF 番号・IBM i リリース・製品を抽出 |
| `build.py` | ライセンスプログラムの判定、リリースの補完、CSV 出力 |
| `gen_html.py` | `preview.html` の生成 |

データ源は、IBM の速報検索画面（Vue 製）が内部で使っている JSON API です。

```
https://www.ibm.com/support/pages/securityapp/api/search?q=IBM i
```

この API から速報の一覧（nid・タイトル・CVE・CVSS Severity・公開日・影響製品）が取れます。
ただし **PTF 番号は含まれていない**ため、各速報のページ（`/support/pages/node/<nid>`）を
取得して Remediation/Fixes と Workarounds and Mitigations を解析しています。

---

## 解析について

速報の書式は 2018 年から 2026 年までの間にかなり揺れており、以下のパターンを解析しています。

**表形式**

- `IBM i Release | 5770-SS1 PTF Number(s) | PTF Download Link(s)` という現行の標準形
- `rowspan` / `colspan` を展開したうえで列の役割を判定（リリース列・PTF 列・製品バージョン列・ダウンロードリンク列）
- 列見出しがリリースそのもので、行が CVE になっている転置レイアウト（`IBM i 7.4 | IBM i 7.3 | IBM i 7.2` × `CVE-2019-9517 | SI70961 | SI70970 | Not affected`）
- Db2 Web Query のように、製品バージョンと IBM i リリースが別々の列で交差する表
- ダウンロードリンク列は URL に PTF 番号が入っているため、番号の二重取りを避けて除外

**文章形式（主に古い速報）**

- `Release 6.1 – SI56418` のように 1 行で完結するもの
- `Release 6.1 –` の次の行に `SI56418` が来るもの
- `IBM i OS and options:` / `IBM i Java:` / `IBM HTTP server for i:` といった製品見出しで対象 LPP が切り替わるもの
- `R720` / `R540` のような旧表記（それぞれ 7.2 / 5.4 と解釈）
- PTF 番号が URL のパス内にしか書かれていないもの
- Remediation/Fixes ではなく Summary や Vulnerability Details に PTF が書かれているもの

**ライセンスプログラムの判定**

表の見出しにある製品番号（`5770-SS1` など）を最優先し、記載が無い場合は本文の製品見出し、
速報タイトル、PTF 接頭辞の順に推定します。推定が入った場合は、その根拠を CSV の `LPP判定根拠` 列と
HTML の製品名の脇に明記しています。

**IBM i リリースの補完**

速報にリリースが明記されていない PTF は、次の順で補完し、HTML のリリース欄に「補完」と表示します
（ホバーで根拠が出ます）。

1. 同じ表の他行が示すリリース範囲
2. Affected Products and Versions の記載
3. ページ末尾の製品タクソノミー（`<div id="taxonomy-source">` にある IBM 自身の分類）

タクソノミーは古い分類が残っている速報があるため、他に手掛かりが無い場合の最終手段としてのみ使います。

---

## 注意

- **Severity は CVSS ベーススコアの区分**で、速報に含まれる CVE のうち最も高い値を採用しています。
  同じ PTF が複数の速報に現れる場合も最も高い値で分類するため、上位に分類された PTF は下位の一覧には現れません。
- **同梱の HTML / CSV は生成時点のスナップショット**です。適用前に必ず各速報の原文を確認してください。
  明細の各行から速報ページへリンクしています。
- **PTF 番号を抽出できない速報が 4 件あります。** いずれも速報側に PTF 番号の記載自体が無いもので、
  ICU（入力のサニタイズのみを推奨）、IBM i Access for Windows のサービスパック、
  Power Systems Firmware のバージョン指定、「IBM i は影響を受けない」という内容のものです。
- 抽出結果は自動解析によるものです。**適用の可否は必ず速報原文と Fix Central で確認してください。**
