import json
import time
from evaluator.metrics import calculate_accuracy
from app.llm import classify_email

DATASET_PATH = "dataset/golden_dataset.json"
PROMPT_PATH = "app/prompts/classifier_v2.yaml"
REPORT_PATH = "reports/evaluation_v2.json"

def load_dataset(path):
    with open(path, "r", encoding="utf-8") as file:

        return json.load(file)
def evaluate():
    dataset = load_dataset(DATASET_PATH)
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
        print(
            f"[{item['id']}]"
            f"expected: {item['expected_category']} |"
            f"predicted: {prediction.category} |"
            f"correct: {'correct' if correct else 'incorrect'}"
            f"latency: {round(latency, 3)} seconds"
        )
    with open(REPORT_PATH, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=4)
    return results

if __name__ == "__main__":
    results = evaluate()

    accuracy = calculate_accuracy(results)

    print()
    print(f"Accuracy: {accuracy:.2%}")