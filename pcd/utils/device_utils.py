import json
from interface.utils.log_utils import loggerr
from interface.utils.http_util import HTTPRequestUtil
from pcd.config import iWebServerConfig
from pcd.datatype.datatype import CreateContainerDataType, DestroyContainerDataType
from pcd.models import DeviceInfo

Log = loggerr(__name__).getLogger()


class DeviceHTTPRequestUtil(HTTPRequestUtil):
    def __init__(self):
        super().__init__(base_url=iWebServerConfig.IWEBSERVER_DEVICE_BASE_URL)
        self.device_type_info = {'hub': 'HUB', 'container': 'Container', 'stb': 'STB'}

    def __is_successful_response(self, result):
        try:
            return result['success'] == True
        except Exception:
            return False

    def regisiter(self, device: DeviceInfo):
        try:
            data = device.to_regisiter_request_data()
            Log.info('got registe request data is {}'.format(data))
            result = self.do_post(url='/api/device/autoregister/', data=data)
            if (result == None or not self.__is_successful_response(result)):
                Log.error('regisiter request failed')
                return False
            Log.info('got regisiter result is {}'.format(json.dumps(result)))
            result = result['msg']
            device.productKey = result['productKey']
            device.deviceName = result['deviceName']
            device.deviceSecret = result['deviceSecret']
            return True
        except Exception as err:
            Log.exception('regisiter err:[' + str(err) + ']')
        return False

    def create_container(self, device: DeviceInfo):
        try:
            data = CreateContainerDataType(roomIdStr='{}'.format(device.room.roomId), roomJoinPin=device.room.roomJoinPin, macAddress=device.macAddress, email=device.owner.email).to_dict()
            Log.info('request data is {}'.format(json.dumps(data)))
            result = self.do_post(url='/api/rms/start_self_container/', data=data)
            if (result == None or not self.__is_successful_response(result)):
                Log.error('create container request failed')
                return False
            Log.info('got result is {}'.format(json.dumps(result)))
            # https://www.wolai.com/yang_ids/e5UPobHGfhX85QEiW4fkQa#4vEHb1Z9mR5QN5fJ5NPSLn
            device.nameSpace = result['msg']['namespace']
            device.turnServer = result['msg']['turnServer']
            device.turnUserName = result['msg']['turnUserName']
            device.turnCredential = result['msg']['turnCredential']
            device.rtcbotConnectUrl = result['msg']['rtcbotConnectUrl']
            device.noVNCConnectUrl = result['msg']['noVNCConnectUrl']
            device.save()
            return True
        except Exception as err:
            Log.exception('create container err:[' + str(err) + ']')
        return False

    def destroy_container(self, device: DeviceInfo):
        try:
            result = self.do_post(url='/api/rms/destroy_container_by_name/', data=DestroyContainerDataType(nameSpace=device.nameSpace, email=device.owner.email).to_dict())
            if (result == None or not self.__is_successful_response(result)):
                Log.error('destroy container request failed')
                return False
            Log.info('got result is {}'.format(json.dumps(result)))
            return True
        except Exception as err:
            Log.exception('destroy container err:[' + str(err) + ']')
        return False
