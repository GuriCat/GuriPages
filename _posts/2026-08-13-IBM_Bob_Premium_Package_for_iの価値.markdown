---
layout: post
title: "IBM Bob Premium Package for i の価値"
date: 2026-08-13 00:00:00 +0900
tags: [モダナイゼーション, RPG, DX, Bob]
---
Bobcoin 枯渇のためまだ使えていないのですが、IBM Bob Premium Package for i がどのようなものか調べてみました。

なお本記事は、拡張機能を導入して**中身の構成を確認した**ものと、[IBM Bob のドキュメントサイト](https://bob.ibm.com/docs/ide/premium-packages/bob-for-i/bob-for-i-index){:target="_blank"}(英語)の記載に基づいています。機能の説明は同サイトの文面によります(**2026年8月13日時点の記載を確認**)。実際に動かして使い込んだわけではない点はご承知おきください。

<hr>
<br>

## PP4i の実態は Bob 専用の API 群である

IBM Bob のサイト ([https://bob.ibm.com/docs/ide/premium-packages/bob-for-i/bob-for-i-index](https://bob.ibm.com/docs/ide/premium-packages/bob-for-i/bob-for-i-index){:target="_blank"}) によると、IBM Bob Premium Package for i (以下 PP4i と略)は「IBM Bob の AI 機能を IBM i アプリケーション開発環境に拡張」するようです。IBM i システムへのアクセスを提供し、開発者が「アプリケーションのライフサイクル全体にわたってより効果的に作業できるようにする」ものと説明されています。

まず押さえておきたいのは、**PP4i の実態は Bob 専用の API 群である**ということです。

PP4i は Bob 本体に同梱されているものではなく、後から導入するアドオンです。導入されると、モード・ワークスペース・ツール・スキル・ワークフローといった要素を Bob 本体に対して登録します。この「登録する」ための受け口は Bob が独自に用意しているもので、汎用の VS Code にも他の AI 開発ツールにも相当する仕組みはありません。つまり PP4i は、Bob という土台の上でのみ意味を持つ拡張として設計されています。

裏を返せば、**Bob を使う前提であれば、追加設定なしにこれらが一式そろう**ということでもあります。

利用の前提として、前提条件の項に挙げられた要件をすべて満たしたうえで、**Code for IBM i 経由で IBM i システムに接続済み**であることが必要です(IBM i 側で SSH が稼働していることが条件)。

<hr>
<br>

## 何が追加されるか

ドキュメントサイトの構成に沿って見ていきます。

### モード (2種類)

モードは「IBM i 開発のために専用に作られた、特化型の AI ペルソナ。IBM i 固有のコンテキスト、用語、ベストプラクティスを取り込んだもの」と説明されています。

|モード|説明|
|---|---|
|`IBM i Developer`|IBM i 上のコードを説明、生成、コンパイル、テスト、文書化する|
|`IBM i Database`|Db2 for i における SQL を生成、モダナイズ、チューニング、レビューする|

<br>

`IBM i Developer` の主な用途は、業務ロジックの説明、コード文書の生成、RPG(OPM または ILE)・CL・DDS・SQL・COBOL のソースの記述とリファクタリング、CL コマンドによるオブジェクトのコンパイル、単体テストの生成と実行、固定形式から free-format RPG へのモダナイゼーションです。`IBM i Database` は SQL 文の記述とレビュー、データベーススキーマの理解、照会パフォーマンスとインデックス戦略の分析を、IBM i のベストプラクティスに沿って支援します。

どちらのモードも、**タスクの開始時に IBM i の接続情報を自動的に注入します**。接続名、ホスト、ユーザープロファイル、OS バージョン、CCSID の設定、現行ライブラリー、ライブラリーリストの情報です。`IBM i Database` ではこれに加えて、Db2 for IBM i のアクティブな SQL ジョブの情報も渡されます。なお、どちらのモードも Bob の設定画面からカスタマイズできます。

### ワークスペース (3種類)

|ワークスペース|説明|
|---|---|
|Local|ローカルワークスペース内のファイルとディレクトリーを対象に作業する(既定)|
|Library List|ライブラリーリスト内のライブラリー、オブジェクト、メンバーを対象に作業する|
|Home Directory|ユーザープロファイルのホームディレクトリー内のストリームファイルやディレクトリーを対象に作業する|

<br>

Local は既定のオプションで、リポジトリーからローカルに clone した IBM i アプリケーションを扱う場合に使います。ローカル中心ではあるものの、必要に応じて Bob が IBM i にアクセスしてコマンドを実行したり、別のソースコードを参照したりすることは可能です。

Library List は、Code for IBM i のユーザーライブラリーリストをタスクワークスペースとしてマップするもので、QSYS 内のソースやコンパイル済みオブジェクトを含む特定のライブラリー群に的を絞って作業できます。Home Directory は IFS の `/home/<ユーザー名>` を対象とし、そこに置かれたスクリプトや文書を扱います。この2つのワークスペースからも、明示的に指示すれば QSYS / IFS の反対側にアクセスできます。

3種類とも、コンテキストメンションによってスコープを絞ったやりとりに対応しており、過去のタスクをワークスペースで絞り込んで参照することもできます(IBM i 固有のワークスペースは接続が有効であることが前提)。

### ツール (20種類)

ツールについては「QSYS または IFS 内のソースコードの読み取り・書き込み・検索と、CL コマンド、SQL 文、PASE コマンドの実行」と説明されています。6つのカテゴリーに分類されています。

|カテゴリー|ツール|説明|
|---|---|---|
|Read|`read_member`|QSYS 内の1つ以上のソースメンバーの内容を読み取る|
||`search_qsys`|ライブラリー、オブジェクト、メンバーを検索する。メンバー内の正規表現検索に対応|
||`read_stream_file`|IFS 内の1つ以上のストリームファイルの内容を読み取る|
||`search_ifs`|ストリームファイルとディレクトリーを検索する。内容の正規表現検索が可能|
||`get_table_columns`|Db2 for i のテーブルまたはビューの列メタデータを取得する|
||`get_cl_command_library`|CL コマンドの登録先ライブラリーを調べる|
|Write|`write_member`|QSYS に新規ソースメンバーを作成、または既存のソースメンバーを上書きする|
||`write_stream_file`|IFS に新規ストリームファイルを作成、または既存のストリームファイルを上書きする|
|Execute|`execute_cl_command`|IBM i 上で CL コマンドを実行する|
||`execute_sql_statement`|IBM i 上で SQL 文を実行する|
||`execute_pase_command`|IBM i 上で PASE コマンドを実行する|
||`convert_rpg_source`|RPG III/400 のコードを RPG IV 形式に変換する|
|Build|`get_compile_actions`|指定したファイルに対する Code for IBM i のアクションを取得する|
||`execute_compile_action`|特定のコンパイルアクションを実行する|
|Test|`generate_rpg_unit_test_stub`|RPGLE / SQLRPGLE ファイルから RPGUnit のテストスタブを生成する|
||`run_rpg_unit_test_suite`|テストをコンパイルして実行する。コードカバレッジの取得も可能|
|Documentation|`search_ibm_i_docs_with_rag`|RAG を使って IBM i のドキュメントを検索する|
||`fetch_cl_command_doc`|CL コマンドのドキュメントを取得する|
||`search_sql_examples`|関連する SQL の例を検索する|
||`fetch_sql_example`|SQL の例の全文を取得する|

<br>

ドキュメント検索については「セマンティック検索を使って IBM i の公式ドキュメントを検索・取得し、正確で最新の内容に基づいた回答を行う」と説明されています。

### スキル (44種類)

スキルは「専門知識の組み込みライブラリー。コンテキストに基づいて Bob が自動的に有効化し、一貫した正確な結果を生み出す」ものと説明されています。「特定のモードで利用可能になり、進行中の会話に関連する場合に Bob が自動的に読み込む」ため、**利用者がスキル名を覚えて呼び出す必要はありません**。

PP4i は「Bob の組み込みスキルを、RPG、CL、DDS、Db2 for i & SQL、単体テストをカバーする包括的なスキル群で拡張する」とされ、内訳は下記のとおりです。

|分野|数|内容|
|---|---|---|
|RPG|20|言語の各形態、モダナイゼーション、デバッグ|
|CL|4|基礎、API 連携|
|DDS|4|各ファイル定義タイプ|
|Db2 for i & SQL|15|照会、ストアードプロシージャー、パフォーマンス|
|単体テスト|1|RPGUnit|

<br>

主な領域として、レガシーからモダンへのコード変換(固定形式から free-format、OPM から ILE)、データベースの最適化とパフォーマンス分析、SQL カーソル操作とストアードプロシージャー、IBM i システム API の連携、コード品質の評価とリファクタリングが挙げられています。各スキルは `IBM i Developer` または `IBM i Database` のいずれかのモードに向けたものです。

### スラッシュコマンド (2種類)

|コマンド|説明|利用可能なモード|
|---|---|---|
|`/erd`|接続中の IBM i 上の一連のデータベーステーブルについて、Mermaid 形式の ER 図(Entity Relationship Diagram)を生成する|IBM i Developer、IBM i Database|
|`/review_SQL`|SQL 文を、正確性・可読性・セキュリティ・パフォーマンスを含むベストプラクティスに照らして包括的にレビューする|IBM i Database|

<br>

`/erd` はシステムテーブルを照会し、データ型とカーディナリティー表記を伴うテーブル構造・関連の図を組み立てます。`/review_SQL` は簡潔化、修飾、セキュリティ、パフォーマンスといった領域を網羅するチェックリストで評価し、構造化された指摘と修正後の SQL を提示します。いずれも IBM i への有効な接続が必要で、分析範囲を指定する任意の引数を受け付けます。

### ワークフロー (5種類)

ワークフローは「RPG モダナイゼーション、業務ルール抽出、単体テスト計画の作成、SQL インデックス戦略の助言のための、ガイド付きの複数ステップのワークフロー」と説明されています。

|ワークフロー|説明|
|---|---|
|RPG Modernization|OPM および固定形式 ILE RPG のソースを、モダンな free-format RPG に変換する。OPM から ILE への変換と ILE 固定形式の変換の両方を、2フェーズの処理で対応|
|Business Rules Extraction|RPGLE のソースコードを分析し、業務ルールを Mermaid 図を含む Markdown レポートとして抽出する。依存関係を特定し、8セクションのエグゼクティブ向け報告書にまとめる|
|RPGUnit Test Plan Creation|IBM i のコードを分析し、構造化された RPGUnit テスト計画書を生成する。テンプレート文書、モジュールの説明、テストスイート、ユーティリティーのカタログを作成|
|RPGUnit Test Suite Implementation|既存のテスト計画書から RPGUnit のテストスイートを実装する。計画書を読み取り、テストコードを記述し、スイートを実行し、エラーを反復的に解決する|
|SQL Index Strategy Advisor|Db2 for i の SQL パフォーマンスデータを分析し、最適化されたインデックス戦略を策定する。パフォーマンス指標をレビューし、インデックスの推奨をユーザーの承認向けに提示する|

<br>

起動方法は2つあります。ひとつはチャット上部の「Start Workflow」ボタンを選び、ワークスペースを選択して目的のワークフローの「Start」をクリックする方法。もうひとつは、依頼内容に合うワークフローがあると Bob が判断した場合に提案してくるので、「Start workflow」を選んで進める方法です。IBM i のワークフローの多くは、有効な接続が無いと表示されません。

### 設定とガードレール

|設定|既定値|説明|
|---|---|---|
|`vscode-ibmi-bob.general.maxRowsToFetch`|100|`execute_sql_statement` ツールが取得する最大行数を制御する。値を大きくすると一度に多くのデータを取得できるが、応答の待ち時間が増える可能性がある|
|`vscode-ibmi-bob.guardrails.enforceQualifiedCLCommands`|true|有効な場合、CL コマンドにライブラリー修飾(例：`QSYS/...`)を必須とする。未修飾のコマンドにはエラーを返し、修飾した代替案を提示する|
|`vscode-ibmi-bob.guardrails.deniedSQLStatementTypes`|17種類|自動承認の権限が与えられている場合でも、実行前に明示的なユーザー承認を必要とする SQL 操作を指定する|

<br>

`enforceQualifiedCLCommands` については、ライブラリーリストに依存した解決のリスクを減らすためのセキュリティのベストプラクティスとして、有効のままにすることが推奨されています。`deniedSQLStatementTypes` の既定値は `ALLOCATE`、`CALL`、`COMMIT`、`CONNECT`、`DISCONNECT`、`DROP`、`EXECUTE`、`GRANT`、`LOCK`、`MERGE`、`PREPARE`、`RENAME`、`REVOKE`、`ROLLBACK`、`SAVEPOINT`、`TRUNCATE`、`UPDATE` の17種類で、チームのリスク許容度と運用上の必要に応じて調整できます。

<hr>
<br>

## 個別に用意できるもの、PP4i にしかないもの

「同じことを他の環境でやろうとしたらどうなるか」という観点で整理すると、下記のように分かれます。

### ユーザーが個別に拡張できる機能

|PP4i の要素|個別に用意する場合の代替|
|---|---|
|`read_member` / `write_member` / `search_qsys`|SSH ＋ `Rfile` / `system` コマンド、または QSYS2 サービス経由の SQL|
|`read_stream_file` / `search_ifs`|SSH(PASE)で通常のファイル操作|
|`execute_cl_command`|`system "CMD"`(PASE 経由)|
|`execute_sql_statement`|Mapepire / JDBC / `db2util`|
|`execute_compile_action`|`actions.json` 相当を定義し `system CRTBNDRPG` 等|
|`run_rpg_unit_test_suite`|RPGUnit の `RUCALLTST` を直接実行|

### PP4i 独自の機能

|PP4i の要素|代替の可否|
|---|---|
|`search_ibm_i_docs_with_rag`|**代替なし**(IBM 公式ドキュメントに対する専用のセマンティック検索)|
|**44スキル＋5ワークフロー**|**代替なし。自前で書く必要がある**|

<br>

個別ツールの大半は、SSH と SQL 接続さえあれば技術的には再現できます。逆に言えば、**PP4i の価値の中心はツールそのものではなく、IBM i ドメイン知識(44スキル)とワークフローの型化にある**ということです。

<hr>
<br>

## 現時点での評価

PP4i の価値は大きく 2 つあると考えています。

**1. 個別にワークをかけて設定が必要なツールが、標準化されたパッケージとして提供されている**

上の表のとおり、ツール類は「やろうと思えばできる」ものです。しかし「できる」と「配ってある」の間には大きな差があります。接続方法を決め、コンパイル定義を書き、権限とガードレールを設計し、動作確認をする——この一連の作業が済んだ状態で手元に来る、というのが PP4i の提供形態です。ライブラリー修飾の強制や、承認を要する SQL 種別の既定リストのように、既定値そのものが検討済みの成果物になっています。

**2. IBM i ドメイン知識(44スキル)と5ワークフローが定型化されている**

RPG/CL の規約を自社で制定し、それに沿ったスキルを整備していく作業は、それ自体が相応の投資になります。PP4i はその部分が最初から型として用意されているため、**スキル整備のワークが節減できます**。RPG モダナイゼーションや業務ルール抽出といったワークフローも、手順そのものが製品として定義されている点に意味があります。

<hr>
<br>

## 「どこでも同じツールで仕事ができる」ことの難しさ

代替機能を自前で用意すること自体は可能です。しかし、それを**自社の生成AI 開発者に標準的に配布し、導入させ、設定させる**となると、話が変わります。

- どの接続方式を標準とするか決める
- 導入手順書を書き、各開発者の環境で動くまで面倒を見る
- 規約に沿ったスキルを書き、レビューし、更新し続ける
- 環境差による「自分の手元では動かない」に対応し続ける

これらは一度やれば終わりではなく、人が増えるたび、バージョンが上がるたびに発生します。結果として「隣の席の人と同じ結果が出ない」「あの人の環境でしか動かない」という状態になりがちです。

かつての PDM や SEU は、どのマシンにログインしても同じキー操作で同じ画面が出て、同じ仕事ができました。当たり前のように思っていましたが、**「どこでも同じツールで仕事ができる」環境は、実は実現が難しいのです**。標準化されたパッケージとして配布されることには、機能一覧に現れない価値があります。

<hr>
<br>

参考リンク(いずれも英語。2026年8月13日確認)：

- [IBM Bob Premium Package for i](https://bob.ibm.com/docs/ide/premium-packages/bob-for-i/bob-for-i-index){:target="_blank"}
- [Modes](https://bob.ibm.com/docs/ide/premium-packages/bob-for-i/modes){:target="_blank"}
- [Workspaces](https://bob.ibm.com/docs/ide/premium-packages/bob-for-i/workspaces){:target="_blank"}
- [Tools](https://bob.ibm.com/docs/ide/premium-packages/bob-for-i/tools){:target="_blank"}
- [Skills](https://bob.ibm.com/docs/ide/premium-packages/bob-for-i/skills){:target="_blank"}
- [Slash commands](https://bob.ibm.com/docs/ide/premium-packages/bob-for-i/slash-commands){:target="_blank"}
- [Workflows](https://bob.ibm.com/docs/ide/premium-packages/bob-for-i/workflows){:target="_blank"}
- [Settings](https://bob.ibm.com/docs/ide/premium-packages/bob-for-i/settings){:target="_blank"}

<br>

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
