from django.urls import path
from . import views

urlpatterns = [
    path('api/real-ai-submit', views.real_ai_submit, name='real AI submit'),
    path('token-csrf', views.get_csrf_token, name='token csrf'),
    
    path('api/mock-ai-submit', views.mock_ai_submit, name='mock AI submit'),
    path('html/mockgemini', views.html_mock_gemini, name='HTML mock AI submit'),
    path('html/realgemini', views.html_real_gemini, name='HTML REAL AI submit'),
    
    path('ai-log', views.get_logs, name='log of ai usage'),
    path('usage-summary', views.get_aggregates, name='aggregate log'),
    path('usage-limit', views.check_usage_limit, name='AI limit'),
    
    path('cnn_with_log', views.cnn_prediction_log, name='cnn_prediction'),
    path('prediction_log_list', views.prediction_log_list, name='prediction_log_list'),
]