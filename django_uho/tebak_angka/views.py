from django.shortcuts import render
from .forms import PhotoUploadForm
from .models import PredictionLog, GeminiLog,UsageStats
from django.db.models import Sum
from django.db import models
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from django.db.models import F
from django.utils.timezone import now
import os
from django.middleware.csrf import get_token

api_key = os.getenv("GEMINI_API_KEY")

VALID_API_KEYS = {os.getenv("ROYAL_API_KEY")} 

RATE_LIMITS = {
    "RPM": 15,
    "TPM": 1_000_000,
    "RPD": 1_500,
}

def check_rate_limits():
    # Fetch or create today's stats
    today = now().date()
    stats, created = UsageStats.objects.get_or_create(date=today)

    # Reset stats daily
    if not created and stats.last_reset.date() != today:
        stats.requests_today = 1
        stats.tokens_today = 1
        stats.last_reset = now()
        stats.save()

    return stats


def get_csrf_token(request):
    return JsonResponse({"csrfToken": get_token(request)})


def real_ai_submit(request):
    req_royal_api_key = request.headers.get('X-API-KEY') 
    
    if req_royal_api_key not in VALID_API_KEYS:
        return JsonResponse({'error': 'Invalid API key'}, status=401) 

    if request.method == 'POST':
        data = json.loads(request.body)

        # Check rate limits
        # stats = check_rate_limits()
        # if stats.requests_today >= RATE_LIMITS['RPD']:
        #     return JsonResponse({"error": "Daily request limit exceeded"}, status=429)
        # if stats.requests_today / ((now() - stats.last_reset).seconds / 60) >= RATE_LIMITS['RPM']:
        #     return JsonResponse({"error": "Requests per minute limit exceeded"}, status=429)

        # total_tokens = data['usageMetadata']['totalTokenCount']
        # if stats.tokens_today + total_tokens > RATE_LIMITS['TPM']:
        #     return JsonResponse({"error": "Tokens per minute limit exceeded"}, status=429)

        # Prepare the request to the Gemini API
        gemini_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
        headers = {"Content-Type": "application/json"}
        gemini_payload = {"contents": [{
            "parts": [{"text": data.get("prompt")}]
        }]}
        
        # Send the request to the Gemini API
        response = requests.post(f"{gemini_url}?key={api_key}", headers=headers, json=gemini_payload)

        if response.status_code != 200:
            return JsonResponse({"error": "Failed to fetch data from Gemini API", "details": response.text}, status=response.status_code)

        # Parse Gemini API response
        gemini_response = response.json()

        # Update stats
        # stats.requests_today = F('requests_today') + 1
        # stats.tokens_today = F('tokens_today') + gemini_response['usageMetadata']['totalTokenCount']
        # stats.save()

        # Log response
        log = GeminiLog(
            response_content=gemini_response['candidates'][0]['content']['parts'][0]['text'],
            finish_reason=gemini_response['candidates'][0]['finishReason'],
            avg_logprobs=gemini_response['candidates'][0].get('avgLogprobs'),
            prompt_token_count=gemini_response['usageMetadata']['promptTokenCount'],
            candidates_token_count=gemini_response['usageMetadata']['candidatesTokenCount'],
            total_token_count=gemini_response['usageMetadata']['totalTokenCount'],
            model_version=gemini_response['modelVersion']
        )
        log.save()

        return JsonResponse({
            "response": gemini_response['candidates'][0]['content']['parts'][0]['text'],
            "model_version": gemini_response['modelVersion']
        }, status=200)

def reset_stats_daily():
    today = now().date()
    UsageStats.objects.filter(date__lt=today).update(requests_today=0, tokens_today=0)

@csrf_exempt
def mock_ai_submit(request):
    req_royal_api_key = request.headers.get('X-API-KEY') 
    
    if req_royal_api_key not in VALID_API_KEYS:
        return JsonResponse({'error': 'Invalid API key'}, status=401) 

    if request.method == 'POST':
        simulated_response = {
            "response": "hi, i just gemini mock response. no hard feeling. stay calm.",
            "model_version": "gemini-1.5-flash"
        }


        return JsonResponse(simulated_response, status=200)
        
# 2. Handler to fetch Gemini logs for the dashboard
def get_logs(request):
    if request.method == 'GET':
        logs = GeminiLog.objects.all().order_by('-timestamp')
        logs_data = [
            {
                "id": log.id,
                "response_content": log.response_content,
                "finish_reason": log.finish_reason,
                "avg_logprobs": log.avg_logprobs,
                "prompt_token_count": log.prompt_token_count,
                "candidates_token_count": log.candidates_token_count,
                "total_token_count": log.total_token_count,
                "model_version": log.model_version,
                "timestamp": log.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            } for log in logs
        ]
        return JsonResponse(logs_data, safe=False, status=200)

# 3. Handler for aggregated log statistics
def get_aggregates(request):
    if request.method == 'GET':
        total_logs = GeminiLog.objects.count()
        avg_prompt_tokens = GeminiLog.objects.all().aggregate(models.Avg('prompt_token_count'))['prompt_token_count__avg']
        avg_candidates_tokens = GeminiLog.objects.all().aggregate(models.Avg('candidates_token_count'))['candidates_token_count__avg']
        total_tokens_used = GeminiLog.objects.all().aggregate(models.Sum('total_token_count'))['total_token_count__sum']

        aggregates = {
            "total_logs": total_logs,
            "avg_prompt_tokens": round(avg_prompt_tokens, 2) if avg_prompt_tokens else 0,
            "avg_candidates_tokens": round(avg_candidates_tokens, 2) if avg_candidates_tokens else 0,
            "total_tokens_used": total_tokens_used if total_tokens_used else 0
        }
        return JsonResponse(aggregates, status=200)

# 4. Recommendation: Add a handler to limit usage
def check_usage_limit(request):
    if request.method == 'GET':
        limit = 100000  # Example token limit
        total_tokens_used = GeminiLog.objects.all().aggregate(models.Sum('total_token_count'))['total_token_count__sum']
        total_tokens_used = total_tokens_used if total_tokens_used else 0

        if total_tokens_used > limit:
            return JsonResponse({"message": "Usage limit exceeded", "tokens_used": total_tokens_used, "limit": limit}, status=403)
        else:
            return JsonResponse({"message": "Within usage limit", "tokens_used": total_tokens_used, "limit": limit}, status=200)

def cnn_prediction_log(request):
    if request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            result = 3
            confidence_score = 7.3

            # Simpan log prediksi
            log = PredictionLog.objects.create(                
                prediction=str(result[0]),
                confidence_score=confidence_score
            )

            return render(request, 'tebak_angka/result.html', {
                'result': result,
                'confidence_score': confidence_score,
                
                'price': log.price
            })
    else:
        form = PhotoUploadForm()
    
    return render(request, 'tebak_angka/form_cnn_with_log.html', {'form':form})

def prediction_log_list(request):
    # Ambil semua log prediksi
    logs = PredictionLog.objects.all().order_by('-created_at')  # Urutkan berdasarkan waktu terbaru
    total_hits = PredictionLog.objects.count()
    total_cost = PredictionLog.objects.aggregate(total_cost=Sum('price'))['total_cost']

    return render(request, 'tebak_angka/prediction_log_list.html', {
        'logs': logs,
        'total_hits': total_hits,
        'total_cost': total_cost
    })