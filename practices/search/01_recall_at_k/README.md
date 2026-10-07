Practice 01: Recall@k

目的

このプラクティスでは、検索システムの評価指標である Recall@k を、実際に小さなデータセットを使って計算します。

このプラクティスを終えると、以下を説明できることを目標とします。

* Recall とは何を評価する指標なのか
* @k は何を意味するのか
* Golden Set（正解データ）がなぜ必要なのか
* Recall@k が高い／低いとはどういう状態なのか
* Recall@k だけでは評価できない検索品質があること

⸻

1. Recallとは

Recall（再現率）は、

本来取得すべき正解を、検索システムがどれだけ取得できたか

を表す指標です。

基本式は次のとおりです。

Recall = 取得できた正解数 / 全正解数

たとえば、ある検索クエリに対して正解の商品が3件あるとします。

item_001
item_003
item_007

検索システムがそのうち、

item_001
item_003

の2件を取得できた場合、

Recall = 2 / 3 = 0.667

となります。

⸻

2. Recall@kとは

実際の検索システムでは検索結果に順位があります。

たとえば、

1位 item_001
2位 item_020
3位 item_003
4位 item_015
5位 item_030

という検索結果が返されたとします。

Recall@k の k は、

検索結果の上位何件までを評価対象にするか

を意味します。

たとえば Recall@3 なら、上位3件だけを評価します。

1位 item_001
2位 item_020
3位 item_003

⸻

3. Golden Set

検索品質を評価するためには、

「このクエリに対して、本来何が検索されるべきなのか」

という正解が必要です。

このプラクティスでは data/golden.json に正解を定義しています。

[
  {
    "query": "赤いランニングシューズ",
    "relevant_ids": ["item_001", "item_003", "item_007"]
  },
  {
    "query": "防水の黒いリュック",
    "relevant_ids": ["item_010", "item_012"]
  }
]

たとえば、

赤いランニングシューズ

という検索に対して、

item_001
item_003
item_007

の3商品を正解としています。

このような評価用の正解データを、このプラクティスでは Golden Set と呼びます。

実際の検索評価では、この「何を正解とするか」が非常に重要になります。

⸻

4. 検索結果

検索システムが返した結果を data/results.json に定義しています。

[
  {
    "query": "赤いランニングシューズ",
    "retrieved_ids": ["item_001", "item_020", "item_003", "item_015", "item_030"]
  },
  {
    "query": "防水の黒いリュック",
    "retrieved_ids": ["item_020", "item_010", "item_021", "item_022", "item_023"]
  }
]

Golden Set と検索結果を比較することで Recall@k を計算できます。

⸻

5. Recall@kを手で計算する

Query 1: 赤いランニングシューズ

正解は3件です。

item_001
item_003
item_007

検索結果は、

1位 item_001  ← 正解
2位 item_020
3位 item_003  ← 正解
4位 item_015
5位 item_030

です。

Recall@1

Top 1 に含まれる正解は item_001 の1件です。

Recall@1
= 1 / 3
= 0.333

Recall@3

Top 3 には、

item_001
item_003

の2件の正解があります。

Recall@3
= 2 / 3
= 0.667

Recall@5

Top 5 に広げても item_007 は検索されていません。

したがって、

Recall@5
= 2 / 3
= 0.667

となります。

⸻

6. もう一つの例

Query 2: 防水の黒いリュック

正解は、

item_010
item_012

の2件です。

検索結果は、

1位 item_020
2位 item_010  ← 正解
3位 item_021
4位 item_022
5位 item_023

です。

したがって、

Recall@1 = 0 / 2 = 0.000
Recall@3 = 1 / 2 = 0.500
Recall@5 = 1 / 2 = 0.500

となります。

⸻

7. 実装

Recall@k の実装は src/evaluation/recall.py にあります。

def recall_at_k(relevant_ids, retrieved_ids, k):
    relevant = set(relevant_ids)
    retrieved_at_k = set(retrieved_ids[:k])
    hits = relevant & retrieved_at_k
    return len(hits) / len(relevant)

処理は非常に単純です。

まず正解集合を作ります。

relevant = set(relevant_ids)

次に検索結果の Top k を取得します。

retrieved_at_k = set(retrieved_ids[:k])

そして両方に含まれるIDを求めます。

hits = relevant & retrieved_at_k

最後に、

取得できた正解数 / 全正解数

を計算します。

⸻

8. 実行

リポジトリのルートディレクトリから実行します。

python practices/search/01_recall_at_k/run.py

実行結果：

query: 赤いランニングシューズ
Recall@1: 0.333
Recall@3: 0.667
Recall@5: 0.667
query: 防水の黒いリュック
Recall@1: 0.000
Recall@3: 0.500
Recall@5: 0.500

⸻

9. Recall@kから分かること

Recall@kを見ることで、

検索結果の上位k件までに、本来取得すべきものをどれだけ回収できているか

を評価できます。

たとえば、

Recall@5 = 0.8

なら、

正解商品の80%がTop 5までに取得できている

という意味になります。

検索システムが「必要なものを取りこぼしていないか」を評価する際に重要な指標です。

⸻

10. Recall@kでは分からないこと

Recall@kには重要な特徴があります。

Top k の中での順位を区別しません。

たとえば正解が item_010 だった場合、

1位 item_010

でも、

3位 item_010

でも、Recall@3では同じ結果になります。

つまり Recall@k は、

Top k に正解が入っているか

を見ることはできますが、

正解がどれだけ上位に表示されたか

を十分に評価することはできません。

EC検索などでは、

正しい商品が検索結果に存在する

だけでなく、

正しい商品がユーザーの目に入りやすい上位に表示される

ことも重要です。

そのため実際の検索評価では Recall@k だけでなく、順位を考慮する別の評価指標も組み合わせます。

次のプラクティスでは、この問題を確認した上で MRR（Mean Reciprocal Rank） を扱います。

