# LLM Model Regression Detector

A local LLM evaluation and regression-testing framework that automatically detects whether a new prompt version or model upgrade improves or degrades performance — before it ships.

Built around **Llama 3.2** running locally through **Ollama**, evaluated against a golden dataset for a customer-support email classification task. CI-gated: if a change regresses accuracy beyond a configurable threshold, the pipeline fails automatically.

---

## Why this exists

Prompt tweaks and model version bumps are easy to make and hard to trust. Without a regression harness, teams either eyeball a handful of outputs or ship blind. This project runs a full before/after comparison on every change, scores it against a golden dataset, and blocks the merge if quality drops — the same discipline unit tests bring to code, applied to LLM behavior.

---

## Features

- 🖥️ **Local inference** via Ollama — no API costs, no external calls
- 📐 **Structured JSON output** validated with Pydantic
- 📊 **Golden evaluation dataset** for consistent, repeatable scoring
- 📈 **Accuracy, latency, and category-level metrics**
- 🔁 **V1 vs V2 comparison** with per-case regression detection
- ⚙️ **Configurable regression threshold**
- ✅ **Python unit tests** for the evaluation pipeline itself
- 📝 **Centralized logging** for every run
- 🤖 **GitHub Actions CI** — auto-fails the build on detected regression
- 🦭 **Podman support** for reproducible, rootless containerized runs

---

## Architecture

```
Golden Dataset
      │
      ▼
   Llama 3.2 (via Ollama)
      │
      ▼
   Evaluator
      │
      ├──► Accuracy
      ├──► Latency
      └──► Category Metrics
      │
      ▼
  V1 / V2 Reports
      │
      ▼
Regression Detector
      │
      ├──► Improved Cases
      └──► Regressed Cases
      │
      ▼
  GitHub Actions
      │
      ├──► ✅ PASS
      └──► ❌ FAIL
```

---

## Quick Start

### Prerequisites
- Python 3.10+
- [Ollama](https://ollama.com) installed and running locally
- [Podman](https://podman.io) (optional, for containerized runs)

### Setup

```bash
git clone https://github.com/amazephoenix-bit/model-regression-detector.git
cd model-regression-detector

pip install -r requirements.txt

# Pull the model used for evaluation
ollama pull llama3.2
```

### Run an evaluation

```bash
python main.py
```

### Run tests

```bash
pytest test_runner.py test_compare.py test_llm.py
```

### Run in a container

```bash
podman build -t model-regression-detector .
podman run --rm model-regression-detector
```

---

## Sample Output

```
Comparing V1 vs V2 on golden dataset (n=120)

Accuracy:   V1: 91.7%   →   V2: 88.3%   (-3.4%)
Latency:    V1: 412ms   →   V2: 398ms   (-14ms)

Category breakdown:
  billing        94% → 90%  ⚠ regressed
  shipping       89% → 91%  ✅ improved
  account        93% → 84%  ⚠ regressed

Regression threshold: 2.0%
Result: ❌ FAIL — 2 categories exceeded regression threshold
```

*(Sample for illustration — replace with a real run's output.)*

---

## Project Structure

```
.
├── app/            # Core application logic
├── dataset/         # Golden evaluation dataset
├── evaluator/        # Scoring, metrics, comparison logic
├── logs/            # Run logs
├── reports/          # Generated V1/V2 comparison reports
├── test_runner.py    # Evaluation run tests
├── test_compare.py   # Regression comparison tests
├── test_llm.py       # LLM interface tests
├── Dockerfile
└── main.py           # Entry point
```

---

## Configuration

The regression threshold and dataset paths can be adjusted in the evaluator config — update this section with the actual file/flag once finalized (e.g. `evaluator/config.py` or CLI flags on `main.py`).

---

## Roadmap / Ideas

- [ ] Support additional local models beyond Llama 3.2
- [ ] Publish HTML report artifacts from CI runs
- [ ] Slack/GitHub PR comment integration for regression summaries

---

## License

Add a license (MIT is a common default for portfolio projects) — currently unlicensed.
