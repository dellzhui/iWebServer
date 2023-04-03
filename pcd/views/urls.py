from django.urls import include, path

urlpatterns = [
    path('v1.0/user/', include('pcd.views.user.urls')),
    path('v1.0/workstation/', include('pcd.views.workstation.urls')),
    path('v1.0/workstation/', include('pcd.views.room.urls')),
    path('v1.0/workstation/room/', include('pcd.views.device.urls')),
    path('v1.0/notify/', include('pcd.views.notify.urls'))
]
