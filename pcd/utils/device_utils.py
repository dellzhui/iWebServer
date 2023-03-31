import json
import logging
from interface.utils.http_util import HTTPRequestUtil
from pcd.config import iWebServerConfig
from pcd.models import DeviceInfo

Log = logging.getLogger(__name__)


class DeviceHTTPRequestUtil(HTTPRequestUtil):
    def __init__(self) -> None:
        super().__init__(base_url=iWebServerConfig.IWEBSERVER_DEVICE_BASE_URL)
        self.device_type_info = {'hub': 'HUB', 'container': 'Container', 'stb': 'STB'}

    def __is_successful_response(self, result):
        try:
            return result['success']
        except Exception:
            return False

    def regisiter(self, device: DeviceInfo):
        try:
            result = self.do_post(url='/api/device/autoregister/', data={"DeviceType": self.device_type_info[device.deviceType], "Mac": device.macAddress, "SerialNumber": device.serialNumber})
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
