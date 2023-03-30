import json
import logging
import os
import random

from interface.utils.mqtt_utils import MqttUtils

Log = logging.getLogger(__name__)


class IoTUtils:
    def __init__(self, DeviceName=None, DeviceSecret=None, on_message_cb=None, sub_topic_list=None):
        self.DeviceName = DeviceName
        self.DeviceSecret = DeviceSecret
        self.__on_message_cb = on_message_cb
        self.__sub_topic_list = sub_topic_list

        self.MqttServerUrlList = os.environ.get('IDMS_IOT_MQTT_SERVER_LIST', '')
        self.MqttKeepAliveTime_S = 60

        self.__mqtt_utils = []

    def __get_mosquitto_host_list(self):
        host_list = []
        try:
            for item in self.MqttServerUrlList.split(';'):
                host = item.split(':')[0]
                if (host == ''):
                    continue
                port = 1883
                try:
                    if (len(item.split(':')) > 1):
                        port = int(item.split(':')[1])
                except Exception:
                    port = 1883
                host_list.append({'host': host, 'port': port})
        except Exception as err:
            Log.exception('__get_mosquitto_host_list err:[' + str(err) + ']')
            return []
        Log.info('get host list is ' + str(host_list))
        return host_list

    def __on_message(self, topic, msg):
        return self.__on_message_cb(topic, msg)

    def StartMqttTaskAsync(self):
        host_list = self.__get_mosquitto_host_list()
        if (host_list == None or len(host_list) == 0):
            Log.error('mqtt server list is None')
            return

        for item in host_list:
            mqtt_util = MqttUtils(MqttUser=self.DeviceName,
                                  MqttPassword=self.DeviceSecret,
                                  MqttServerUrl=item['host'],
                                  MqttServerPort=item['port'],
                                  MqttKeepAliveTime_S=self.MqttKeepAliveTime_S,
                                  SubscribeTopicList=self.__sub_topic_list,
                                  on_message_cb=self.__on_message)
            Log.info('StartMqttTaskAsync:we will start mqtt task')
            mqtt_util.start_mqtt_task_async(handle=mqtt_util)
            self.__mqtt_utils.append(mqtt_util)

    def StopMqttTask(self):
        Log.info('StopMqttTask:we will stop mqtt task')
        for mqtt_util in self.__mqtt_utils:
            mqtt_util.stop_mqtt_task()

    def PublishDeviceCommonBatchData(self, topic, content, broadcast=False):
        try:
            payload = json.dumps(content) if(isinstance(content, dict)) else content
            Log.info('mqtt payload is {}'.format(payload))
            if(len(self.__mqtt_utils) == 0):
                Log.error('no mqtt connected')
                return False
            if(broadcast == True):
                for mqtt_util in self.__mqtt_utils:
                    mqtt_util.do_publish(topic, payload)
                return True
            return self.__mqtt_utils[random.randint(0, len(self.__mqtt_utils)-1)].do_publish(topic, payload)
        except Exception as err:
            Log.exception('IoTUtils PublishDeviceCommonBatchData err:[' + str(err) + ']')
        return False