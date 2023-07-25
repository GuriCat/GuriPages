---
layout: post
title:  "Authority collection (権限収集)は役に立つか？"
date:   2022-03-11 10:10:10 +0900
categories: セキュリティ
---
IBM i 7.3からOSに組み込まれた[Authority collection(権限収集)](https://www.ibm.com/docs/ja/i/7.3?topic=reference-authority-collection)機能は、使い方が難しい機能と思っています。Authority collection自体は「誰が、何を、どのレベルの権限で<span style="color: blue">アクセスしたか</span>」を収集します。収集された情報を評価するには、「誰が、何を、どのレベルの権限で<span style="color: red">アクセスすべきか</span>」を決める必要があり、そのために多くの時間と工数が必要です。厳格なセキュリティを適用するためのリソース確保が難しい場合は、[「Is Authority Collection The Right Thing For IBM i Security?」](https://www.itjungle.com/2019/08/12/is-authority-collection-the-right-thing-for-ibm-i-security/)に記載されているようにツールの利用を検討するか、あるいは、これまで通りにAuthority collectionに依存しないセキュリティモデルを考えるべきでしょう。

セキュリティ関連では2017年4月の[「State Of IBM i Security: Seven Areas That Demand Attention」](https://www.itjungle.com/2017/04/24/state-ibm-security-seven-areas-demand-attention/)という記事も興味深いです。「2016年に332のシステムで実施されたセキュリティ評価に基づいたレポートの調査結果」を紹介しており、今でも8年前と大きく状況は変わっていない気がするので興味のある方はご一読をどうぞ。

また、[「Guru: IBM i Experience Sharing, Case 1 – Object Authority Check And Batch Job Performance」](https://www.itjungle.com/2022/03/07/guru-ibm-i-experience-sharing-case-1-object-authority-check-and-batch-job-performance/)のように、適切な権限を付与して**バッチ処理時間が8時間→4.5時間に短縮**された例もあります。正しい知識(スキル)に基づいてバランスをとる事が肝要でしょう。
