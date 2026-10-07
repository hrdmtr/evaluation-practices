import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT))

from src.evaluation.recall import recall_at_k


BASE_DIR = Path(__file__).parent

with open(BASE_DIR / "data/golden.json", encoding="utf-8") as f:
    golden = json.load(f)

with open(BASE_DIR / "data/results.json", encoding="utf-8") as f:
    results = json.load(f)


for gold, result in zip(golden, results):
    print(f"\nquery: {gold['query']}")

    for k in [1, 3, 5]:
        recall = recall_at_k(
            gold["relevant_ids"],
            result["retrieved_ids"],
            k,
        )

        print(f"Recall@{k}: {recall:.3f}")
