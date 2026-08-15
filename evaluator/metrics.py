def calculate_accuracy(results):
    
    correct = sum(
        result["correct"]
        for result in results
    )
    total = len(results)

    return correct / total if total > 0 else 0.0
    