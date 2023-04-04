import json
import time
from interface.config import iWebServerBaseConfig
from interface.utils.http_util import HTTPRequestUtil
from interface.utils.iot_utils import IoTUtils
from interface.utils.log_utils import loggerr
from standalong.config import MQTTSubscriberServiceConfig

Log = loggerr(__name__).getLogger()


class MQTTSubscriberService:
    def __init__(self):
        self._stopped = False
        self._iot_util = IoTUtils(DeviceName=iWebServerBaseConfig.IWEBSERVER_MQTT_USERNAME, DeviceSecret=iWebServerBaseConfig.IWEBSERVER_MQTT_PASSWORD, on_message_cb=self._on_mqtt_msg_cb, sub_topic_list=self._sub_topic_list)
        self.http_util = HTTPRequestUtil(base_url=MQTTSubscriberServiceConfig.IWEBSERVER_3D_PCD_BASE_URL)

    @property
    def _sub_topic_list(self):
        # TODO: sub others
        sub_list = ['/sys/rms/crc/+/+/response/publisherReady']
        return sub_list

    def _on_mqtt_msg_cb(self, topic, msg: str):
        try:
            Log.info('topic:[{}], payload:[{}]'.format(topic, msg))
            result = self.http_util.do_post(url='/notify/webrtc', data={'type': 'mqtt', 'data': json.loads(msg)})
        except Exception as err:
            Log.exception('_on_mqtt_msg_cb err:[' + str(err) + ']')

    def start_sync(self):
        while(self._stopped == False):
            try:
                self._iot_util.StartMqttTask(sync=True)
                Log.error('service exited')
                time.sleep(10)
            except Exception as err:
                Log.exception('start_sync err:[' + str(err) + ']')
                time.sleep(10)
