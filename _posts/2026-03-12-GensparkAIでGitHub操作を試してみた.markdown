---
layout: post
title: "Genspark AIでGitHub操作を試してみた"
date: 2026-03-12 09:00:00 +0900
tags: [その他]
---
AI アシスタント「Genspark」を使って、GitHub リポジトリの clone・編集・push を自動化できるか試してみました。

## 概要

[Genspark](https://www.genspark.ai/){:target="_blank"} は、検索・コード実行・ファイル操作などを組み合わせた AI アシスタントです。サンドボックス環境内で Bash コマンドを実行できるため、git 操作も可能です。

## やったこと

1. **PAT（Personal Access Token）の準備**  
   GitHub の Developer Settings で Fine-grained Token を発行し、対象リポジトリのみ `Contents: Read and write` 権限を付与。

2. **サンドボックスでの clone**  
   ```bash
   git clone https://<username>:<PAT>@github.com/GuriCat/GuriPages.git
   ```

3. **新規ブログエントリーの作成**  
   既存の `.markdown` ファイルのフォーマットを参考に、Genspark が自動でファイルを生成。

4. **commit & push**  
   ```bash
   git add .
   git commit -m "Add new blog post via Genspark AI"
   git push origin main
   ```

## 感想

AI がリポジトリ構造を自動解析し、既存記事のフォーマットに合わせた新規エントリーを生成・push まで一気に行ってくれました。繰り返し作業の自動化に活用できそうです。

<br>

<!-- This content will not appear in the rendered Markdown
タグ
tags: [その他]

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
 -->
