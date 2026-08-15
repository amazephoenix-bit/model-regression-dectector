import json
import os
import statistics

from app.logger import get_logger


logger = get_logger(__name__)

V1_PATH = "reports/evaluation_v1.json"
V2_PATH = "reports/evaluation_v2.json"

ACCURACY_THRESHOLD = 0.05


def load_report(path):
    """Load an evaluation report from a JSON file."""
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def calculate_accuracy(results):
    """Calculate overall accuracy."""
    correct = sum(
        1 for item in results
        if item["correct"]
    )

    total = len(results)

    return correct / total if total else 0


def calculate_average_latency(results):
    """Calculate average inference latency."""
    latencies = [
        item["latency_seconds"]
        for item in results
        if "latency_seconds" in item
    ]

    return statistics.mean(latencies) if latencies else 0


def calculate_category_metrics(results):
    """Calculate accuracy for each expected category."""
    categories = {}

    for item in results:
        category = item["expected"]

        if category not in categories:
            categories[category] = {
                "correct": 0,
                "total": 0
            }

        categories[category]["total"] += 1

        if item["correct"]:
            categories[category]["correct"] += 1

    for category, data in categories.items():
        data["accuracy"] = (
            data["correct"] / data["total"]
            if data["total"]
            else 0
        )

    return categories


def write_github_summary(
    v1_accuracy,
    v2_accuracy,
    accuracy_change,
    v1_latency,
    v2_latency,
    improved,
    regressed,
    categories
):
    """Write evaluation results to the GitHub Actions job summary."""

    summary_file = os.getenv("GITHUB_STEP_SUMMARY")

    # Running locally, so there is no GitHub summary file.
    if not summary_file:
        return

    with open(summary_file, "a", encoding="utf-8") as file:

        file.write("# LLM Regression Report\n\n")

        file.write("| Metric | V1 | V2 | Change |\n")
        file.write("|---|---:|---:|---:|\n")

        file.write(
            f"| Accuracy | "
            f"{v1_accuracy:.2%} | "
            f"{v2_accuracy:.2%} | "
            f"{accuracy_change:+.2%} |\n"
        )

        file.write(
            f"| Avg Latency | "
            f"{v1_latency:.3f}s | "
            f"{v2_latency:.3f}s | "
            f"{v2_latency - v1_latency:+.3f}s |\n"
        )

        file.write("\n## Category Performance\n\n")

        file.write(
            "| Category | Correct | Total | Accuracy |\n"
        )

        file.write(
            "|---|---:|---:|---:|\n"
        )

        for category, data in categories.items():
            file.write(
                f"| {category} | "
                f"{data['correct']} | "
                f"{data['total']} | "
                f"{data['accuracy']:.2%} |\n"
            )

        file.write("\n## Case Changes\n\n")

        file.write(
            f"- Improved cases: **{len(improved)}**\n"
        )

        file.write(
            f"- Regressed cases: **{len(regressed)}**\n"
        )


def compare():
    """Compare V1 and V2 evaluation reports."""

    logger.info("Starting regression comparison")

    # --------------------------------------------------
    # Load reports
    # --------------------------------------------------

    v1 = load_report(V1_PATH)
    v2 = load_report(V2_PATH)

    logger.info(
        "Loaded evaluation reports: V1=%d cases, V2=%d cases",
        len(v1),
        len(v2)
    )

    # --------------------------------------------------
    # Calculate overall metrics
    # --------------------------------------------------

    v1_accuracy = calculate_accuracy(v1)
    v2_accuracy = calculate_accuracy(v2)

    v1_latency = calculate_average_latency(v1)
    v2_latency = calculate_average_latency(v2)

    accuracy_change = v2_accuracy - v1_accuracy
    latency_change = v2_latency - v1_latency

    logger.info(
        "Accuracy: V1=%.2f%% | V2=%.2f%% | Change=%+.2f%%",
        v1_accuracy * 100,
        v2_accuracy * 100,
        accuracy_change * 100
    )

    logger.info(
        "Latency: V1=%.3fs | V2=%.3fs | Change=%+.3fs",
        v1_latency,
        v2_latency,
        latency_change
    )

    # --------------------------------------------------
    # Category metrics
    # --------------------------------------------------

    v2_categories = calculate_category_metrics(v2)

    # --------------------------------------------------
    # Detect improved and regressed cases
    # --------------------------------------------------

    improved = []
    regressed = []

    for old, new in zip(v1, v2):

        if not old["correct"] and new["correct"]:
            improved.append(new)

        elif old["correct"] and not new["correct"]:
            regressed.append(new)

    logger.info(
        "Case changes: improved=%d | regressed=%d",
        len(improved),
        len(regressed)
    )

    # --------------------------------------------------
    # Console output
    # --------------------------------------------------

    print("================================")
    print("       MODEL REGRESSION TEST")
    print("================================")

    print()

    print(f"V1 Accuracy: {v1_accuracy:.2%}")
    print(f"V2 Accuracy: {v2_accuracy:.2%}")
    print(f"Accuracy Change: {accuracy_change:+.2%}")

    print()

    print(f"V1 Avg Latency: {v1_latency:.3f}s")
    print(f"V2 Avg Latency: {v2_latency:.3f}s")
    print(f"Latency Change: {latency_change:+.3f}s")

    # --------------------------------------------------
    # Category performance
    # --------------------------------------------------

    print()

    print("CATEGORY PERFORMANCE")
    print("--------------------")

    for category, data in v2_categories.items():
        print(
            f"{category}: "
            f"{data['correct']}/{data['total']} "
            f"({data['accuracy']:.2%})"
        )

    # --------------------------------------------------
    # Improved cases
    # --------------------------------------------------

    print()

    print("IMPROVED CASES")
    print("--------------")

    if improved:

        for item in improved:
            print(
                f"ID {item['id']}: "
                f"{item['expected']} → "
                f"{item['predicted']}"
            )

    else:
        print("None")

    # --------------------------------------------------
    # Regressed cases
    # --------------------------------------------------

    print()

    print("REGRESSED CASES")
    print("----------------")

    if regressed:

        for item in regressed:
            print(
                f"ID {item['id']}: "
                f"{item['expected']} → "
                f"{item['predicted']}"
            )

    else:
        print("None")

    # --------------------------------------------------
    # GitHub Actions summary
    # --------------------------------------------------

    write_github_summary(
        v1_accuracy=v1_accuracy,
        v2_accuracy=v2_accuracy,
        accuracy_change=accuracy_change,
        v1_latency=v1_latency,
        v2_latency=v2_latency,
        improved=improved,
        regressed=regressed,
        categories=v2_categories
    )

    # --------------------------------------------------
    # Regression decision
    # --------------------------------------------------

    if accuracy_change < -ACCURACY_THRESHOLD:

        print("STATUS: REGRESSION")

        logger.warning(
            "Regression detected: accuracy change=%+.2f%%",
            accuracy_change * 100
        )

        return False

    elif accuracy_change > ACCURACY_THRESHOLD:

        print("STATUS: IMPROVEMENT")

        logger.info(
            "Model improvement detected: accuracy change=%+.2f%%",
            accuracy_change * 100
        )

        return True

    else:

        print("STATUS: NO SIGNIFICANT CHANGE")

        logger.info(
            "No significant accuracy change detected: %+.2f%%",
            accuracy_change * 100
        )

        return True


if __name__ == "__main__":

    success = compare()

    if not success:
        raise SystemExit(1)