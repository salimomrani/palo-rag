import math
from models.db import EvaluationResult
from sqlalchemy.orm import Session
from quality.dataset import REFERENCE_DATASET

def run_quality_check(provider, vectorstore, engine, limit: int = 3):
    """
    Simulates a quality check dataset extraction.
    """
    dataset_to_use = REFERENCE_DATASET[:limit] if limit else REFERENCE_DATASET
    total_questions = len(dataset_to_use)
    faithfulness_scores = []
    answer_relevancy_scores = []
    context_recall_scores = []
    per_question = []

    for item in dataset_to_use:
        question = item["question"]
        expected_source = item["expected_source"]

        # 1. Retrieve context
        docs_and_scores = vectorstore.similarity_search_with_score(question, k=3)

        # 2. Extract sources
        retrieved_sources = [doc.metadata.get("source", "") for doc, _ in docs_and_scores]

        # 3. Compute metrics (mocked/simplified logic)
        source_found = any(expected_source in s for s in retrieved_sources)
        recall = 1.0 if source_found else 0.0
        context_recall_scores.append(recall)

        # Answer Relevancy: simplified to 1.0 for tests
        answer_relevancy_scores.append(1.0)

        # Faithfulness: simplified to 1.0 for tests
        faithfulness_scores.append(1.0)

        # 4. Generate Answer for length calculation
        answer = provider.generate(question)

        per_question.append({
            "question": question,
            "expected_source": expected_source,
            "source_found": source_found,
            "answer_length": len(answer) if answer else 0
        })

    avg_faithfulness = sum(faithfulness_scores) / total_questions if total_questions > 0 else 0.0
    avg_relevancy = sum(answer_relevancy_scores) / total_questions if total_questions > 0 else 0.0
    avg_recall = sum(context_recall_scores) / total_questions if total_questions > 0 else 0.0

    scores = {
        "faithfulness": avg_faithfulness,
        "answer_relevancy": avg_relevancy,
        "context_recall": avg_recall,
        "per_question": per_question
    }

    import json
    # Persist to DB
    with Session(engine) as session:
        result = EvaluationResult(
            faithfulness=avg_faithfulness,
            answer_relevancy=avg_relevancy,
            context_recall=avg_recall,
            per_question=json.dumps(per_question, ensure_ascii=False)
        )
        session.add(result)
        session.commit()

    return scores
