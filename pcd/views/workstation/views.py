from interface.utils.log_utils import loggerr
from rest_framework.generics import GenericAPIView
from pcd.config import iWebServerConfig
from interface.datatype.datatype import IoTErrorResponse, IoTSuccessResponse
from interface.utils.tools import ParasUtil
from interface.views import iwebserver_logger_c
from pcd.models import WorkstationInfo

Log = loggerr(__name__).getLogger()


class iWebServerWorkstationView(GenericAPIView):
    @iwebserver_logger_c
    def get(self, request):
        try:
            workstations = WorkstationInfo.objects.filter(owner_id=request.user.id)
            if ('workstationId' in request.query_params):
                workstations = workstations.filter(id=request.query_params['workstationId'])
            return IoTSuccessResponse().GenResponse(data=[item.to_dict() for item in workstations])
        except Exception as err:
            Log.exception('iWebServerWorkstationView get err:[' + str(err) + ']')
        return IoTErrorResponse.GenResponse()

    @iwebserver_logger_c
    def post(self, request):
        try:
            if(ParasUtil.is_missing_paras(request.data, ['workstationName'])):
                return IoTErrorResponse.GenParasErrorResponse(error_msg='missing workstationName')

            workstation = WorkstationInfo.objects.filter(name=request.data['workstationName'], owner_id=request.user.id).last()
            if(workstation != None):
                Log.error('workstation {} already presenced'.format(request.data['workstationName']))
                return IoTErrorResponse.GenResponse(error_code=iWebServerConfig.IWEBSERVER_ERROR_CODE_WORKSTATION_ALREADY_PRESENCED, error_msg='workstation {} already presenced'.format(request.data['workstationName']))

            workstation = WorkstationInfo.objects.create(name=request.data['workstationName'], owner_id=request.user.id)
            # assign_perm('pcd.{}'.format(iWebServerConfig.IWEBSERVER_PERMISSION_WORKSTATION_ACCESS), User.objects.filter(id=request.user.id).last(), workstation)
            return IoTSuccessResponse().GenResponse(data=workstation.to_dict())
        except Exception as err:
            Log.exception('iWebServerWorkstationView post err:[' + str(err) + ']')
        return IoTErrorResponse.GenResponse()

    @iwebserver_logger_c
    def put(self, request):
        try:
            if (ParasUtil.is_missing_paras(request.query_params, ['workstationId'])):
                return IoTErrorResponse.GenParasErrorResponse(error_msg='missing workstationId')
            if (ParasUtil.is_missing_paras(request.data, ['workstationName'])):
                return IoTErrorResponse.GenParasErrorResponse(error_msg='missing workstationName')

            if (request.data['workstationName'] == ''):
                Log.error('invalid workstationName')
                return IoTErrorResponse.GenResponse(error_code=iWebServerConfig.IWEBSERVER_ERROR_CODE_PASSWORD_NOT_MATCH, error_msg='invalid workstationName')

            workstation = WorkstationInfo.objects.filter(id=request.query_params['workstationId'], owner_id=request.user.id).last()
            if (workstation == None):
                Log.error('workstation {} not presenced'.format(request.query_params['workstationId']))
                return IoTErrorResponse.GenResponse(error_code=iWebServerConfig.IWEBSERVER_ERROR_CODE_WORKSTATION_NOT_PRESENCED, error_msg='workstation not presenced')

            workstation.name = request.data['workstationName']
            workstation.save()
            return IoTSuccessResponse().GenResponse(data=workstation.to_dict())
        except Exception as err:
            Log.exception('iWebServerWorkstationView put err:[' + str(err) + ']')
        return IoTErrorResponse.GenResponse()

    @iwebserver_logger_c
    def delete(self, request):
        try:
            if (ParasUtil.is_missing_paras(request.query_params, ['workstationId'])):
                return IoTErrorResponse.GenParasErrorResponse()

            workstation = WorkstationInfo.objects.filter(id=request.query_params['workstationId'], owner_id=request.user.id).last()
            if (workstation == None):
                Log.error('workstation {} not presenced'.format(request.query_params['workstationId']))
                return IoTErrorResponse.GenResponse(error_code=iWebServerConfig.IWEBSERVER_ERROR_CODE_WORKSTATION_NOT_PRESENCED, error_msg='workstation not presenced')

            workstation.do_delete()
            return IoTSuccessResponse().GenResponse()
        except Exception as err:
            Log.exception('iWebServerWorkstationView delete err:[' + str(err) + ']')
        return IoTErrorResponse.GenResponse()
