---
layout: post
title:  "ObjectConnectのネイティブTCP/IPサポート"
date:   2021-01-28 10:10:10 +0900
tags: [TCP/IP]
---
唯一？残っていたSNAの残滓にObjectConnectがありましたが、ついにTCP/IPをネイティブにサポートしたようです。

詳細はIBMのサポート文書[「ObjectConnect over TCP/IP」](https://www.ibm.com/support/pages/objectconnect-over-tcpip)を参照ください。今の所7.4のみPTF[「SI73828 - add native TCP support to ObjectConnect」](https://www.ibm.com/support/pages/ptf/SI73828)が出ていますが、7.2や7.3にもPTFバックしてほしいものです。

[ObjectConnect](https://www.ibm.com/docs/en/i/7.4?topic=system-objectconnect-function)は有償のOSオプションですが、SAVRSTxxxコマンドで複数のサーバー/区画間で\*PGMや\*FILEをFTPより容易・高速に転送できます。下記はサポート文書の翻訳から抜粋したものです。

* システムは、オンライン保管ファイル(SAVF)や配布待ち行列を使用せずに、オブジェクトをターゲットシステムに直接コピーします。
* ObjectConnectは、コピーされるオブジェクトの中間コピーを格納するための追加のディスク領域を必要としません。
* ObjectConnectは、システム間でオブジェクトをコピーする他の方法よりも全体的なパフォーマンスが優れている傾向があります。

ObjectConnectのためだけにSNA/EEを構成していたお客様もいらっしゃったくらいなので、頻繁にオブジェクト転送を行う場合はSAVF+FTPの代替として検討する価値があるでしょう。

　

---

　

#### 2021-06-10追記：ObjectConnect on TCP/IPはDCMが前提

当初のIBMのサポート文書には「strongly suggested you assign a certificate」と記載され、IBM Communityでも[ディスカッション](https://community.ibm.com/community/user/power/discussion/objectconnect-over-tcpip)されていましたが、[こちらのサイト](https://blog.easi.net/en/services/ibm-power-systems/the-question-to-encrypt-or-not-to-encrypt-is-now-answered-by-ibm-i)の記載のように、実際はDCMが**「必須」**らしいです(構成していないと STRTCPSVR SERVER(*OBJC) ででエラーで起動しない)。このサイトでは、暗号化を必須とした理由を次のように推測しています。(本当の理由は不明)

1. growing awareness for a better security. (セキュリティへの関心が高まっている)
1. IBM does not break something which is already there. (現行の仕組みに影響させない)

重要な前提があいまいだったケースでは、Db2 Mirrorの初期バージョンの構成に「外部ストレージが必須」というのもありました。新しい機能を検討する際は、前提を明確にしないとお客様にご迷惑をおかけすることになるので気をつけたいです。

　

---

　

#### 2021-09-14追記：ObjectConnect over TCP/IPの構成に証明書を不要とする要望(RFE)

2021-06-10に書いたように、ObjectConnect over TCP/IPを利用するには「証明書」が必要です。もちろんEEで構成すれば使えるのですが、いまさらSNAの構成を作るのも将来的に禍根を残しそうであまりやりたくないですね。

この不便を解消するためのRFE[「Remove certificate requirement from ObjectConnect over TCP/IP」](https://ibm-power-systems.ideas.ibm.com/ideas/IBMI-I-2532)(要ログイン)がSubmitされていますがどうなる事やら...

※ ちなみに、この機能を7.3にPTF backするRFE 145962は、「複雑なため」却下されています。


　

---

　

#### 2021-11-29追記：RFE却下

RFEは却下されました。下記がIBMのコメントです。

<blockquote>
<font size=3>
IBM does not intend to provide a solution to this request, so it is being closed. 
<BR>
Configuring certificates is a common activity for security/system administrators today and becomes easier to do with each new DCM, API, or SQL Service enhancement. There is information, examples and internet videos available to administrators on how to use DCM and configure certificates.
</font>
</blockquote>

IBM i 独自のDCM(あるいはAPIやSQLサービス)による認証が**一般的なタスク**で、かつ、情報・サンプル・動画などが提供されている、のが理由だそうです。
