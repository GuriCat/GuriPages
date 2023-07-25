---
layout: post
title:  "What's all the fuss about NVMe with IBM i (IBM i ＋NVMeの大騒ぎは何？)"
date:   2021-03-24 10:10:10 +0900
categories: ハードウェア
---
表題のタイトルの[動画](https://www.youtube.com/watch?v=kkmmQ9T-CsQ&t=2523s)が公開されています。全編英語ですが、YouTubeなので字幕を出して英語→日本語に翻訳して見れます。

内容は、IBMがLab Serviceで行ったHDDとNVMeのパフォーマンスとコストの比較です(IBMの正式なテストでは有りません)。パフォーマンスは言わずもがなでNVMeがHDDを圧倒します(下図参照。青がNVMe、オレンジはHDD/ミラー、灰色はHDD/RAID6)。コストも、P05構成で30%、P10構成だと46%もNVMe構成の方が廉価になります。

Q&Aで次のような点を挙げています。

* NVMeはホットスワップ不可？ → <span style="color: red">AiCは不可</span>、<span style="color: blue">U.2は可能</span>。
  * [古いM.2 NVMe以外は活性保守が可能](https://community.ibm.com/community/user/power/communities/community-home/digestviewer/viewthread?MessageKey=f010d039-7e4c-4691-989f-3d07df69b2fe&CommunityKey=f0246bc4-08f3-43c5-a7f8-b6a64d387894&tab=digestviewer#bmf010d039-7e4c-4691-989f-3d07df69b2fe)だそうです。「... it does have a number of other considerations and pre-requites but never the less both the U.2 and AIC  NVMe can be concurrently maintained.」
* NVMeは劣化する？ → はい。しかし従来のSSDより長寿命で、Fuel gauge (寿命表示)も利用可能。

非常に小規模でパフォーマンスを考慮せずにとにかく最安にする場合、あるいは外部ストレージが必要な大規模な構成の場合を除き、最新のPOWER9サーバーとIBM i 7.4であれば、NVMe(SSD)にしない理由を見つける方が難しいかもしれません。

　

![2021-03-24-What's all the fuss about NVMe with IBM i (IBM i ＋NVMeの大騒ぎは何？).jpg](/GuriPages/image/2021-03-24-What's all the fuss about NVMe with IBM i (IBM i ＋NVMeの大騒ぎは何？).jpg)

　

---

　

#### 2021-03-30 追記

「IBM Power Systems Community」の[ディスカッション](https://community.ibm.com/community/user/power/communities/community-home/digestviewer/viewthread?MessageKey=2b799bb4-ee33-4529-9208-0dcff9930ee6&CommunityKey=f0246bc4-08f3-43c5-a7f8-b6a64d387894&tab=digestviewer#bm2b799bb4-ee33-4529-9208-0dcff9930ee6)から。

* PCIe Gen3 AiCは5DWPD(Drive Write Per Day)、Gen4 AiC (現時点でU.2同等)は3DWPD。Gen4は潜在的にGen3より2.5倍高速なので、それほどパフォーマンスを必要としない、あるいは、3DWPDで耐久性が不足する場合はGen3 AiCの選択もあり？
* AiCはU.2よりコストパフォーマンスが良いが、U.2を選択する理由は次の点。
  * いずれも並行保守可能だが、多くの場合にU.2ははるかに保守が容易で低リスク(サーバーの上を取らなくてもよいので、誤ってケーブルを抜いたりする恐れが少ない)。
  * 最大4個のU.2 NVMeを内部PCIeスロットを消費せずにサーバー前面に設置可能。空いたPCIeスロットは、SASやネットワーク、Fibreなどに利用できる。

結論。「Whilst there is no 100% right answer as to whether you should always choose AiC or U.2 NMVe, I'm still pretty confident you should always choose NMVe over HDD.」 → **AiCかU.2かはケースによるが、常にHDDではなくMVNeを選択すべき。**

　

---

　

#### 2021-05-21 追記

IBM Power Systems Communityの表題の[投稿](https://community.ibm.com/community/user/power/communities/community-home/digestviewer/viewthread?MessageKey=3b170cbf-77dd-4875-b3b7-e0e495512a5a&CommunityKey=f0246bc4-08f3-43c5-a7f8-b6a64d387894&tab=digestviewer#bm3b170cbf-77dd-4875-b3b7-e0e495512a5a)ですが、NVMeから派生し、VIOSとIBM i ホスティングとの比較、NVMe利用時の騒音増加と対応パッチ、など興味深い内容です。Google翻訳版は[こちら](/GuriPages/image/IBM i-IBM Power Systems Community.pdf)でどうぞ。
