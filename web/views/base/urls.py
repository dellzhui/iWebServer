from django.contrib.auth.decorators import login_required
from django.urls import path
from web.views.base import views

urlpatterns = [
    path('', login_required(views.dashboard), name='dashboard'),
    path('menu_config_list/', login_required(views.menu_config_list), name='menu_config_list'),
    path('menu_config_actions/', login_required(views.menu_config_actions), name='menu_config_actions'),
    path('forbidden/', login_required(views.forbidden), name='forbidden'),
]
