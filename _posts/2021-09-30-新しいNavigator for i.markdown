---
layout: post
title:  "新しいNavigator for i"
date:   2021-09-30 10:10:10 +0900
tags: [Navigator]
---
2021/09/28に7.4の前提PTF「IBM HTTP Server for i レベル14」が公開されたので試してみました。設定があるのか分かりませんが、「ビューの切り替え」、「カスタム・グラフ」、「新規ノードの追加」、「製品情報」、「保守容易性(接続設定)」が表示されました。[「Navigator for i」](https://www.ibm.com/support/pages/node/6483299)(IBM Supportサイト)やTechChannelの[「IBM i New Navigator」](https://techchannel.com/SMB/09/2021/ibm-i-new-nav)にはいろいろ書いていますが、まだデモ版レベルなので今後の拡張に期待です。

なお、新しいNavigatorのURLは`http://hostname:2002/Navigator`で、従来のNavigatorへは`http://hostname:2004/ibm/console`で、任意に切り替えてアクセスできると[「IBM Navigator for i - Heritage Version」](https://www.ibm.com/support/pages/node/1142704)に記載されています。ポート2001にアクセスした場合もこのURLにリダイレクトされます。
