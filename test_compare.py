from evaluator.compare import (
    calculate_accuracy,
    calculate_average_latency,
)
def test_calculate_accuracy_latency():
    results = [
        {"correct": True},
        {"correct": False},
        {"correct": True},
        {"correct": True},
    ]
    accuracy = calculate_accuracy(results)
    assert accuracy == 0.75

def test_calculate_accuracy_empty():
    assert calculate_accuracy([]) == 0

def test_average_latency():
    results = [
        {"latency_seconds": 0.5},
        {"latency_seconds": 1.0},
        {"latency_seconds": 1.5},
    ]
    latency = calculate_average_latency(results)
    assert latency == 1.0

def test_average_latency_empty():
    assert calculate_average_latency([]) == 0

def test_improvement():
    v1_accuracy = 0.64
    v2_accuracy = 0.80

    accuracy_change = v2_accuracy - v1_accuracy
    assert accuracy_change > 0

def test_regression():
    v1_accuracy = 0.80
    v2_accuracy = 0.64

    accuracy_change = v2_accuracy - v1_accuracy
    assert accuracy_change < -0.05