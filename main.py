from app.llm import classify_email
result = classify_email(
    email="Hi, I paid yesterday but my payment failed and i was charged twice.",
    prompt_file="app/prompts/classifier_v1.yaml"
)
print(result)