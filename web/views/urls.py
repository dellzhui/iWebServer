from django.urls import include, path

urlpatterns = [
    path('', include('web.views.base.urls')),
]
