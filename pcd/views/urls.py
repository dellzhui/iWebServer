from django.urls import include, path

urlpatterns = [
    path('v1.0/user/', include('pcd.views.user.urls')),
    path('v1.0/workstation/', include('pcd.views.workstation.urls')),
    path('v1.0/workstation/', include('pcd.views.room.urls')),
]
