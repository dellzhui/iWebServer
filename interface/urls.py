from django.contrib.auth.decorators import login_required
from django.urls import path
from interface import views

urlpatterns = [
    path('', login_required(views.dashboard), name='dashboard'),
    path('forbidden', login_required(views.forbidden), name='forbidden'),
]
