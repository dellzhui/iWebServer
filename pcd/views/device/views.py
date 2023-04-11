from interface.utils.log_utils import loggerr
from rest_framework.generics import GenericAPIView
from pcd.config import iWebServerConfig
from interface.datatype.datatype import IoTErrorResponse, IoTSuccessResponse
from interface.utils.tools import ParasUtil, CommonTools
from interface.views import iwebserver_logger_c
from pcd.models import DeviceInfo, DEVICE_TYPE_CHOICES, WorkstationInfo, RoomInfo
from pcd.utils.device_utils import DeviceHTTPRequestUtil

Log = loggerr(__name__).getLogger()


class iWebServerDeviceView(GenericAPIView):
    @iwebserver_logger_c
    def get(self, request):
        try:
            devices = DeviceInfo.objects.filter(owner_id=request.user.id)
            if('workstationId' in request.query_params):
                devices = devices.filter(workstation_id=request.query_params['workstationId'])
            if ('roomId' in request.query_params):
                devices = devices.filter(room__roomId=request.query_params['roomId'])
            if ('deviceId' in request.query_params):
                devices = devices.filter(id=request.query_params['deviceId'])
            if ('deviceType' in request.query_params):
                devices = devices.filter(deviceType=request.query_params['deviceType'])

            return IoTSuccessResponse().GenResponse(data=[item.to_dict() for item in devices])
        except Exception as err:
            Log.exception('iWebServerDeviceView get err:[' + str(err) + ']')
        return IoTErrorResponse.GenResponse()

    @iwebserver_logger_c
    def post(self, request):
        try:
            if (ParasUtil.is_missing_paras(request.query_params, ['workstationId', 'roomId'])):
                return IoTErrorResponse.GenParasErrorResponse(error_msg='missing workstationId or roomId')
            workstationId = request.query_params['workstationId']
            roomId = request.query_params['roomId']

            if(ParasUtil.is_missing_paras(request.data, ['macAddress', 'deviceType'])):
                return IoTErrorResponse.GenParasErrorResponse(error_msg='missing macAddress or deviceType')
            macAddress = request.data['macAddress'].lower()

            deviceType = request.data['deviceType']
            if(deviceType not in dict(DEVICE_TYPE_CHOICES)):
                Log.error('deviceType {} not in [{}]'.format(deviceType, dict(DEVICE_TYPE_CHOICES)))
                return IoTErrorResponse.GenResponse(error_code=iWebServerConfig.IWEBSERVER_ERROR_CODE_CREATE_ROOM_FAILED, error_msg='deviceType {} not in [{}]'.format(deviceType, dict(DEVICE_TYPE_CHOICES)))


            # check macAddress
            if(deviceType == 'container'):
                macAddress = '20:{}:{}:{}:11:{}'.format(CommonTools.getRamdomHex(2), CommonTools.getRamdomHex(2), CommonTools.getRamdomHex(2), CommonTools.getRamdomHex(2)).lower()
            else:
                if(not ParasUtil.is_valid_mac(macAddress)):
                    Log.error('macAddress error')
                    return IoTErrorResponse.GenParasErrorResponse(error_msg='macAddress error')
                # TODO: only one mac is temporarily supported
                if (DeviceInfo.objects.filter(macAddress=macAddress).last() != None):
                    Log.error('device {} already presenced'.format(macAddress))
                    return IoTErrorResponse.GenResponse(error_code=iWebServerConfig.IWEBSERVER_ERROR_CODE_DEVICE_ALREADY_PRESENCED, error_msg='device {} already presenced'.format(macAddress))

            workstation = WorkstationInfo.objects.filter(id=workstationId, owner_id=request.user.id).last()
            if(workstation == None):
                return IoTErrorResponse.GenParasErrorResponse(error_msg='workstationId {} is invalid'.format(workstationId))
            room = RoomInfo.objects.filter(roomId=roomId, workstation=workstation).last()
            if (room == None):
                return IoTErrorResponse.GenParasErrorResponse(error_msg='roomId {} is invalid'.format(roomId))

            # check deviceType
            # TODO: only one type is temporarily supported
            if (DeviceInfo.objects.filter(deviceType=deviceType, room=room, workstation=workstation, owner_id=request.user.id).last() != None):
                Log.error('deviceType {} already presenced'.format(deviceType))
                return IoTErrorResponse.GenResponse(error_code=iWebServerConfig.IWEBSERVER_ERROR_CODE_DEVICE_ALREADY_PRESENCED, error_msg='deviceType {} already presenced'.format(deviceType))

            device = DeviceInfo.objects.filter(macAddress=macAddress, room=room, workstation=workstation, owner_id=request.user.id).last()
            if(device != None):
                Log.error('device {} already presenced'.format(macAddress))
                return IoTErrorResponse.GenResponse(error_code=iWebServerConfig.IWEBSERVER_ERROR_CODE_DEVICE_ALREADY_PRESENCED, error_msg='device {} already presenced'.format(macAddress))

            device = DeviceInfo(macAddress=macAddress, deviceType=deviceType, room=room, workstation=workstation, owner_id=request.user.id)
            device_util = DeviceHTTPRequestUtil()
            if(not device_util.regisiter(device)):
                Log.error('regisiter request failed')
                return IoTErrorResponse.GenResponse(error_msg='regisiter request failed')
            device.save()
            # assign_perm('pcd.{}'.format(iWebServerConfig.IWEBSERVER_PERMISSION_DEVICE_ACCESS), User.objects.filter(id=request.user.id).last(), device)
            return IoTSuccessResponse().GenResponse(data=device.to_dict())
        except Exception as err:
            Log.exception('iWebServerDeviceView post err:[' + str(err) + ']')
        return IoTErrorResponse.GenResponse()

    @iwebserver_logger_c
    def delete(self, request):
        try:
            if (ParasUtil.is_missing_paras(request.query_params, ['workstationId', 'roomId', 'deviceId'])):
                return IoTErrorResponse.GenParasErrorResponse(error_msg='missing workstationId or roomId or deviceId')

            device = DeviceInfo.objects.filter(id=request.query_params['deviceId'], workstation_id=request.query_params['workstationId'], room__roomId=request.query_params['roomId'], owner_id=request.user.id).last()
            if (device == None):
                Log.error('device {} not presenced'.format(request.query_params['deviceId']))
                return IoTErrorResponse.GenResponse(error_code=iWebServerConfig.IWEBSERVER_ERROR_CODE_DEVICE_NOT_PRESENCED, error_msg='device not presenced')

            device.do_delete()
            return IoTSuccessResponse().GenResponse()
        except Exception as err:
            Log.exception('iWebServerDeviceView delete err:[' + str(err) + ']')
        return IoTErrorResponse.GenResponse()