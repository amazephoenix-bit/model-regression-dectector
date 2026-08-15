import json
import os
import yaml
from ollama import Client

from app.config import MODEL, HOST
from app.schemas import SupportResponse

client=Client(host=HOST)

def load_prompt(prompt_file: str) -> str:
    with open(prompt_file, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)
    return data["system_prompt"]

def classify_email(email: str,prompt_file: str) -> SupportResponse:
    system_prompt = load_prompt(prompt_file)
    response = client.chat(
        model=MODEL,
        format="json",
        options={"temperature": 0.0},
        messages=[
            {"role": "system",
              "content": system_prompt},
            {"role": "user",
              "content": email}
        ],
        
    )
    output = json.loads(response["message"]["content"])
    output["category"] = output["category"].strip().title()
    return SupportResponse(**output)