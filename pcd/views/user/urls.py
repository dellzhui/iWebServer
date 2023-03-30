from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^user$', views.iWebServerUserView.as_view()),
]
