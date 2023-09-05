---
layout: post
title:  "Announcing IBM i 7.4 TR2 and 7.3 TR8"
date:   2020-04-14 10:10:10 +0900
tags: [ACS, TR, SQL, V7R4, V7R3]
---
表題の[TR](https://www.ibm.com/support/pages/node/1119129)が発表されました。詳しくはこちら([7.4 TR2](https://www.ibm.com/support/pages/ibm-i-74-tr2-enhancements), [7.3 TR8](https://www.ibm.com/support/pages/node/6155511))を参照ください。

有用と思われる項目をリストします。

* Db2 Mirror for i の初期設定で外部ストレージが不要。提案できる構成が大幅に増えます。
* [ACS 1.1.8.4](https://www.ibm.com/support/pages/ibm-i-access-client-solutions-1184)の発表。RFE 132374の反映で半角(SBCS)の「￥」と「＼」を同時に使えるようになりました。他に有用そうなのは、「WindowsのPDT印刷でユーザー定義文字のフォント・イメージ・ファイルを生成」や、「IBM i 内部でバッチでACSデータ転送を起動してExcelファイルなどを作成」、「テーブルの比較機能」など。細々と多くの機能が拡張されています。
* 仮想テープライブラリー装置の構成・利用が容易に。NWSDで、FC＋SAN S/W or VIOSを代替する？詳細不明。
* IBM i サービス(SQL)の拡張。例えば、パフォーマンス次第では[「LIBRARY_INFOテーブル関数」](https://www.ibm.com/docs/en/i/7.4?topic=services-library-info-table-function)がRTVDSKINFの代替に使えるかも。他にサブシステム記述関連を取得するサービス、ユーザーや経過日数など指定した条件でスプールファイルを削除する[「SYSTOOLS.DELETE_OLD_SPOOLED_FILES」](https://www.ibm.com/support/pages/node/6174519)など。
