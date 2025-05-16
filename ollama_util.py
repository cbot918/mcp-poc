import requests

def ask_ollama(prompt: str) -> str:
    res = requests.post(
        "http://localhost:11434/api/chat",
        json = {
            "model": "gemma3:12b",  # 或你自己有的模型
            "messages": [{"role": "user", "content": prompt}],
            "stream": False
        },
    )
    data = res.json()
    return data["message"]["content"]
