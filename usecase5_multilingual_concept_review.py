import json
import os
from dotenv import load_dotenv
from openai import OpenAI

# -------------------------------------------------
# Base directory (folder where this script exists)
# -------------------------------------------------
base_dir = os.path.dirname(os.path.abspath(__file__))

# -------------------------------------------------
# Load API key from .env
# -------------------------------------------------
env_path = os.path.join(base_dir, ".env")
load_dotenv(env_path)

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY not found in .env")

client = OpenAI(api_key=api_key)

# -------------------------------------------------
# Read text file
# -------------------------------------------------
def read_text_file(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

# -------------------------------------------------
# Load multilingual inputs
# -------------------------------------------------
def load_multilingual_inputs(folder_path: str) -> dict:

    files = {
        "French proposal": "french_proposal.txt",
        "German interpretation": "german_interpretation.txt",
        "Italian concern": "italian_concern.txt",
        "Spanish amendment": "spanish_amendment.txt"
    }

    texts = {}

    for label, filename in files.items():

        file_path = os.path.join(folder_path, filename)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Missing file: {file_path}")

        texts[label] = read_text_file(file_path)

    return texts

# -------------------------------------------------
# AI analysis
# -------------------------------------------------
def analyze_multilingual_concepts(texts: dict) -> str:

    prompt = f"""
You are a multilingual concept review analyst.

Below are four texts representing perspectives from different stakeholders.

Please analyze them and explain clearly:

1. What common concepts appear across the texts
2. What differences in concern or emphasis appear
3. What shared Meta Concept could align these perspectives
4. What governance implications emerge

Texts:
{json.dumps(texts, indent=2, ensure_ascii=False)}
"""

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {
                "role": "system",
                "content": "You analyze multilingual governance texts by extracting shared concepts and differences."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content

# -------------------------------------------------
# Main
# -------------------------------------------------
def main():

    multilingual_dir = os.path.join(base_dir, "multilingual_inputs")

    if not os.path.exists(multilingual_dir):
        raise FileNotFoundError(f"Folder not found: {multilingual_dir}")

    texts = load_multilingual_inputs(multilingual_dir)

    print("Loaded multilingual inputs:")
    print(json.dumps(texts, indent=2, ensure_ascii=False))
    print()

    analysis = analyze_multilingual_concepts(texts)

    print("Multilingual Concept Review:")
    print(analysis)
    print()

# -------------------------------------------------
# Run
# -------------------------------------------------
if __name__ == "__main__":
    main()
