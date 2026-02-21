import json
import os
from urllib import error, request as urlrequest

from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

def home(request):
    return render(request, "home.html")


def terms_view(request):
    return render(request, "legal/terms.html")


def data_policy_view(request):
    return render(request, "legal/data-policy.html")


def cookie_policy_view(request):
    return render(request, "legal/cookie-policy.html")


@login_required
def chat_view(request):
    return render(request, "chat.html")


@login_required
@require_POST
def chat_send_view(request):
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"error": "Invalid JSON payload."}, status=400)

    user_message = (payload.get("message") or "").strip()
    if not user_message:
        return JsonResponse({"error": "Message cannot be empty."}, status=400)

    openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
    if not openrouter_api_key:
        return JsonResponse({"error": "OPENROUTER_API_KEY is not set."}, status=500)

    configured_model = os.getenv(
        "OPENROUTER_MODEL", "meta-llama/llama-3.2-3b-instruct:free"
    )
    fallback_models_env = os.getenv("OPENROUTER_FALLBACK_MODELS", "")
    fallback_models = [
        model.strip() for model in fallback_models_env.split(",") if model.strip()
    ]
    model_candidates = [
        configured_model,
        *fallback_models,
        "openrouter/auto",
    ]

    def call_openrouter(model_name: str):
        openrouter_payload = {
            "model": model_name,
            "messages": [
                {"role": "system", "content": "You are Vaani, a concise helpful assistant."},
                {"role": "user", "content": user_message},
            ],
            "temperature": 0.7,
        }

        req = urlrequest.Request(
            "https://openrouter.ai/api/v1/chat/completions",
            data=json.dumps(openrouter_payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {openrouter_api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        with urlrequest.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))

    tried_models = []
    openrouter_response = None
    last_http_error = None
    last_details = ""

    for model_name in model_candidates:
        if model_name in tried_models:
            continue
        tried_models.append(model_name)
        try:
            openrouter_response = call_openrouter(model_name)
            break
        except error.HTTPError as exc:
            last_http_error = exc
            last_details = exc.read().decode("utf-8", errors="replace")
            if exc.code == 429:
                continue
            return JsonResponse(
                {"error": f"OpenRouter API error ({exc.code}).", "details": last_details},
                status=502,
            )
        except (error.URLError, TimeoutError):
            return JsonResponse({"error": "Could not reach OpenRouter API."}, status=502)

    if openrouter_response is None and last_http_error is not None:
        return JsonResponse(
            {
                "error": f"OpenRouter API error ({last_http_error.code}).",
                "details": f"{last_details} | models_tried={tried_models}",
            },
            status=502,
        )

    choices = openrouter_response.get("choices") or []
    if not choices:
        return JsonResponse({"error": "No response returned by OpenRouter."}, status=502)

    assistant_text = choices[0].get("message", {}).get("content", "").strip()
    if not assistant_text:
        return JsonResponse({"error": "OpenRouter returned empty content."}, status=502)

    return JsonResponse({"reply": assistant_text})

