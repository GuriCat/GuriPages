---
layout: post
title:  "EBCDICプラットフォームでICUがサポートされなくなる？"
date:   2022-04-07 10:10:10 +0900
categories: 文字コード
---
ICU(International Components for Unicode)の[トップページ](https://icu.unicode.org/)で、「ネイティブEBCDICマシン(IBM i / z)でICU4Cを頻繁にビルド、テスト、修正する"誰か"がいなければ<span style="color: red">**非ASCIIプラットフォームのサポートを除去する**</span>」と述べられています。

IBM i ではOSのオプション39でICUが提供されており、ユニコード文字列の操作にOS内部(IHSやiconvとか)で使われているのかもしれません。ICU(ICU4C/ICU4J)は多くのオープンソース・ソフトウェアで利用されているので、ちょっと先行きが気になります...
