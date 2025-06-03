
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from users.views import home_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')), 
     path('basket/', include('basket.urls')), # подключаем маршруты users
     path('orders/', include('orders.urls')),
    path('', home_view, name='home'),
    path('fighters/', include('statistics_fighters.urls', namespace='statistics_fighters')),
    path('catalog/', include('catalog_product.urls', namespace='catalog')),
    path('password-change/', 
         auth_views.PasswordChangeView.as_view(template_name='users/password_change.html'), 
         name='password_change'),
    path('password-change/done/', 
         auth_views.PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'), 
         name='password_change_done'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
