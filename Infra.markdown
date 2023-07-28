---
layout: page
title: インフラ
permalink: /Infra/

---

---

<P></P>

### 現状調査

<P></P>

－－－－－－－－

<P></P>

#### インフラ収集情報
移行や構築時にIBM i から収集可能な主要情報の一覧。プロジェクトの要件やアクセス制限によって選別。

* [「インフラ収集情報.xlsx」](/GuriPages/files/インフラ収集情報.xlsx)：情報と取得方法/取得形式の例。IBM i 7.1以降の場合は[IBM i サービス(SQL)](https://www.ibm.com/docs/ja/ssw_ibm_i_73/rzajq/rzajqservicessys.htm)でPTF情報やTCP/IP設定の取得を推奨。

* 情報取得簡易プログラム
  * [RTVLANGINF.clle](https://github.com/GuriCat/GuriPages/blob/main/files/RTVLANGINF.clle)：パラメーター無しでCALLするとIBM i の言語基本情報をメッセージで出力
  
  ```
  > call rtvlanginf                                    
  DEFAULT LANG INFO: NLV-2962 EBCDIC-5026, ASCII-942.
  ```

  * [TCPA0200.rpgle](https://github.com/GuriCat/GuriPages/blob/main/files/TCPA0200.rpgle)：パラメーター無しでCALLするとIBM i のTCP/IP属性を印刷出力([出力例](/GuriPages/files/TCPA0200.spl.txt))

  * [TCPA0300.rpgle](https://github.com/GuriCat/GuriPages/blob/main/files/TCPA0300.rpgle)：パラメーター無しでCALLするとIBM i のTCP/IPドメイン設定を印刷出力([出力例](/GuriPages/files/TCPA0300.spl.txt))


<P></P>

－－－－－－－－

<P></P>

### [HMCスキャナー](https://www.ibm.com/support/pages/hmc-scanner-power-server-config-and-performance-stats)

クライアントからHMCに接続し、LPAR情報などを取得してExcel形式で保管。

HMC Scanner is a Java program that uses SSH to connect to an HMC or SDMC or FSM or IVM (IVM is experimental), downloads the system configuration and produces a single Excel spreadsheet that contains the configuration of servers and LPARs. 

<P></P>

－－－－－－－－

<P></P>

### [Query/400 Discovery Tool](https://www.ibm.com/support/pages/query400-discovery-tool-0)

Queryの棚卸などに利用。

The utility creates database tables that contain such information as which files/tables are being used by the queries, join tests, result fields, etc.  

<P></P>

　

<P></P>

---

<P></P>


### 計画

<P></P>


－－－－－－－－

<P></P>

#### バージョンアップ影響調査ワークシート
バージョンを上げた場合の変更点を「プログラム資料説明書  (Memo to Users)」から引用・集約し、網羅的なチェックと判断を可能にします。

#### IBM Pre-Upgrade Verification Tool for IBM i (PRUV)

ｸライアントで実行され、 IBM i データを検査して、 アップグレードの開始前に必要な要件がすべて完了していることを確実にします。このツールは、アップグレード前の主なステップを検証します。 

pruv7.5.0.20220505.jar (4.94MB) 2022-05-13 IBMサイトに登録を確認

pruv_7.4.0.20200305.exe (122MB)
#### 暗黙のアクセスパスの共用
##### 暗黙のアクセスパス共有による影響概要 (お客様説明用) 
「バージョンアップ影響調査ワークシート」の「暗黙共有アクセスパスの考慮点」シートを参照。

適切なキー指定がされていない場合、OSのバージョン更新でアプリケーションが想定しない動作となる場合があります。
##### IBM Knowledge Centerの記載。
「例 : 暗黙共用アクセス・パス」 https://www.ibm.com/support/knowledgecenter/ja/ssw_ibm_i_73/dbp/rbafoiapse.htm などを参照

##### アクセス・パスが暗黙共用されることによってプログラムの動作に影響を与えることがあります。 (System i-11-01)  http://www-01.ibm.com/support/docview.wss?uid=jpn1J1005994 (リンク切れ)

