# from django.urls import re_path
# from . import views
#
# app_name = "myaccount"
# urlpatterns = [
#     re_path(r'^profile/$', views.profile, name='profile'),
#     re_path(r'^profile/update/$', views.profile_update, name='profile_update'),
# ]
from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

app_name = 'myaccount'
urlpatterns = [
    path('profile/', login_required(views.profile), name='profile'),
    path('profile/update/', login_required(views.profile_update), name='profile_update'),
    path('profile/management/', login_required(views.management), name='management'),
    path('profile/management/user/add', login_required(views.new_user), name='new_user'),
    # url(r'^profile/management/user/(?P<pk>\d+)/delete$', login_required(views.delete_user), name='delete_user'),
    # url(r'^profile/management/user/(?P<pk>\d+)/type/set$', login_required(views.set_user_type), name='set_user_type'),
    # url(r'^profile/management/user/(?P<pk>\d+)/group/set$', login_required(views.set_user_group), name='set_user_group'),
    # path('profile/management/permissions/', login_required(views.management_groups), name='management_groups'),
    # url(r'profile/management/group/(?P<pk>\d+)/level/(?P<level>\d+)/details/$', login_required(views.group_perm_details), name='group_perm_details'),
]