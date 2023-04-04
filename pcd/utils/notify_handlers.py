import logging
from pcd.utils.mqtt_handlers import MQTThandlers

Log = logging.getLogger(__name__)


class NotifyHandler:
    def __init__(self):
        self.__handlers = {
            'mqtt': MQTThandlers(),
        }

    def notify(self, handler_type: str, data: dict):
        if(handler_type == None or handler_type not in self.__handlers):
            return False
        try:
            return self.__handlers[handler_type].notify(data)
        except Exception as err:
            logging.exception('notify err:[' + str(err) + ']')
        return False
