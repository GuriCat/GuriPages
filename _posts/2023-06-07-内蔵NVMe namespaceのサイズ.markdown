---
layout: post
title:  "内蔵NVMe namespaceのサイズ"
date:   2023-06-07 10:10:10 +0900
categories: インフラ
---
Power10は触っていないのですが、内蔵ストレージがNVMeなのでHDD/SSD時代とは手順がかなり違うようですね。

* [Creating NVMe namespaces and adding them to an ASP](https://www.ibm.com/support/pages/creating-nvme-namespaces-and-adding-them-asp) (IBMサポート文書)
* [NVMe - Configuring and adding Name Spaces to IBM i](https://www.youtube.com/watch?v=8z0nnZsGkLE) (YouTube)
* [「NVMe」市場にでて1年、その評価は？](https://www.jbcc.co.jp/products/files/ibmpowercolumn20220128_NVMe_rev.pdf) (JBCC社の資料)

IBM i は(仮想)アーム数が一定数あったほうが効率よく動くので、NVMe namespace (StorageでいうLUNのようなもの?)のサイズは、1.6TBのNVMeは188GB、3.2/6.4TBのNVMeなら393GBがよさそう。下の表はIBM Communityの[「Migrate to NVME mirrored by IBM i」](https://community.ibm.com/community/user/power/discussion/migrate-to-nvme-mirrored-by-ibm-i#bm3467e34d-1262-4ae4-8419-854d25b8fea7)というスレッドに貼ってあったもので出所は判りません。

![2023-06-07_chart.jpg](/image/2023-06-07_chart.jpg)
---
2023-06-08追記：IBM Communityの[元スレッド](https://community.ibm.com/community/user/power/discussion/migrate-to-nvme-mirrored-by-ibm-i#bma3e7035b-6eb1-40d9-b780-c39000ba2ee1)より。

<blockquote>
<p>もう一つ注意点があります。</p>

<p>あなたのシステムを受け取ったとき、ロードソース用に1つのネームスペースがすでに作成されています。しかし、この名前空間は800GBのものである。これは私たちが望むものではありません。</p>

<p>Dモード(マニュアル)でslicのdvdかusb、またはsavsysのtapeでシステムを起動します。ここで、既存の名前空間を削除し、ロードソース用に新しい名前空間（188GBまたは393GB）を作成することができます。IBMのlicpgmsがプリインストールされたシステムを注文した場合、上記の手順ですべてを削除することになるので注意してください。</p>

<p>Fabianが言ったように、ディスクの応答時間やシステム全体の応答時間に驚くことでしょう。最初の正常なIPLの間に、もうコーヒーを飲む暇もないでしょう。</p>
</blockquote>
