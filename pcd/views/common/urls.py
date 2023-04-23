from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^auth/token/refresh$', views.refresh_token, name='refresh_token'),
]
