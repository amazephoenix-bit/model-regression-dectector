from evaluator.runner import load_dataset

def test_load_dataset():
    dataset = load_dataset("dataset/golden_dataset.json")
    assert isinstance(dataset, list)
    assert len(dataset) == 25

def test_dataset_structure():
    dataset = load_dataset("dataset/golden_dataset.json")
    for item in dataset:
        assert "id" in item
        assert "email" in item
        assert "expected_category" in item