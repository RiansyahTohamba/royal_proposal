from django.db import models
from django.utils.timezone import now

class GeminiLog(models.Model):
    response_content = models.TextField()
    finish_reason = models.CharField(max_length=20)
    avg_logprobs = models.FloatField(null=True, blank=True)
    prompt_token_count = models.IntegerField()
    candidates_token_count = models.IntegerField()
    total_token_count = models.IntegerField()
    model_version = models.CharField(max_length=50)
    timestamp = models.DateTimeField(default=now)

class UsageStats(models.Model):
    date = models.DateField(default=now)
    requests_today = models.IntegerField(default=0)
    tokens_today = models.IntegerField(default=0)
    last_reset = models.DateTimeField(default=now)

class UploadedPhoto(models.Model):
    photo = models.ImageField(upload_to='uploaded_photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class PredictionLog(models.Model):
    photo = models.ForeignKey(UploadedPhoto, on_delete=models.CASCADE, related_name='logs')
    prediction = models.CharField(max_length=255)
    confidence_score = models.FloatField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=4000)
    created_at = models.DateTimeField(auto_now_add=True)

class Customer(models.Model):
    name = models.CharField(max_length=255)    
    