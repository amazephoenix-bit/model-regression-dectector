import json
import statistics

from app.logger import get_logger

logger = get_logger(__name__)
V1_PATH = "reports/evaluation_v1.json"
V2_PATH = "reports/evaluation_v2.json"
ACCURACY_THRESHOLD = 0.05


def load_report(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def calculate_accuracy(results):
    correct = sum(1 for item in results if item["correct"])
    total = len(results)

    return correct / total if total else 0


def calculate_average_latency(results):
    latencies = [
        item["latency_seconds"]
        for item in results
        if "latency_seconds" in item
    ]

    return statistics.mean(latencies) if latencies else 0


def compare():
    v1 = load_report(V1_PATH)
    v2 = load_report(V2_PATH)
    logger.info("Starting regression comparison")
    v1_accuracy = calculate_accuracy(v1)
    v2_accuracy = calculate_accuracy(v2)

    v1_latency = calculate_average_latency(v1)
    v2_latency = calculate_average_latency(v2)

    accuracy_change = v2_accuracy - v1_accuracy
    latency_change = v2_latency - v1_latency

    print("================================")
    print("       MODEL REGRESSION TEST")
    print("================================")

    print()
    print(f"V1 Accuracy: {v1_accuracy:.2%}")
    print(f"V2 Accuracy: {v2_accuracy:.2%}")
    print(f"Accuracy Change: {accuracy_change:+.2%}")
    logger.info(
        "V1 accuracy=%.2f%% | V2 accuracy=%.2f%% | change=%+.2f%%",
        v1_accuracy * 100,
        v2_accuracy * 100,
        accuracy_change * 100
    )


    print()
    print(f"V1 Avg Latency: {v1_latency:.3f}s")
    print(f"V2 Avg Latency: {v2_latency:.3f}s")
    print(f"Latency Change: {latency_change:+.3f}s")
    logger.info(
        "V1 latency=%.3fs | V2 latency=%.3fs | change=%+.3fs",
        v1_latency,
        v2_latency,
        latency_change
    )

    improved = []
    regressed = []

    for old, new in zip(v1, v2):
        if not old["correct"] and new["correct"]:
            improved.append(new)

        elif old["correct"] and not new["correct"]:
            regressed.append(new)

    print()

    print("IMPROVED CASES")
    print("--------------")

    if improved:
        for item in improved:
            print(
                f"ID {item['id']}: "
                f"{item['expected']} → {item['predicted']}"
            )
    else:
        print("None")

    print()

    print("REGRESSED CASES")
    print("----------------")

    if regressed:
        for item in regressed:
            print(
                f"ID {item['id']}: "
                f"{item['expected']} → {item['predicted']}"
            )
    else:
        print("None")

    print()

    if accuracy_change < -ACCURACY_THRESHOLD:
        print("STATUS: REGRESSION")
        logger.warning("Regressuon detected")
        return False
    elif accuracy_change > ACCURACY_THRESHOLD:
        print("STATUS: IMPROVEMENT")
        logger.info("model improvement detected")
        return True
    else:
        print("STATUS: NO SIGNIFICANT CHANGE")
        logger.info("No significant change detected")
        return True


if __name__ == "__main__":
    success = compare()

    if not success:
        raise SystemExit(1)