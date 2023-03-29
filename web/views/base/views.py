import json
import logging
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from rest_framework_simplejwt.tokens import RefreshToken

from interface.utils.UserControlUtils import UserUtils
from web.datatype.base import IoTErrorResponse, AuthResponseInfo, IoTSuccessResponse

Log = logging.getLogger(__name__)


def dashboard(request):
    return redirect('forbidden')

@require_POST
def access_token(request):
    try:
        request_data = json.loads(request.body.decode('utf-8'))
        username = request_data['username']
        password = request_data['password']

        user_util = UserUtils(username, password)
        if(user_util.auto_login(request)):
            refresh = RefreshToken.for_user(user_util.get_user())
            return AuthResponseInfo(access=str(refresh.access_token), refresh=str(refresh)).GenResponse()
    except Exception as err:
        Log.exception('access_token post err:[' + str(err) + ']')
    return IoTErrorResponse.GenResponse(error_msg='internal error')

@require_POST
def refresh_token(request):
    try:
        request_data = json.loads(request.body.decode('utf-8'))
        Log.info('got request info is {}'.format(request_data))
        return IoTSuccessResponse().GenResponse(data={'access': str(RefreshToken(token=request_data['refresh']).access_token)})
    except Exception as err:
        Log.exception('refresh_token post err:[' + str(err) + ']')
        return IoTErrorResponse.GenResponse(error_msg='internal error')

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
