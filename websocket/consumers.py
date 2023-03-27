import json
import logging
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import User
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken
from jwt import decode as jwt_decode

from iWebServer import settings
from imqtt.utils.iot_utils import IoTUtils

Log = logging.getLogger(__name__)


class xChatConsumer(WebsocketConsumer):
    def __init__(self):
        self.__user: User | None = None
        self.__iot_util: IoTUtils | None = None
        self.__sub_topic_list = []
        super().__init__()

    def __on_mqtt_msg_cb(self, topic, msg):
        self.send(msg)

    def __get_sub_topic_list(self):
        #TODO:
        return None

    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        Log.info('{} disconnected'.format(self.__user.username if(self.__user != None) else None))
        if (self.__iot_util != None):
            self.__iot_util.StopMqttTask()
        self.__user = None

    def receive(self, text_data=None, bytes_data=None):
        try:
            Log.info('receive {}'.format(text_data))
            text_data_json = json.loads(text_data)
            type = text_data_json['type']
            if (self.__user == None):
                if (type != 'auth'):
                    Log.error('not authed')
                    self.send(text_data=json.dumps({
                        'message': 'not authed'
                    }))
                    return self.close()
                access_token = text_data_json['access_token']
                try:
                    UntypedToken(access_token)
                except (InvalidToken, TokenError) as err:
                    Log.exception('token is invalid, err:[' + str(err) + ']')
                    self.send(text_data=json.dumps({
                        'message': 'token is invalid'
                    }))
                    return self.close()
                else:
                    decoded_data = jwt_decode(access_token, settings.SECRET_KEY, algorithms=["HS256"])
                    self.__user = User.objects.filter(id=decoded_data["user_id"]).last()
                    if(self.__user != None):
                        self.__get_sub_topic_list()
                        self.__iot_util = IoTUtils(DeviceName=None, DeviceSecret=None, on_message_cb=self.__on_mqtt_msg_cb, sub_topic_list=self.__sub_topic_list)
                        self.__iot_util.StartMqttTaskAsync()
                        return self.send(text_data=json.dumps({
                            'message': 'auth succeed'
                        }))

            if (self.__user == None):
                Log.error('not authed')
                self.send(text_data=json.dumps({
                    'message': 'not authed'
                }))
                return self.close()

            return self.send(text_data=json.dumps({
                'message': 'succeed'
            }))
        except Exception as err:
            Log.exception('receive err:[' + str(err) + ']')
            self.send(text_data=json.dumps({
                'message': 'internal error'
            }))
        return self.close()
