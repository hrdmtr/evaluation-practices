def recall_at_k(relevant_ids, retrieved_ids, k):
    relevant = set(relevant_ids)
    retrieved_at_k = set(retrieved_ids[:k])

    hits = relevant & retrieved_at_k

    return len(hits) / len(relevant)
