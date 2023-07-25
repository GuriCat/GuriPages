---
layout: post
title:  "IBM Documentation オフライン"
date:   2022-10-27 10:10:10 +0900
categories: その他
---
IBM Docsの情報をインターネット接続が無い状況でも参照できるようになりました。利用手順は次のような感じ ([Qiitaの投稿](https://qiita.com/keniooi/items/d0bce040ddb78d6fcbf7)の方が図入りでわかりやすいかも)。

1. [「IBM Documentation オフライン」](https://www.ibm.com/docs/ja/offline)からWindows用アプリケーションをダウンロード/インストール
1. IBM Docsの任意のページ([IBM i 7.5](https://www.ibm.com/docs/ja/i/7.5)とか[S1014](https://www.ibm.com/docs/ja/power10/9105-41B)とか)を開き、右上の「人物」アイコンをクリックして「サインイン」すると、左下に「Offline docs ↓」と青字で表示されるの、これをクリックしてダウンロード
1. IBM Documentation Offlineアプリを開き、右の「Add or update docs」をクリック、表示されたウインドゥで「Select product files」をクリックしてダウンロードしたZIPファイルを選択し、「Upload products」をクリック
1. アプリの左にアップロードした製品が表示されるので、IBM Docs Webサイト同様に操作

今回試した範囲での感想です。

* アプリが未成熟？(アプリケーションアイコンが設定されない、メニューが英語しかない？)
* 差分のみのオンライン更新が無く、更新は全文書を再ダウンロードして登録？
* 昔のBookMgrと比較すると「しおり」や「ノート」などが無く、機能が限定的
* デフォルトでCドライブに文書が保管され、ディスクスペースを圧迫(IBM i 7.5の日本語&英語で約2GB)
* 画面表示が速い(IBMのDocsサーバーが遅い？)

通信禁止のデータセンター作業の時にドキュメントを参照したい場合などに便利かもしれません。
