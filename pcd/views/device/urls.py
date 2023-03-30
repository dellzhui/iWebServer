from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^device$', views.iWebServerDeviceView.as_view()),
]
