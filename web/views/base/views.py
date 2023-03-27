from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import redirect, render


def dashboard(request):
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
