from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^room$', views.iWebServerRoomView.as_view()),
]
