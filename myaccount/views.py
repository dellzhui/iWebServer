from interface.utils.log_utils import loggerr
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .models import UserProfile
from .forms import ProfileForm
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

Log = loggerr(__name__).getLogger()


def profile(request):
    user = request.user
    return render(request, 'account/profile.html', {'user': user})


def profile_update(request):
    user = request.user
    user_profile = get_object_or_404(UserProfile, user=user)

    if request.method == "POST":
        form = ProfileForm(request.POST)

        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()

            user_profile.org = form.cleaned_data['org']
            user_profile.telephone = form.cleaned_data['telephone']
            user_profile.save()

            return HttpResponseRedirect(reverse('myaccount:profile'))
    else:
        default_data = {'first_name': user.first_name, 'last_name': user.last_name,
                        'org': user_profile.org, 'telephone': user_profile.telephone, }
        form = ProfileForm(default_data)

    return render(request, 'account/profile_update.html', {'form': form, 'user': user})

def management(request):
    if (not (request.user.has_perm('boards.all_access'))):
        return redirect('forbidden')
    users = User.objects.filter(is_superuser=False).exclude(username='AnonymousUser').order_by('-id')
    users_admin = []
    users_general = []
    users_guest = []

    for user in users:
        if (user.has_perm('boards.all_access')):
            user.UserType = 'Admin'
            users_admin.append(user)
        elif(user.has_perm('boards.regular_access')):
            user.UserType = 'Regular'
            users_general.append(user)
        else:
            user.UserType = 'Guest'
            users_guest.append(user)

    paginator = Paginator(users_admin + users_general + users_guest, 10)
    page = request.GET.get('page', 1)
    target_users = paginator.get_page(page)

    paras = {}
    paras['users'] = target_users
    # paras['groups'] = Group.objects.filter(name__in=[item.AreaName for item in UserControl.objects.filter(AreaName__isnull=False)])
    return render(request, 'management_userlist.html', paras)

def new_user(request):
    if (not (request.user.has_perm('boards.all_access'))):
        return redirect('forbidden')
    if (request.method == 'POST'):
        Log.d(request.POST)
        try:
            UserName = request.POST.get('UserName')
            Password = request.POST.get('Password')
            Email = request.POST.get('Email')
            if(UserName != None and UserName != '' and Password != None and Password != ''):
                User.objects.create_user(username=UserName, password=Password, email=Email)
                return redirect('myaccount:management')
        except Exception as err:
            Log.e('new_user err:[' + str(err) + ']')
    return HttpResponse('404 Error')

def delete_user(request, pk):
    if (not (request.user.has_perm('boards.all_access'))):
        return redirect('forbidden')
    user = get_object_or_404(User, pk=pk)
    if (user.is_superuser or user.has_perm('boards.all_access')):
        return HttpResponse('404 Error')
    groups = Group.objects.filter(name='RegularGroup')
    if (len(groups) == 1):
        group = groups[0]
        group.user_set.remove(user)
    user.delete()
    return redirect('myaccount:management')

def set_user_type(request, pk):
    if (not (request.user.has_perm('boards.all_access'))):
        return redirect('forbidden')
    if(request.method != 'POST'):
        return redirect('forbidden')
    user = get_object_or_404(User, pk=pk)
    if(user.is_superuser or user.has_perm('boards.all_access')):
        return HttpResponse('404 Error')

    UserType = request.POST.get('UserType')
    if(UserType == None):
        Log.d('UserType error')
        return HttpResponse('404 Error')

    if(UserType == 'Regular' and not user.has_perm('boards.regular_access')):
        groups = Group.objects.filter(name='RegularGroup')
        if(len(groups) == 1):
            group = groups[0]
            group.user_set.add(user)
            return redirect('myaccount:management')
    elif(UserType == 'Guest' and user.has_perm('boards.regular_access')):
        groups = Group.objects.filter(name='RegularGroup')
        if (len(groups) == 1):
            group = groups[0]
            group.user_set.remove(user)
            return redirect('myaccount:management')
    return HttpResponse('404 Error')

# def set_user_group(request, pk):
#     if (not (request.user.has_perm('boards.all_access'))):
#         return redirect('forbidden')
#     if(request.method != 'POST'):
#         return redirect('forbidden')
#     user = get_object_or_404(User, pk=pk)
#     if(user.is_superuser or user.has_perm('boards.all_access')):
#         return HttpResponse('404 Error')
#
#     GroupName = request.POST.get('GroupName')
#     if(GroupName == None):
#         Log.d('GroupName error')
#         return HttpResponse('404 Error')
#
#     groups = Group.objects.filter(name=GroupName)
#     if (groups.count() == 1):
#         group = groups[0]
#         user.groups.clear()
#         user.groups.add(group)
#         Log.d('set user {} group to {} succeed'.format(user.username, group.name))
#         return redirect('myaccount:management')
#
#     return HttpResagement_groups(request):
#     if (not (request.user.has_perm('boards.all_access'))):
#         return redirect('forbidden')
#     user_controls = UserControl.objects.filter().order_by('Level', '-id')
#     page = request.GET.get('page', 1)
#     target_user_controls = Paginator(user_controls, 10).get_page(page)
#     user_control_province = UserControl.objects.filter(Level=1).last()
#
#     paras = {}
#     paras['user_controls'] = target_user_controls
#     paras['user_control_province'] = user_control_province
#     return render(ponse('404 Error')

# def manrequest, 'management_grouplist.html', paras)

# def group_perm_details(request, pk, level):
#     if (not (request.user.has_perm('boards.all_access'))):
#         return redirect('forbidden')
#     util = UserControlUtils()
#     user_control = UserControl.objects.filter(pk=pk).last()
#     Level = int(level)
#     user_control_province = UserControl.objects.filter(Level=1).last()
#
#     if (request.method == 'POST'):
#         Name = CommonTools.GetPara(request, 'Name', user_control)
#         b_need_update = False
#
#         if(user_control == None and ((Name != None and Name != '') or (user_control_province != None and Level == 1))):
#             if(UserControl.objects.filter(Name=Name).last() != None):
#                 return redirect('myaccount:group_perm_details', pk, level)
#
#         user_control = UserControl() if (user_control == None) else user_control
#         if(Name != None and Name != ''):
#             b_need_update = True if(user_control.Name != Name) else b_need_update
#             user_control.Name = Name
#             user_control.Desc = user_control.Name
#             user_control.AreaName = user_control.Name
#         else:
#             Log.e('Name is None')
#             return redirect('myaccount:group_perm_details', pk, level)
#         user_control.Level = Level
#         b_need_update = True if (user_control.Level != Level) else b_need_update
#         user_control.super_control = user_control_province if (Level > 1) else user_control.super_control
#         if(b_need_update):
#             user_control.save()
#             if(user_control.is_vaild() and user_control.super_control != None and user_control.super_control.is_vaild() and user_control.Level == 2):
#                 if(AreaInfo.objects.filter(ProvinceName=user_control.super_control.AreaName, CityName=user_control.AreaName).count() == 0):
#                     Log.d('we will create city {}'.format(user_control.AreaName))
#                     AreaInfo.objects.create(ProvinceName=user_control.super_control.AreaName, CityName=user_control.AreaName)
#
#         permission_list = []
#         if (request.POST.get('PermissionName') != None):
#             permission_list = request.POST.getlist('PermissionName')
#             Log.d('get permission list from request is ' + str(permission_list))
#         else:
#             Log.d('WARNING:PermissionName not set')
#
#         group = Group.objects.filter(name=user_control.Name).last()
#         group = group if(group != None) else Group.objects.create(name=user_control.Name)
#         util.InitPermissionObject()
#         Log.d('permission_list is' + str(permission_list))
#         for perm in permission_list:
#             Log.d('we will add {} for group {}'.format(perm, group.name))
#             util.AssignPermissionToObject(perm, user_control.AreaName)
#         for perm in util.GetPermissions(Level):
#             if(util.CheckPermissionToObject(perm, user_control.AreaName) and perm not in permission_list):
#                 Log.d('we will remove {} for group {}'.format(perm, group.name))
#                 remove_perm(perm, group, user_control)
#         save_access_log(request, 'New Group : {}'.format(Name))
#         return redirect('myaccount:management_groups')
#
#     permissions_selected = []
#     if(user_control == None):
#         permissions_selected = util.GetPermissions(Level)
#     else:
#         group = Group.objects.filter(name=user_control.Name).last()
#         if(group != None):
#             permissions_selected = util.GetObjectPermissions(user_control.AreaName)
#             permissions_selected = permissions_selected if(permissions_selected != None) else []
#     paras = {}
#     paras['user_control'] = user_control
#     paras['Level'] = Level
#     paras['permissions'] = UserControlUtils().GetPermissions(Level)
#     paras['permissions_selected'] = permissions_selected
#     return render(request, 'management_group_details.html', paras)
