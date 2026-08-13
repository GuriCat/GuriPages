---
layout: post
title: "IBM Bob Premium Package for i の価値"
date: 2026-08-13 00:00:00 +0900
tags: [モダナイゼーション, RPG, DX, Bob]
---
Bobcoin 枯渇のためまだ使えていないのですが、IBM Bob Premium Package for i がどのようなものか調べてみました。

なお本記事は、拡張機能を導入して**中身の構成を確認した**ものと、IBM Bob のドキュメントサイト(英語)の記載に基づいています。機能の説明は同サイトの文面によります(**2026年8月13日時点の記載を確認**)。実際に動かして使い込んだわけではない点はご承知おきください。

<br>
<hr>

## PP4i の実態は Bob 専用の API 群である

<br>

IBM Bob のサイトによると、IBM Bob Premium Package for i (以下 [PP4i](https://bob.ibm.com/docs/ide/premium-packages/bob-for-i/bob-for-i-index){:target="_blank"} と略)は「IBM Bob の AI 機能を IBM i アプリケーション開発環境に拡張」するようです。IBM i システムへのアクセスを提供し、開発者が「アプリケーションのライフサイクル全体にわたってより効果的に作業できるようにする」ものと説明されています。

まず押さえておきたいのは、**PP4i の実態は Bob 専用の API 群である**ということです。

PP4i は Bob 本体に同梱されているものではなく、後から導入するアドオンです。導入されると、モード・ワークスペース・ツール・スキル・ワークフローといった要素を Bob 本体に対して登録します。この「登録する」ための受け口は Bob が独自に用意しているもので、汎用の VS Code にも他の AI 開発ツールにも相当する仕組みはありません。つまり PP4i は、Bob という土台の上でのみ意味を持つ拡張として設計されています。

裏を返せば、**Bob を使う前提であれば、追加設定なしにこれらが一式そろう**ということでもあります。

利用の前提として、前提条件の項に挙げられた要件をすべて満たしたうえで、**Code for IBM i 経由で IBM i システムに接続済み**であることが必要です(IBM i 側で SSH が稼働していることが条件)。

<br>
<hr>

## 何が追加されるか

<br>

追加される要素は下記のとおりです。

|要素|数|内容|
|---|---|---|
|モード|2|`IBM i Developer`(コードの説明・生成・コンパイル・テスト・文書化)、`IBM i Database`(Db2 for i の SQL の生成・モダナイズ・チューニング・レビュー)|
|ワークスペース|3|Local(ローカルのファイル)、Library List(ライブラリーリスト内のライブラリー・オブジェクト・メンバー)、Home Directory(ホームディレクトリー内のストリームファイル)|
|ツール|20|Read 6、Write 2、Execute 4、Build 2、Test 2、Documentation 4|
|スキル|44|RPG 20、CL 4、DDS 4、Db2 for i & SQL 15、単体テスト 1|
|スラッシュコマンド|2|`/erd`(Mermaid 形式の ER 図生成)、`/review_SQL`(SQL のレビュー。Database モードのみ)|
|ワークフロー|5|RPG モダナイゼーション、業務ルール抽出、RPGUnit テスト計画作成、同実装、SQL インデックス戦略|
|設定|3|SQL 取得行数の上限、CL のライブラリー修飾の強制、承認を要する SQL 種別|

<br>

モードは「IBM i 開発のために専用に作られた、特化型の AI ペルソナ」、スキルは「専門知識の組み込みライブラリー。コンテキストに基づいて Bob が自動的に有効化し、一貫した正確な結果を生み出す」と説明されています。どちらのモードも、**タスクの開始時に接続情報(接続名、ホスト、ユーザープロファイル、OS バージョン、CCSID、現行ライブラリー、ライブラリーリスト)を自動的に注入します**。スキルは会話の内容に応じて自動的に読み込まれるため、利用者が名前を覚えて呼び出す必要はありません。

### ツール (20種類)

|カテゴリー|ツール|
|---|---|
|Read|`read_member`、`search_qsys`、`read_stream_file`、`search_ifs`、`get_table_columns`、`get_cl_command_library`|
|Write|`write_member`、`write_stream_file`|
|Execute|`execute_cl_command`、`execute_sql_statement`、`execute_pase_command`、`convert_rpg_source`|
|Build|`get_compile_actions`、`execute_compile_action`|
|Test|`generate_rpg_unit_test_stub`、`run_rpg_unit_test_suite`|
|Documentation|`search_ibm_i_docs_with_rag`、`fetch_cl_command_doc`、`search_sql_examples`、`fetch_sql_example`|

<br>

「QSYS または IFS 内のソースコードの読み取り・書き込み・検索と、CL コマンド、SQL 文、PASE コマンドの実行」が一式そろっています。これを Library List / Home Directory のワークスペースと組み合わせることで、**ソースを PC に落とさずに、IBM i 上のメンバーを対象として作業できます**。

### ワークフロー (5種類)

|ワークフロー|説明|
|---|---|
|RPG Modernization|OPM および固定形式 ILE RPG のソースを、モダンな free-format RPG に変換する(2フェーズの処理)|
|Business Rules Extraction|RPGLE のソースコードを分析し、業務ルールを Mermaid 図を含む Markdown レポート(8セクション)として抽出する|
|RPGUnit Test Plan Creation|IBM i のコードを分析し、構造化された RPGUnit テスト計画書を生成する|
|RPGUnit Test Suite Implementation|既存のテスト計画書からテストスイートを実装し、実行してエラーを反復的に解決する|
|SQL Index Strategy Advisor|Db2 for i の SQL パフォーマンスデータを分析し、最適化されたインデックス戦略を策定して承認向けに提示する|

<br>

起動方法は、チャット上部の「Start Workflow」ボタンから選ぶか、依頼内容に合うワークフローがあると Bob が判断した場合に提案してくるものを受けるかの2つです。IBM i のワークフローの多くは、有効な接続が無いと表示されません。

### ガードレール

|設定|既定値|説明|
|---|---|---|
|`general.maxRowsToFetch`|100|`execute_sql_statement` ツールが取得する最大行数|
|`guardrails.enforceQualifiedCLCommands`|true|CL コマンドにライブラリー修飾(例：`QSYS/...`)を必須とする。未修飾の場合はエラーを返し、修飾した代替案を提示する|
|`guardrails.deniedSQLStatementTypes`|17種類|自動承認の権限が与えられている場合でも、実行前に明示的なユーザー承認を必要とする SQL 種別|

<br>

`deniedSQLStatementTypes` の既定値は `DROP`、`GRANT`、`REVOKE`、`TRUNCATE`、`UPDATE` など17種類で、チームのリスク許容度に応じて調整できます。ライブラリー修飾の強制は、ライブラリーリストに依存した解決のリスクを減らすためのセキュリティのベストプラクティスとして、有効のままにすることが推奨されています。

<br>
<hr>

## 個別に用意できるもの、PP4i にしかないもの

<br>

「同じことを他の環境でやろうとしたらどうなるか」という観点で整理すると、下記のように分かれます。

|PP4i の要素|個別に用意する場合の代替|
|---|---|
|`read_member` / `write_member` / `search_qsys`|SSH ＋ `Rfile` / `system` コマンド、または QSYS2 サービス経由の SQL|
|`read_stream_file` / `search_ifs`|SSH(PASE)で通常のファイル操作|
|`execute_cl_command`|`system "CMD"`(PASE 経由)|
|`execute_sql_statement`|Mapepire / JDBC / `db2util`|
|`execute_compile_action`|`actions.json` 相当を定義し `system CRTBNDRPG` 等|
|`run_rpg_unit_test_suite`|RPGUnit の `RUCALLTST` を直接実行|
|`search_ibm_i_docs_with_rag`|**代替なし**(IBM 公式ドキュメントに対する専用のセマンティック検索)|
|**44スキル＋5ワークフロー**|**代替なし。自前で書く必要がある**|

<br>
<hr>

## 現時点での評価

<br>

PP4i の価値は大きく 2 つあると考えています。

**1. 個別にワークをかけて設定が必要なツールが、標準化されたパッケージとして提供されている**

上の表のとおり、ツール類は「やろうと思えばできる」ものです。しかし「できる」と「配ってある」の間には大きな差があります。接続方法を決め、コンパイル定義を書き、権限とガードレールを設計し、動作確認をする——この一連の作業が済んだ状態で手元に来る、というのが PP4i の提供形態です。ライブラリー修飾の強制や、承認を要する SQL 種別の既定リストのように、既定値そのものが検討済みの成果物になっています。

**2. IBM i ドメイン知識(44スキル)と5ワークフローが定型化されている**

RPG/CL の規約を自社で制定し、それに沿ったスキルを整備していく作業は、それ自体が相応の投資になります。PP4i はその部分が最初から型として用意されているため、**スキル整備と AI のトレーニングのワークが節減できます**。RPG モダナイゼーションや業務ルール抽出といったワークフローも、手順そのものが製品として定義されている点に意味があります。

<br>
<hr>

## 「どこでも同じツールで仕事ができる」ことの難しさ

<br>

代替機能を自前で用意すること自体は可能です。しかし、それを**自社の生成AI 開発者に標準的に配布し、導入させ、設定させる**となると、話が変わります。

- どの接続方式を標準とするか決める
- 導入手順書を書き、各開発者の環境で動くまで面倒を見る
- 規約に沿ったスキルを書き、レビューし、更新し続ける
- 環境差による「自分の手元では動かない」に対応し続ける

これらは一度やれば終わりではなく、人が増えるたび、バージョンが上がるたびに発生します。結果として「隣の席の人と同じ結果が出ない」「あの人の環境でしか動かない」という状態になりがちです。

かつての PDM や SEU は、どのマシンにログインしても同じキー操作で同じ画面が出て、同じ仕事ができました。当たり前のように思っていましたが、**「どこでも同じツールで仕事ができる」環境は、実は実現が難しいのです**。標準化されたパッケージとして配布されることには、機能一覧に現れない価値があります。

<br>
<hr>

Bobcoin の手当てができたらいろいろと試してみようと心待ちにしています。

<br>

{::comment}
タグ
tags: [V7R5, V7R4, ACS, TR]

EOS
V7R3
V7R4
V7R5
V7R6
ACS
Db2
DX
HMC
LTO
Merlin
Navigator
NetServer
NVMe
OSS
PTF
POWER9
POWER10
POWER11
RDi
RDX
RPG
SQL
SWMA
TCP/IP
TR
技術情報
ペーパー
モダナイゼーション
パフォーマンス
運用
セキュリティ
その他
{:/comment}
