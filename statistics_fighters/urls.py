from django.urls import path
from . import views

app_name = 'statistics_fighters'

urlpatterns = [
    path('ranking/', views.fighter_ranking_view, name='fighter_ranking'),
    path('fighter/<int:fighter_id>/', views.fighter_detail_view, name='fighter_detail'),
]
