---
layout: post
title:  "GO SAVE/GO RESTOREで制限状態の挙動が変化"
date:   2021-04-01 10:10:10 +0900
categories: OS
---
IBM i 7.2/7.3/7.4に特定のPTFを適用すると、「システムがすでに制限状態の場合にENDSBSをスキップする」そうです(詳細は[こちら](https://www.ibm.com/support/pages/improvement-restricted-state-processing-go-save-and-go-restore))。余分なENDSBSを行わないことで時間が短縮できる、制限状態で限定的にTCP/IPサービスを利用できる、ことがメリットと記載されています。

「TCP/IP終了待ち時間」(デフォルトで300秒)はENDSBSチェックの前に独立して処理されるので、この値が*NONE(すべてのサブシステムを終了する前にTCP/IP処理の終了は行われない)以外の場合はTCP/IPサービスが終了される、と書かれています。

特にGO SAVE/GO RESTOREの操作に変更は不要と思いますが、動作は把握しておくと良いでしょう。
