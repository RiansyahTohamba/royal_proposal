from django.shortcuts import render
from .forms import PhotoUploadForm
from .models import PredictionLog, GeminiLog
from django.db.models import Sum
from django.db import models
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def process_response(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        # Log the response to the database
        log = GeminiLog(
            response_content=data['candidates'][0]['content']['parts'][0]['text'],
            finish_reason=data['candidates'][0]['finishReason'],
            avg_logprobs=data['candidates'][0].get('avgLogprobs'),
            prompt_token_count=data['usageMetadata']['promptTokenCount'],
            candidates_token_count=data['usageMetadata']['candidatesTokenCount'],
            total_token_count=data['usageMetadata']['totalTokenCount'],
            model_version=data['modelVersion']
        )
        log.save()

        # Forward the relevant data to Flutter
        return JsonResponse({
            "response": data['candidates'][0]['content']['parts'][0]['text'],
            "model_version": data['modelVersion']
        }, status=200)
    
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