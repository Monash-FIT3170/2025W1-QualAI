import requests

def chat_with_model(token):
    url = 'http://localhost:3000/api/chat/completions'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    data = {
      "model": "deepseek-r1:1.5b",
      "messages": [
        {
          "role": "user",
          "content": "Why is the sky blue?"
        }
      ]
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()