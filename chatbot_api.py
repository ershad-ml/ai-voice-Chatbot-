import requests

OLLAMA_URL = "http://localhost:11434/api/chat"

conversation = [
    {
        "role": "system",
        "content": "You are a helpful, friendly AI assistant. Keep responses concise."
    }
]

def ask_chatbot(user_message):
    global conversation

    conversation.append({"role": "user", "content": user_message})

    payload = {
        "model": "gemma:2b",
        "messages": conversation,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        response.raise_for_status()

        reply = response.json()["message"]["content"]
        conversation.append({"role": "assistant", "content": reply})

        if len(conversation) > 12:
            conversation[:] = conversation[:2] + conversation[-10:]

        return reply

    except Exception:
        return "Sorry, the local AI model is not responding."
