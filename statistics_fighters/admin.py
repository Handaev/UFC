from django.contrib import admin
from .models import Fighter, WeightCategory

admin.site.register(WeightCategory)
admin.site.register(Fighter)