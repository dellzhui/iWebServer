import logging
import os
import re
import ssl
import time
from paho.mqtt import client as mqtt
from interface.utils.tools import DBHandleTask

Log = logging.getLogger(__name__)


class MqttUtils:
    def __init__(self, MqttUser=None, MqttPassword=None, MqttServerUrl=None, MqttServerPort=1883, MqttKeepAliveTime_S=60, SubscribeTopicList=None, on_message_cb=None):
        self.MqttUser = MqttUser
        self.MqttPassword = MqttPassword
        self.MqttServerUrl = MqttServerUrl
        self.MqttServerPort = MqttServerPort
        self.MqttKeepAliveTime_S = MqttKeepAliveTime_S
        self.SubscribeTopicList = SubscribeTopicList

        self.Client = mqtt.Client(userdata=self)
        self.Client.on_connect = self.__on_connect
        self.Client.on_message = self.__on_message
        # self.Client.on_log = self.__on_log
        self.Client.on_socket_close = self.__on_socket_close
        self.__on_message_cb = on_message_cb

        self.__stopped = False
        self.__connected = False

        self.CA = os.environ.get('IDMS_IOT_TLS_CA_PATH', '/home/yang/idms/bin/ca/ca.crt')
        self.Cert = os.environ.get('IDMS_IOT_TLS_CERT_PATH', '/home/yang/idms/bin/ca/client.crt')
        self.PrivateKey = os.environ.get('IDMS_IOT_TLS_PRIVATE_KEY_PATH', '/home/yang/idms/bin/ca/client.key')
        self.IOT_TLS_FLAG = True if (int(os.environ.get('IDMS_IOT_TLS_FLAG', 0)) == 1) else False
        self.IOT_TLS_PORT = os.environ.get('IDMS_IOT_TLS_PORT', '')
        self.DEFAULT_IOT_TLS_PORT = 8883

    def __on_log(self, client, userdata, level, buf):
        Log.log(level, 'on log:{}'.format(buf))

    def __on_socket_close(self, client, userdata, sock):
        Log.error('__on_socket_close')
        self.__connected = False
        while(self.__stopped == False):
            try:
                Log.error('__on_socket_close, {} {}, we will reconnect'.format(self.Client, client))
                client.reconnect()
                Log.info('reconnect succeed')
                return
            except Exception as err:
                Log.exception('__on_socket_close err:[' + str(err) + ']')
            time.sleep(5)

    def __on_connect(self, client, userdata, flags, rc):
        Log.info("Connected with result code "+str(rc))

        if(self.SubscribeTopicList != None):
            for item in self.SubscribeTopicList:
                Log.info('we will sub ' + item)
                client.subscribe(item, 0)
        self.__connected = True

    def __on_message(self, client, userdata, msg):
        try:
            payload = msg.payload
            if(payload != None and type(payload) == bytes):
                payload = payload.decode('utf-8')
            Log.info('__on_message:receive [{}] [{}]'.format(msg.topic, payload))
            if (self.__on_message_cb != None):
                self.__on_message_cb(msg.topic, payload)
        except Exception as err:
            Log.exception('__on_message err:[' + str(err) + ']')

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
        mqtt_utils = paras
        if(mqtt_utils == None):
            Log.error('start_mqtt_task_impl:handle is None')
            return
        mqtt_utils.Client.username_pw_set(mqtt_utils.MqttUser, mqtt_utils.MqttPassword)
        while (mqtt_utils.__stopped == False):
            Log.info('begin to connect')
            try:
                if self.IOT_TLS_FLAG == True:
                    mqtt_utils.Client.tls_set(ca_certs=self.CA, certfile=self.Cert, keyfile=self.PrivateKey, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS, ciphers=None)
                    if mqtt_utils.checkPortIsValid(self.IOT_TLS_PORT):
                        mqtt_utils.Client.connect(mqtt_utils.MqttServerUrl, int(self.IOT_TLS_PORT), mqtt_utils.MqttKeepAliveTime_S)
                    else:
                        mqtt_utils.Client.connect(mqtt_utils.MqttServerUrl, self.DEFAULT_IOT_TLS_PORT, mqtt_utils.MqttKeepAliveTime_S)
                else:
                    mqtt_utils.Client.connect(mqtt_utils.MqttServerUrl, mqtt_utils.MqttServerPort, mqtt_utils.MqttKeepAliveTime_S)
                break
            except Exception as err:
                Log.exception('connect error:[' + str(err) + ']')
                time.sleep(5)
        mqtt_utils.Client.loop(timeout=1.0)
        index = 0
        while (mqtt_utils.__stopped == False):
            # Log.info('waiting for onpublish:' + str(index + 1))
            mqtt_utils.Client.loop(timeout=1.0)
            index += 1
        Log.info('start_mqtt_task_impl:we will disconnect mqtt')
        mqtt_utils.Client.disconnect()

    def start_mqtt_task_async(self, handle):
        task = DBHandleTask(cb=self.start_mqtt_task_impl, paras=handle)
        task.start()

    def stop_mqtt_task(self):
        self.__stopped = True
        index = 0
        while(index < 10 and self.__connected == True):
            time.sleep(1)
            index += 1

    def do_publish(self, topic, payload):
        if(self.__connected == False):
            Log.error('do_publish:not connected')
            return False
        Log.info('publish topic:{}, payload:{}'.format(topic, payload))
        result = self.Client.publish(topic, payload)
        Log.info('rc is {}'.format(result.rc))
        if(result.rc == mqtt.MQTT_ERR_SUCCESS):
            return True
        return False
