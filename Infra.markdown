---
layout: page
title: インフラ
permalink: /Infra/

---

リリースアップの作業項目や実施の流れはYouTubeの動画[「IBM i リリースアップ概要」](https://youtu.be/aX9lMxxYY_w)も参照ください。

内容：
* [現状調査](#現状調査)
* [計画](#計画)
* 運用 ⇒ サニタイズが可能であれば後日掲載
* [パフォーマンス](#パフォーマンス)
* [その他参考情報](#その他参考情報)


<P></P>
　

---

<P></P>

### 現状調査

<P></P>

－－－－－－－－

<P></P>

#### ●インフラ収集情報
移行や構築時にIBM i から収集可能な主要情報の一覧。プロジェクトの要件やアクセス制限によって選別。IBM i 7.1以降の場合は[IBM i サービス(SQL)](https://www.ibm.com/docs/ja/ssw_ibm_i_73/rzajq/rzajqservicessys.htm)でPTF情報やTCP/IP設定の取得を推奨。

* [インフラ収集情報 Excelワークイート](/GuriPages/files/インフラ収集情報.xlsx)：情報と取得方法/取得形式の例。

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

#### ●HMCスキャナー

 [IBM提供](https://www.ibm.com/support/pages/hmc-scanner-power-server-config-and-performance-stats)のツール。クライアントからHMCに接続し、LPAR情報などを取得してExcel形式で保管。

HMC Scanner is a Java program that uses SSH to connect to an HMC or SDMC or FSM or IVM (IVM is experimental), downloads the system configuration and produces a single Excel spreadsheet that contains the configuration of servers and LPARs. 

<P></P>

－－－－－－－－

<P></P>

#### ●Query/400 Discovery Tool

 [IBM提供](https://www.ibm.com/support/pages/query400-discovery-tool-0)のツール。Queryの棚卸などに利用。

The utility creates database tables that contain such information as which files/tables are being used by the queries, join tests, result fields, etc.  

<P></P>

　

<P></P>

---

<P></P>


### 計画

<P></P>


－－－－－－－－

<P></P>

#### ●バージョンアップ影響調査ワークシート

バージョンを上げた場合の変更点を「プログラム資料説明書  (Memo to Users)」から引用・集約し、網羅的なチェックと判断を可能にします。

プログラム資料説明書はリリースが発表される時点で各国語版が発行されるが、更新は英語版にのみ行なわれます。ファイル[「2023-06-06 バージョンアップ変更点と影響調査.xlsx」](GuriPages/files/2023-06-06 バージョンアップ変更点と影響調査.xlsx)は2023年5月までの変更を反映しています。



<P></P>


－－－－－－－－

<P></P>

#### ●IBM Pre-Upgrade Verification Tool for IBM i (PRUV)

IBMが提供するツールで、解説とダウンロードは[こちら](https://www.ibm.com/support/pages/ibm-pre-upgrade-verification-tool-ibm-i)。

クライアントで実行され、 IBM i データを検査して、 アップグレードの開始前に必要な要件がすべて完了していることを確実にします。このツールは、アップグレード前の主なステップを検証します。 


<P></P>


－－－－－－－－

<P></P>

#### ●暗黙のアクセスパスの共用

適切なキー指定がされていない場合、OSのバージョン更新でアプリケーションが想定しない動作となる場合があります。

FIFOなどのキーワードが明示指定されていない場合、実行時に暗黙共用されるアクセス・パスによって、同一キーを持つレコードの読取順は不定です。この仕様を考慮せずに「同一キーが到着順に読み取られる」と誤った想定で設計されたプログラムは無限ループなどの異常を引き起こすケースがありました。

共用されるアクセスパスを「LFの作成順序を変える」「PGMの実行順序を変える」などで固定しようとする試みは多くの場合に上手くいかず、かつ、継続性がありません。下記の情報を参照の上、PGM/LFの仕様を見直して再作成する事を推奨します。

* IBM Docsの[「例 : 暗黙共用アクセス・パス」](https://www.ibm.com/docs/ja/i/7.3?topic=files-example-implicitly-shared-access-paths)

* 日本IBMの[「テクニカル・フラッシュ 一覧 ＜IBM i＞」](https://www.ibm.com/support/pages/%E3%83%86%E3%82%AF%E3%83%8B%E3%82%AB%E3%83%AB%E3%83%BB%E3%83%95%E3%83%A9%E3%83%83%E3%82%B7%E3%83%A5-%E4%B8%80%E8%A6%A7-0)にタイトル「2011年1月7日 アクセス・パスが暗黙共用されることによってプログラムの動作に影響を与えることがあります。 (System i-11-01)」がありますが、[リンク切れ](http://www.ibm.com/support/docview.wss?uid=jpn1J1005994)になっています。基本的な内容はIBM Docsと同様ですが、必要な方はIBMに連絡すると文書が見つかるかもしれません。

<P></P>

－－－－－－－－

<P></P>

#### ●インフラ計画のための情報

<P></P>

* 主な情報源

  * [「IBM i Technology Updates」](https://www.ibm.com/support/pages/node/1119129)：各リリースのそれぞれのTRへのポインター
  * [「IBM i Release support」](https://www.ibm.com/support/pages/ibm-i-release-support)
  * [「System to IBM i maps」](https://www.ibm.com/support/pages/system-ibm-i-mapping)
  * [「Upgrade planning」](https://www.ibm.com/support/pages/upgrade-planning)
  * [「テクニカル・フラッシュ 一覧 ＜IBM i＞」](https://www-01.ibm.com/support/docview.wss?uid=jpn1J1009152)
  * [「Release life cycle」](https://www.ibm.com/support/pages/release-life-cycle)：製品/バージョンごとのGA/EOS日付け

<P></P>

* クライアントサポート
  * ACSのトップページ： [「IBM i Access - Client Solutions」](https://www.ibm.com/support/pages/node/633843)
  * [「IBM i Access - Windows」](https://www.ibm.com/support/pages/ibm-i-access-windows)：
    * Effective **April 30, 2019**, IBM® has withdrawn support for 5770-XE1 IBM i Access for Windows™  7.1.  IBM i Access for Windows 7.1. was delivered with IBM i 7.3, 7.2, and 7.1.  Extended support will not be available.
  * [「IBM i Access - for Windows Supported Operating Systems」](https://www.ibm.com/support/pages/ibm-i-access-windows-supported-operating-systems)：Access for WindowsがサポートしていたWindowsのバージョン。
  * [「5724-I20 IBM Host Access Client Package 15.0 - Product life cycle dates」](https://www.ibm.com/docs/en/announcements/host-access-client-package-150?region=JPN)：PCOMMを含むHACPのサポート開始・終了日、動作環境など。


<P></P>

－－－－－－－－

<P></P>

#### ●IBM i Technology Updates

* [IBM i Technology Refresh - FAQs](https://www.ibm.com/support/pages/ibm-i-technology-refresh-faqs)
* [PSP - IBM i Group PTFs with Level](https://www.ibm.com/support/pages/ibm-i-group-ptfs-level)
  * 各IBM i リリースでタイトルが「Technology Refresh」のPTF(例：R750ならSF99957、R730ならSF99727)を見つけます。このPTFのレベルをWRKPTFGRPコマンドで表示すれば、そのPTFのレベル=TRレベルとなります。

|Rel|Base GA|TR1|TR2|TR3|TR4|TR5|TR6|TR7|TR8|TR9|TR10|TR11|TR12|TR13| 
|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|
|[7.5](https://www.ibm.com/support/pages/node/6597663)|[22/05/10](https://www.ibm.com/support/pages/ibm-i-75-base-enhancements)|[22/12/02](https://www.ibm.com/support/pages/ibm-i-75-tr1-enhancements)|[23/05/05](https://www.ibm.com/support/pages/ibm-i-75-tr2-enhancements)|  |   |   |   |   |
|[7.4](https://www.ibm.com/support/pages/node/959455)|[19/06/21](https://www.ibm.com/support/pages/node/1164634)|[19/11/15](https://www.ibm.com/support/pages/node/1164034)|[20/07/17](https://www.ibm.com/support/pages/node/1381917)|[20/11/13](https://www.ibm.com/support/pages/node/6250855)|[21/04/16](https://www.ibm.com/support/pages/node/6405632)|[21/09/10](https://www.ibm.com/support/pages/node/6456987)|[22/05/24](https://www.ibm.com/support/pages/ibm-i-74-tr6-enhancements)|[22/12/02](https://www.ibm.com/support/pages/ibm-i-74-tr7-enhancements)|[23/05/05](https://www.ibm.com/support/pages/ibm-i-74-tr8-enhancements)|
|[7.3](https://www.ibm.com/support/pages/node/687365)|[16/04/15](https://www.ibm.com/support/pages/node/1169032)|[16/11/11](https://www.ibm.com/support/pages/node/1168750)|[17/03/17](https://www.ibm.com/support/pages/node/1168480)|[17/10/27](https://www.ibm.com/support/pages/node/1164682)|[18/03/16](https://www.ibm.com/support/pages/node/1168426)|[18/09/14](https://www.ibm.com/support/pages/node/1164652)|[19/05/10](https://www.ibm.com/support/pages/node/1164646)|[19/11/15](https://www.ibm.com/support/pages/node/1164640)|[20/07/17](https://www.ibm.com/support/pages/node/6155511)|[20/11/13](https://www.ibm.com/support/pages/node/6250925)|[21/04/16](https://www.ibm.com/support/pages/node/6405636)|[21/09/10](https://www.ibm.com/support/pages/node/6456989)|[22/05/24](https://www.ibm.com/support/pages/node/687365)|[22/12/02](https://www.ibm.com/support/pages/node/687365)|
|[7.2](https://www.ibm.com/support/pages/node/687327)|[14/05/02](https://www.ibm.com/support/pages/ibm-i-72-base-enhancements)|[14/11/11](https://www.ibm.com/support/pages/ibm-i-72-tr1-enhancements)|[15/05/29](https://www.ibm.com/support/pages/ibm-i-72-tr2-enhancements)|[15/11/20](https://www.ibm.com/support/pages/ibm-i-72-tr3-enhancements)|[16/05/20](https://www.ibm.com/support/pages/ibm-i-72-tr4-enhancements)|[16/11/11](https://www.ibm.com/support/pages/node/1274236)|[17/03/17](https://www.ibm.com/support/pages/ibm-i-72-tr6-enhancements)|[17/10/27](https://www.ibm.com/support/pages/ibm-i-72-tr7-enhancements)|[18/03/16](https://www.ibm.com/support/pages/node/1282828)|[18/09/14](https://www.ibm.com/support/pages/ibm-i-72-tr9-enhancements)|
|[7.1](https://www.ibm.com/support/pages/node/687325)|[10/04/23](https://www.ibm.com/common/ssi/ShowDoc.wss?docURL=/common/ssi/rep_ca/3/760/PWR10033/index.html&lang=ja)|[10/09/10](https://www.redbooks.ibm.com/abstracts/sg247858.html)|[11/05/13](https://www.redbooks.ibm.com/abstracts/sg247858.html)|[11/10/14](https://www.redbooks.ibm.com/abstracts/sg247858.html)|[12/05/18](https://www.redbooks.ibm.com/abstracts/sg247858.html)|[12/10/12](https://www.redbooks.ibm.com/abstracts/sg247858.html)|[13/02/13](https://www.redbooks.ibm.com/abstracts/sg247858.html)|[13/11/15](https://www.redbooks.ibm.com/abstracts/sg247858.html)|[14/06/06](https://www.ibm.com/docs/en/announcements/archive/JAJPJP14-0122)|[14/11/11](https://www.ibm.com/docs/en/announcements/archive/ENUSZP14-0508)|[15/05/29](https://www.ibm.com/docs/en/announcements/archive/ENUS215-137)|[15/11/20](https://www.ibm.com/docs/en/announcements/archive/ENUSAP15-0343)|

* [IBM i - Technical Articles](https://www.ibm.com/support/pages/node/1136062)
* [IBM i Tutorials, Demos, and SQL examples](https://www.ibm.com/support/pages/ibm-i-tutorials-demos-and-sql-examples-0)
* IBM i Technology Updates - by IBM i product or subject matter
  * [Access Client Solutions](https://www.ibm.com/support/pages/node/633843)
  * [Application Modernization](https://www.ibm.com/support/pages/node/1136122)
  * [Backup Recovery and Media Services (BRMS)](https://www.ibm.com/support/pages/node/1105629)
  * [Db2 for i (Database)](https://www.ibm.com/support/pages/node/1116645/)
  * [IBM Cloud Storage Solutions for i](https://www.ibm.com/support/pages/node/1135282)
  * [General IBM i Operating System](https://www.ibm.com/support/pages/node/1119357)
  * [Hardware and Firmware](https://www.ibm.com/support/pages/node/1128525)
  * [Integrated Web Services for IBM i](https://www.ibm.com/support/pages/node/1138612)
  * [Java on IBM i](https://www.ibm.com/support/pages/java-ibm-i)
  * [IBM Navigator for i](https://www.ibm.com/support/pages/node/6483299) [(Heritage Version)](https://www.ibm.com/support/pages/node/1142704)
  * [Open Source Technologies](https://www.ibm.com/support/pages/node/1128513)
  * [Performance Tools](https://www.ibm.com/support/pages/node/1120329)
  * [PowerHA SystemMirror for i](https://www.ibm.com/support/pages/node/1138294/)
  * [IBM i Security](https://www.ibm.com/support/pages/node/6150021)
  * [Systems Management](https://www.ibm.com/support/pages/node/1274284)
  * [IBM i Services (SQL)](https://www.ibm.com/support/pages/node/1119123)
  * [Web Integration on i](https://www.ibm.com/support/pages/node/1167808)

<P></P>

　

---


<P></P>

### パフォーマンス

<P></P>

－－－－－－－－

<P></P>

#### ●主な情報源

* [パフォーマンス関連リンク集](https://www.ibm.com/support/pages/node/1120383/)
* [DB2 for i Performance Enhancements](https://www.ibm.com/support/pages/node/1116615)
* [「IBM Power Systems Performance Capabilities Reference - IBM i  7.5 July 2022」](https://drive.google.com/file/d/1vhCOhKHTR_4RH3UOrxi4j8euWYdYb8VP/view)：Power8～10モデルのCPW
* パフォーマンスFAQ(不定期更新)：[「IBM i on Power - Performance FAQ May 1, 2023」](https://www.ibm.com/downloads/cas/QWXA9XKN)
* IBM Redbooks [「End to End Performance Management on IBM i」](https://www.redbooks.ibm.com/abstracts/sg247808.html)


<P></P>

－－－－－－－－

<P></P>

#### ●Db2/SQL

* [「Improving SQL procedure performance」](https://www.ibm.com/support/pages/sites/default/files/inline-files/SQL%20Procedure%20PerformanceV2.pdf)



<P></P>

－－－－－－－－

<P></P>

#### ●ディスク・パフォーマンス

* **有用な情報やツールなし。**
  * IBM i に外部ストレージを構成した場合、ディスクサブシステムのパフォーマンス分析/シミュレーションには[Disk Magic](https://www.intellimagic.com/products/disk-magic-rmf-magic-batch-magic/)を利用したケースがあるが、2020/1以降はアップデートなし(古い内蔵HDD(8.59～282.2GB)しか選択できず、大容量の内蔵ディスクや、NVMe、SSDは選択肢になく、マニュアル設定も不可)。新しいWebブラウザベースの「IBM Storage Modeller」(IBM/IBMパートナーのみアクセス可)であるが、内蔵ディスクは選択肢に見つからず。
  * 2021-03-05にRFE(現IBM Ideas)に[「Provide easy to use "IBM i internal disk performance modeling tool" which supports latest technologies (SSD, NVMe)」](https://ideas.ibm.com/ideas/IBMI-I-2952)が提案されるが「改善予定なし」で終了。



<P></P>

－－－－－－－－

<P></P>

#### ●Navigator for i 

* [IBM i Performance Data Investigator](https://developer.ibm.com/tutorials/ibm-i-performance-data-investigator/)
* [2013年「Collection Services & PDI - Whats new in 7-2.pdf」](https://www.esselware.com.mx/IBMi_en_Espanol/IBMi_PDI/Collection%20Services%20&%20PDI%20-%20Whats%20new%20in%207-2.pdf)
* [「IBM i Performance Data Investigator: Memory Allocation Perspectives」](https://techchannel.com/Trends/01/2021/ibm-i-performance-data-investigator)
* 待機アカウンティング
  * [IBM i Wait Accounting](https://www.ibm.com/support/pages/ibm-i-wait-accounting)
  * [Blog「i Can Tell You Why You’re Waiting」](https://dawnmayi.com/2009/11/16/i-can-tell-you-why-youre-waiting/)
  * [「Job Waits and iDoctor for IBM i White Paper」](https://public.dhe.ibm.com/services/us/igsc/idoctor/Job_Waits_White_Paper.pdf)
  
　


<P></P>


---


<P></P>

### その他参考情報

<P></P>

－－－－－－－－

<P></P>

* OSの制限事項(最大処理能力)：[7.5](https://www.ibm.com/docs/ja/i/7.5?topic=availability-maximum-capacities), [7.4](https://www.ibm.com/docs/ja/i/7.4?topic=availability-maximum-capacities), [7.3](https://www.ibm.com/docs/ja/i/7.3?topic=availability-maximum-capacities), [7.2](https://www.ibm.com/docs/ja/i/7.2?topic=availability-maximum-capacities), [7.1](https://www.ibm.com/docs/ja/i/7.1?topic=availability-maximum-capacities)

* プログラム資料説明書 (Memo to Users)
  * プログラム資料説明書：[7.5](https://www.ibm.com/docs/ja/i/7.5?topic=documentation-memo-users), [7.4](https://www.ibm.com/docs/ja/i/7.4?topic=information-memo-users), [7.3](https://www.ibm.com/docs/ja/i/7.3?topic=documentation-memo-users), [7.2](https://www.ibm.com/docs/ja/i/7.2?topic=information-memo-users), [7.1](https://www.ibm.com/docs/ja/i/7.1?topic=information-memo-users)
  * リリース後の変更一覧 → [Memo To Users Document has been updated](https://www.ibm.com/support/pages/memo-users-document-has-been-updated)
  
* HMC
  * [Recommended Fixes - HMC Code Upgrades](https://www.ibm.com/support/pages/recommended-fixes-hmc-code-upgrades)
  * [Updating to HMC v9](https://techchannel.com/SMB/03/2021/updating-hmc-v9)

