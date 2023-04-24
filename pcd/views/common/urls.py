from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^auth/token/refresh$', views.refresh_token, name='refresh_token'),
    re_path(r'^auth/token/ice$', views.get_ice_info, name='get_ice_info'),
]
