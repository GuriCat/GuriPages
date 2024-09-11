---
layout: post
title:  "新しいDb2 for i クライアント Mapepire"
date:   2024-09-11 13:48:37 +0900
tags: [Db2, OSS]
---
8月30日に、IBMは「Mapepire」というクラウド、コンテナ、OSS言語(Python、Node.js、Java)に対応したDb2 for i クライアントのTechnology Previewを発表しました。

Mapepireは「シンプルさとパフォーマンスを念頭に置いて構築された、クラウド対応の IBM i データベース アクセス レイヤー」と[GitHubページ](https://mapepire-ibmi.github.io/){:target="_blank"}に記載されています。詳しくはGitHubページのほか、下記を参照ください。

- ITJungleの記事[「BM Introduces Mapepire, The New Db2 For i Client (英語)」](https://www.itjungle.com/2024/09/09/ibm-introduces-mapepire-the-new-db2-for-i-client/){:target="_blank"}
- [worksofliam/blog Mapepire: A new IBM i database client #68](https://github.com/worksofliam/blog/issues/68){:target="_blank"}

Mapepireは「マ**パ**イアー」?(‘mapəpɪə’ or ‘MAH-pup-ee’。[発音を聞く](https://www.youtube.com/watch?v=qIdnIyAFT8A){:target="_blank"})とするらしく、ロゴは南アメリカに生息する有毒なマムシを表しています。
<img src="/GuriPages/image/2024-09-11_mapepire.png" width="300" />
<hr>
Mapepireは、一言でいうとUNIX ODBCおよびJDBCドライバーの代替です。GitHubでは下表のようにMapepireとJDBCおよびODBCを比較しています。

|                    |JDBC|ODBC|Mapepire|
|-------------------|--|--|--|
|必要なポートは1つだけ|  |  |✅|
|データは常に暗号化される|  |  |✅|
|システム出口点で管理可能|✅|✅|✅|
|強化されたCCSIDサポート|✅|	 |✅|
|WatsonX.ai Jupyter Notebooksで実行|   |  |✅|
|軽量コンテナで実行|✅|  |✅|
|複数のClient言語を直接サポート|  |   |✅|

<br>

以下はざっと[GitHub](https://mapepire-ibmi.github.io/){:target="_blank"}を眺めた個人的な感想です。

**従来のDBドライバーより優れている点**

- Secure web socketsで実装しており、可搬性に優れている。
- 動作が軽くレスポンスが高速。ODBCとのパフォーマンス比較は[こちら(英文)](https://github.com/worksofliam/blog/issues/69){:target="_blank"}。
- プラットフォームへの依存性が低く、クラウドでの利用やコンテナ化が容易。
- クライアントにDBドライバー(ODBCのような)のインストールが不要。

**懸念点**

- RPG(ILEを含む)からは利用できず、プランにも記載なし。
- 現時点でTechnology Previewであり、本番業務に採用しにくい。
- 通信を暗号化するため証明書管理が必要。自動的に自己署名証明書を生成する機能があるが、この検証は現在サポートされていない。

<hr>
<br>

[YouTubeの動画](https://youtu.be/RUOfH6U5tRk?t=1079){:target="_blank"}や[リスキリング資料](https://guricat.github.io/Web-Service-on-IBM-i/#/2_Web%E3%82%B5%E3%83%BC%E3%83%93%E3%82%B9%E6%A6%82%E8%A6%81?id=%e5%8f%82%e8%80%83-web%e3%82%b5%e3%83%bc%e3%83%93%e3%82%b9%e3%83%bb%e3%82%b5%e3%83%bc%e3%83%90%e3%83%bc%e3%81%ae%e3%83%91%e3%83%95%e3%82%a9%e3%83%bc%e3%83%9e%e3%83%b3%e3%82%b9){:target="_blank"}でWebサービス・サーバーの簡易パフォーマンス調査をしたことがあります。

IBM i がサーバーの場合、TCP/IP経由で高密度のDBリクエストが発生すると、DBサーバー・ジョブであるQZDASOINITが大量に生成され、これが一定数に達するとリクエストをさばき切れなくなりました。Mapepireでこのような状況が改善される可能性があります。

RPGがネイティブでサポートされない(ILE-RPGからJavaメソッドを呼び出せば使えるかも)のは残念ですが、今後が楽しみです。


<br>

{::comment}
タグ
tags: [V7R5, V7R4, ACS, TR]

EOS
V7R3
V7R4
V7R5
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
RDi
RDX
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
