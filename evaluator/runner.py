import json
import time
from evaluator.metrics import calculate_accuracy
from app.llm import classify_email
from app.logger import get_logger

logger = get_logger(__name__)

DATASET_PATH = "dataset/golden_dataset.json"
PROMPT_PATH = "app/prompts/classifier_v2.yaml"
REPORT_PATH = "reports/evaluation_v2.json"

def load_dataset(path):
    with open(path, "r", encoding="utf-8") as file:

        return json.load(file)


def evaluate():
    dataset = load_dataset(DATASET_PATH)
    logger.info("Starting evaluation")
    logger.info(f"Loaded {len(dataset)} items from dataset")
    results = []
    for item in dataset:
        start_time = time.perf_counter()
        prediction = classify_email(
            email= item["email"],
            prompt_file= PROMPT_PATH
            )
        latency = time.perf_counter() - start_time
        correct = (
            prediction.category.strip().lower() == item["expected_category"].strip().lower()
        )
                    
        results.append(
            {
                   "id": item["id"],
                 "email": item["email"],
                 "expected": item["expected_category"],
                 "predicted": prediction.category,
                 "correct": correct,
                 "summary": prediction.summary,
                 "latency_seconds": round(latency, 3)
            }
        )
        logger.info(
            "Case %s | Expected: %s | Predicted: %s | Correct: %s | Latency: %.3f seconds",
            item["id"],
            item["expected_category"],
            prediction.category,
            correct,
            latency,
        )
        print(
            f"[{item['id']}]"
            f"expected: {item['expected_category']} |"
            f"predicted: {prediction.category} |"
            f"correct: {'correct' if correct else 'incorrect'}"
            f"latency: {round(latency, 3)} seconds"
        )
    logger.info("Evaluation completed")
    with open(REPORT_PATH, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=4)
    return results

if __name__ == "__main__":
    results = evaluate()

    accuracy = calculate_accuracy(results)

    print()
    print(f"Accuracy: {accuracy:.2%}")