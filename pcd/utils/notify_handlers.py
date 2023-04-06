from interface.utils.log_utils import loggerr
from pcd.utils.mqtt_handlers import MQTThandlers

Log = loggerr(__name__).getLogger()


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
            Log.exception('notify err:[' + str(err) + ']')
        return False
