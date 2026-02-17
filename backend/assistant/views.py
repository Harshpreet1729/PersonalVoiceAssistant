import json
import os

import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL = "llama3-8b-8192"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"


@csrf_exempt
def ask(request):
    if request.method != "POST":
        return JsonResponse({"reply": "Method not allowed."}, status=405)

    if not GROQ_API_KEY:
        return JsonResponse(
            {"reply": "Error: GROQ_API_KEY not set in backend/.env"}, status=500
        )

    try:
        payload = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"reply": "Invalid JSON body."}, status=400)

    user_input = payload.get("message", "")

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    body = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are Jarvis, a helpful AI assistant."},
            {"role": "user", "content": user_input},
        ],
        "temperature": 0.7,
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=body, timeout=30)
        response.raise_for_status()
        result = response.json()
        reply = result["choices"][0]["message"]["content"]
        return JsonResponse({"reply": reply})
    except requests.RequestException as exc:
        return JsonResponse({"reply": f"Error: {str(exc)}"}, status=502)
    except (KeyError, IndexError, TypeError) as exc:
        return JsonResponse({"reply": f"Unexpected API response: {str(exc)}"}, status=502)
