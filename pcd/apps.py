from django.apps import AppConfig


class WebConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pcd'


# def check_object_permission(func):
#     @wraps(func)
#     def decorated(o, request):
#         user = User.objects.filter(pk=request.user.pk).last()
#         if('workstationId' in request.query_params):
#             workstation = WorkstationInfo.objects.filter(id=request.query_params['workstationId'], owner_id=request.user.id).last()
#             if (workstation == None):
#                 return IoTErrorResponse.GenParasErrorResponse(
#                     error_msg='workstationId {} is invalid'.format(request.query_params['workstationId']))
#         if(request.user.has_perm('interface.{}'.format(iWebServerBaseConfig.IWEBSERVER_PERMISSION_ADMIN_ACCESS))):
#             return func(o, request)
#         user = User.objects.filter(pk=request.user.pk).last()
#         if(user != None and user.has_perm('interface.{}'.format(iWebServerBaseConfig.IWEBSERVER_PERMISSION_ADMIN_ACCESS))):
#             return func(o, request)
#         return IoTErrorResponse.GenResponse(error_code=iWebServerBaseConfig.IWEBSERVER_ERROR_CODE_NO_ADMIN_PERMISSION, error_msg='only admin can access')
#     return decorated