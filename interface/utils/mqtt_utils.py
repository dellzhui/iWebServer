import json
import logging
import re
import ssl
import time
from paho.mqtt import client as mqtt
from interface.config import iWebServerBaseConfig
from interface.utils.tools import DBHandleTask

Log = logging.getLogger(__name__)


class MqttConfig:
    MQTT_CONFIG_MODE_SUB = 'sub'
    MQTT_CONFIG_MODE_PUB = 'pub'

    def __init__(self, MqttMode=MQTT_CONFIG_MODE_SUB, MqttUser=None, MqttPassword=None, MqttServerUrl=None, MqttServerPort=1883, MqttKeepAliveTime_S=60, RequestId=None, SubscribeTopicList=None, PublishTopic=None, PublishPayload: str=None, WaitingForPublish=True, WaitingForPublishTimeoutS=20, on_message_cb=None):
        self.MqttMode = MqttMode
        self.MqttUser = MqttUser
        self.MqttPassword = MqttPassword
        self.MqttServerUrl = MqttServerUrl
        self.MqttServerPort = MqttServerPort
        self.MqttKeepAliveTime_S = MqttKeepAliveTime_S
        self.RequestId = RequestId
        self.SubscribeTopicList = SubscribeTopicList
        self.PublishTopic = PublishTopic
        self.PublishPayload: str = PublishPayload
        self.WaitingForPublish = WaitingForPublish
        self.WaitingForPublishTimeoutS = WaitingForPublishTimeoutS
        self.on_message_cb = on_message_cb

        self.CA = iWebServerBaseConfig.IWEBSERVER_MQTT_TLS_CA_PATH
        self.Cert = iWebServerBaseConfig.IWEBSERVER_MQTT_TLS_CERT_PATH
        self.PrivateKey = iWebServerBaseConfig.IWEBSERVER_MQTT_TLS_PRIVATE_KEY_PATH
        self.IOT_TLS_FLAG = iWebServerBaseConfig.IWEBSERVER_MQTT_TLS_ENABLE
        self.IOT_TLS_PORT = iWebServerBaseConfig.IWEBSERVER_MQTT_TLS_PORT
        self.DEFAULT_IOT_TLS_PORT = 8883

    def __is_paras_empty(self, paras: list):
        for item in paras:
            if(item == None or item == ''):
                return True
        return False

    def is_mqtt_config_valid(self):
        if(self.MqttMode not in [MqttConfig.MQTT_CONFIG_MODE_SUB, MqttConfig.MQTT_CONFIG_MODE_PUB]):
            return False

        if (self.__is_paras_empty([self.MqttUser, self.MqttPassword, self.MqttServerUrl, self.MqttServerPort, self.MqttKeepAliveTime_S, self.SubscribeTopicList])):
            return False

        if (self.MqttMode in [MqttConfig.MQTT_CONFIG_MODE_SUB]):
            if(self.on_message_cb == None):
                return False

        if (self.MqttMode in [MqttConfig.MQTT_CONFIG_MODE_PUB]):
            if(self.__is_paras_empty([self.RequestId, self.PublishTopic, self.PublishPayload, self.WaitingForPublish])):
                return False
        return True


class MqttUtils:
    def __init__(self, config: MqttConfig):
        self.mqttConfig = config
        self.mqttClient = mqtt.Client(userdata=self)
        self.mqttClient.on_connect = self.__on_connect
        self.mqttClient.on_message = self.__on_message
        # self.mqttClient.on_log = self._on_log
        self.mqttClient.on_socket_close = self._on_socket_close

        self.OnPublishPayload = None
        self._stopped = False
        self._connected = False
        self._published = False

    def _on_log(self, client, userdata, level, buf):
        Log.log(level, 'on log:{}'.format(buf))

    def _on_socket_close(self, client, userdata, sock):
        if(self.mqttConfig.MqttMode == MqttConfig.MQTT_CONFIG_MODE_PUB):
            return
        Log.error('_on_socket_close')
        self._connected = False
        while(self._stopped == False):
            try:
                Log.error('_on_socket_close, {} {}, we will reconnect'.format(self.mqttClient, client))
                client.reconnect()
                Log.info('reconnect succeed')
                return
            except Exception as err:
                Log.exception('_on_socket_close err:[' + str(err) + ']')
            time.sleep(5)

    def __on_connect_mode_sub(self, client):
        if(self.mqttConfig.MqttMode != MqttConfig.MQTT_CONFIG_MODE_SUB):
            return

        if (self.mqttConfig.SubscribeTopicList != None):
            for item in self.mqttConfig.SubscribeTopicList:
                Log.info('we will sub ' + item)
                client.subscribe(item, 0)

    def __on_connect_mode_pub(self, client):
        if (self.mqttConfig.MqttMode != MqttConfig.MQTT_CONFIG_MODE_PUB):
            return

        if (self.mqttConfig.SubscribeTopicList != None):
            for item in self.mqttConfig.SubscribeTopicList:
                Log.info('we will sub ' + item)
                client.subscribe(item, 0)

        if (self.mqttConfig.PublishTopic != None):
            Log.info('we will pub ' + self.mqttConfig.PublishTopic)
            Log.info(self.mqttConfig.PublishPayload)
            client.publish(topic=self.mqttConfig.PublishTopic, payload=self.mqttConfig.PublishPayload, qos=0)

        if (self.mqttConfig.WaitingForPublish == False):
            self._published = True

    def __on_connect(self, client, userdata, flags, rc):
        Log.info("Connected with result code "+str(rc))

        if(self.mqttConfig.MqttMode == MqttConfig.MQTT_CONFIG_MODE_SUB):
            self.__on_connect_mode_sub(client)
        elif(self.mqttConfig.MqttMode == MqttConfig.MQTT_CONFIG_MODE_PUB):
            self.__on_connect_mode_pub(client)

        self._connected = True

    def __on_message(self, client, userdata, msg):
        try:
            payload = msg.payload
            if(payload != None and type(payload) == bytes):
                payload = payload.decode('utf-8')
            Log.info('__on_message:receive [{}] [{}]'.format(msg.topic, payload))

            if(self.mqttConfig.MqttMode == MqttConfig.MQTT_CONFIG_MODE_SUB):
                if (self.mqttConfig.on_message_cb != None):
                    self.mqttConfig.on_message_cb(msg.topic, payload)
            elif(self.mqttConfig.MqttMode == MqttConfig.MQTT_CONFIG_MODE_PUB):
                try:
                    response = json.loads(payload)
                    if ('RequestId' not in response):
                        return
                    if (self.mqttConfig.RequestId == None or self.mqttConfig.RequestId != response['RequestId']):
                        Log.info('received another request_id')
                        return
                except Exception as err:
                    Log.exception('err:[' + str(err) + ']')
                    return
                self.OnPublishPayload = payload
                self._published = True
        except Exception as err:
            Log.exception('__on_message err:[' + str(err) + ']')

    def get_received_onpublish_payload(self):
        return self.OnPublishPayload

    def checkPortIsValid(self, port):
        try:
            regex = '([0-9]|[1-9]\d{1,3}|[1-5]\d{4}|6[0-4]\d{3}|65[0-4]\d{2}|655[0-2]\d|6553[0-5])$'
            if re.match(regex, port) != None:
                return True
            else:
                return False
        except Exception as err:
            Log.exception(str(err))
            return False

    def start_mqtt_task_impl(self, paras):
        mqtt_utils: MqttUtils = paras
        if(mqtt_utils == None):
            Log.error('start_mqtt_task_impl:handle is None')
            return
        if(not mqtt_utils.mqttConfig.is_mqtt_config_valid()):
            Log.error('check mqtt config error')
            return
        mqtt_utils.mqttClient.username_pw_set(mqtt_utils.mqttConfig.MqttUser, mqtt_utils.mqttConfig.MqttPassword)
        while (mqtt_utils._stopped == False):
            Log.info('begin to connect')
            try:
                if mqtt_utils.mqttConfig.IOT_TLS_FLAG == True:
                    mqtt_utils.mqttClient.tls_set(ca_certs=mqtt_utils.mqttConfig.CA, certfile=mqtt_utils.mqttConfig.Cert, keyfile=mqtt_utils.mqttConfig.PrivateKey, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS, ciphers=None)
                    if mqtt_utils.checkPortIsValid(mqtt_utils.mqttConfig.IOT_TLS_PORT):
                        mqtt_utils.mqttClient.connect(mqtt_utils.mqttConfig.MqttServerUrl, int(mqtt_utils.mqttConfig.IOT_TLS_PORT), mqtt_utils.mqttConfig.MqttKeepAliveTime_S)
                    else:
                        mqtt_utils.mqttClient.connect(mqtt_utils.mqttConfig.MqttServerUrl, mqtt_utils.mqttConfig.DEFAULT_IOT_TLS_PORT, mqtt_utils.mqttConfig.MqttKeepAliveTime_S)
                else:
                    mqtt_utils.mqttClient.connect(mqtt_utils.mqttConfig.MqttServerUrl, mqtt_utils.mqttConfig.MqttServerPort, mqtt_utils.mqttConfig.MqttKeepAliveTime_S)
                break
            except Exception as err:
                Log.exception('connect error:[' + str(err) + ']')
                time.sleep(5)
        mqtt_utils.mqttClient.loop(timeout=1.0)
        index = 0
        while (mqtt_utils._stopped == False):
            if(mqtt_utils.mqttConfig.MqttMode == MqttConfig.MQTT_CONFIG_MODE_PUB):
                if(index < mqtt_utils.mqttConfig.WaitingForPublishTimeoutS and mqtt_utils._published == False):
                    Log.info('waiting for onpublish:' + str(index + 1))
                else:
                    break
            mqtt_utils.mqttClient.loop(timeout=1.0)
            index += 1
        Log.info('start_mqtt_task_impl:we will disconnect mqtt')
        mqtt_utils.mqttClient.disconnect()

    def start_mqtt_task_sync(self, handle):
        return self.start_mqtt_task_impl(handle)

    def start_mqtt_task_async(self, handle):
        task = DBHandleTask(cb=self.start_mqtt_task_impl, paras=handle)
        task.start()

    def stop_mqtt_task(self):
        self._stopped = True
        index = 0
        while(index < 10 and self._connected == True):
            time.sleep(1)
            index += 1

    def do_publish(self, topic, payload):
        if(self._connected == False):
            Log.error('do_publish:not connected')
            return False
        Log.info('publish topic:{}, payload:{}'.format(topic, payload))
        result = self.mqttClient.publish(topic, payload)
        Log.info('rc is {}'.format(result.rc))
        if(result.rc == mqtt.MQTT_ERR_SUCCESS):
            return True
        return False
