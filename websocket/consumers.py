import json
from interface.utils.log_utils import loggerr
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import User
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken
from jwt import decode as jwt_decode

from iWebServer import settings
from interface.config import iWebServerBaseConfig
from interface.datatype.datatype import IoTSuccessResponse, IoTErrorResponse
from interface.utils.iot_utils import IoTUtils

Log = loggerr(__name__).getLogger()


class iWebServerConsumer(WebsocketConsumer):
    def __init__(self):
        self._user: User | None = None
        self._iot_util: IoTUtils | None = None
        super().__init__()

    @property
    def _sub_topic_list(self):
        return None

    def _on_mqtt_msg_cb(self, topic, msg):
        self.send(msg)

    def _handle_ws_message(self, requestId, text_data_json: dict=None, bytes_data=None):
        return self.send(text_data=json.dumps(IoTSuccessResponse().GenJson(data={'message': 'succeed'}, requestId=requestId)))

    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        Log.info('{} disconnected'.format(self._user.username if(self._user != None) else None))
        if (self._iot_util != None):
            self._iot_util.StopMqttTask()
        self._user = None

    def receive(self, text_data=None, bytes_data=None):
        try:
            Log.info('receive {}'.format(text_data))
            text_data_json = json.loads(text_data)
            type = text_data_json['type']
            requestId = text_data_json['requestId']
            if (self._user == None):
                if (type != 'auth'):
                    Log.error('not authed')
                    self.send(text_data=json.dumps(IoTErrorResponse.GenJson(error_msg='not authed', requestId=requestId)))
                    return self.close()
                access_token = text_data_json['access_token']
                try:
                    UntypedToken(access_token)
                except (InvalidToken, TokenError) as err:
                    Log.exception('token is invalid, err:[' + str(err) + ']')
                    self.send(text_data=json.dumps(IoTErrorResponse.GenJson(error_msg='token is invalid', requestId=requestId)))
                    return self.close()
                decoded_data = jwt_decode(access_token, settings.SECRET_KEY, algorithms=["HS256"])
                self._user = User.objects.filter(id=decoded_data["user_id"]).last()
                if(self._user != None):
                    self._iot_util = IoTUtils(DeviceName=iWebServerBaseConfig.IWEBSERVER_MQTT_USERNAME, DeviceSecret=iWebServerBaseConfig.IWEBSERVER_MQTT_PASSWORD, on_message_cb=self._on_mqtt_msg_cb, sub_topic_list=self._sub_topic_list)
                    self._iot_util.StartMqttTaskAsync()
                    return self.send(text_data=json.dumps(IoTSuccessResponse().GenJson(data={'message': 'auth succeed'}, requestId=requestId)))

            if (self._user == None):
                Log.error('not authed')
                self.send(text_data=json.dumps(IoTErrorResponse.GenJson(error_msg='not authed', requestId=requestId)))
                return self.close()

            if (type == 'auth'):
                Log.info('already authed')
                return self.send(text_data=json.dumps(IoTSuccessResponse().GenJson(data={'message': 'already authed'}, requestId=requestId)))

            return self._handle_ws_message(requestId=requestId, text_data_json=text_data_json, bytes_data=bytes_data)
        except Exception as err:
            Log.exception('receive err:[' + str(err) + ']')
            self.send(text_data=json.dumps(IoTErrorResponse.GenJson()))
        return self.close()
