---
layout: post
title:  "現行版Navigator for i のLog4j脆弱性は修正されない"
date:   2022-01-20 10:10:10 +0900
categories: Navigator for i
---
2022/1/10付けのIBMサポートの文書[「Security Bulletin: IBM i components are affected by CVE-2021-4104 (log4j version 1.x)」](https://www.ibm.com/support/pages/node/6539162)に、<span style="color: red">「IBM Navigator for i - heritage version は log4j v1.x を使用しており、log4j v2.x へのアップデートや使用停止はできません。 顧客は、IBM Navigator for i の heritage version の使用を中止することで、CVE を軽減することができます。」</span>と記載されています。つまり、**現在ほとんどのユーザーが利用している従来のNavigator for i はセキュリティの脆弱性への対処を行わない**ので、利用しないようにとのこと。

Navigator for i を使っていなければ実質的な影響はありません。もし利用している場合、多くの機能(NetServer共有の作成などは標準では不可)は5250画面で代替できます。あるいは、新しいNavigator for i に乗り換えるよう”強く推奨”されていますが、次のような懸念があります。

* Navigator for i に設定した項目が失われる可能性がある? (「ターゲット・システム」や「お気に入り」とか...)
* メニューや操作方法が全く異なるので慣れるのに時間を要する (新Naviの詳細を解説した資料は見たことがありません)
* 新Naviでサポートされない機能がある (詳細な確認はしていませんが、データベースタスクの一部や、区画関連など)
* IBM i 7.2はEOSなのでそもそも新Naviが使えない (おそらくそのまま)

追加の情報は下記サイトなども参照ください。

* [Log4j Hits Heritage Version of Navigator for i – No Patch Coming](https://www.itjungle.com/2022/01/12/log4j-hits-heritage-version-of-navigator-for-i-no-patch-coming/) (January 12, 2022)
* [No Plan To Support New Nav on Older IBM i Releases, IBM Says](https://www.itjungle.com/2022/01/19/no-plan-to-support-new-nav-on-older-ibm-i-releases-ibm-says/) (January 19, 2022)
