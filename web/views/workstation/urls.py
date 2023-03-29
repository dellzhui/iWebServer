from django.urls import re_path
from web.views.workstation import views

urlpatterns = [
    re_path(r'^workstation$', views.iWebServerWorkstationView.as_view()),
]
