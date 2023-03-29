from django.urls import include, path

urlpatterns = [
    path('v1.0/user/', include('web.views.user.urls')),
    # path('api/v1.0/workstation/', include('web.views.workstation.urls')),
]
