import requests


def ask_llm(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "phi3",
            "prompt": prompt,
            "stream": False,
            "option": {
                "num_predict":150
            }
        }
    )
    return response.json()["response"]