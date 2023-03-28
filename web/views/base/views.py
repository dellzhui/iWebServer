from django.shortcuts import redirect, render


def dashboard(request):
    return redirect('forbidden')

def menu_config_list(request):
    # if (not request.user.has_perm('boards.all_access')):
    #     return redirect('forbidden')
    #
    # menu_default = menu_global_variable(request).get("menu_default")
    # # datebase get
    # menu_datebase = BaseMenuConfig.objects.all().order_by('Sequence')

    paras = {}

    # paras['menu_default'] = menu_default
    # paras['menu_datebase'] = menu_datebase
    # paras['menu_MenuUrl'] = [menu.MenuUrl for menu in menu_datebase]
    return render(request, 'dark/menu_config.html', paras)

def menu_config_actions(request):
    # if (not request.user.has_perm('boards.all_access')):
    #     return redirect('forbidden')
    # MenuName = request.POST.get('MenuName', "")
    # MenuUrl = request.POST.get('MenuUrl', "")
    # Sequence = request.POST.get('Sequence', "")
    # Level = request.POST.get('Level')
    # EnabledFlag = request.POST.get('EnabledFlag', "")
    # if(MenuName == "" or MenuUrl == "" or Sequence == "" or Level == None or EnabledFlag == ""):
    #     return HttpResponse("get menu config date error")
    #
    # MenuConfig_filter = BaseMenuConfig.objects.filter(MenuName=MenuName)
    # if not MenuConfig_filter.exists():
    #     MenuConfig_filter.create(MenuName=MenuName, MenuUrl=MenuUrl, Level=int(Level), EnabledFlag=EnabledFlag, Sequence=Sequence)
    #
    # if MenuConfig_filter.exists() and EnabledFlag != None:
    #     MenuConfig_filter.update(EnabledFlag=EnabledFlag)

    return redirect('menu_config_list')

def forbidden(request):
    return render(request, 'forbidden.html', {})
