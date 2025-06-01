# statistics_fighters/views.py
from django.shortcuts import render, get_object_or_404
from .models import WeightCategory, Fighter

def fighter_ranking_view(request):
    categories = WeightCategory.objects.prefetch_related('fighters').all()
    return render(request, 'statistics_fighters/fighter_ranking.html', {'categories': categories})

def fighter_detail_view(request, fighter_id):
    fighter = get_object_or_404(Fighter, id=fighter_id)
    context = {'fighter': fighter}
    return render(request, 'statistics_fighters/fighter_detail.html', context)