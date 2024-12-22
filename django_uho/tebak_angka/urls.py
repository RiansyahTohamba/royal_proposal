from django.urls import path
from . import views

urlpatterns = [
    path('gemini_log', views.get_logs, name='log gemini'),
    path('cnn_with_log', views.cnn_prediction_log, name='cnn_prediction'),
    path('prediction_log_list', views.prediction_log_list, name='prediction_log_list'),
]