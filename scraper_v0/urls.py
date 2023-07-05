from django.contrib import admin
from django.urls import path
from scraper_app import views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('run_worker/<int:worker_id>/', views.run_worker, name='run_worker'),
    path('admin/', admin.site.urls),
]
