import json
import logging
from websocket.consumers import iWebServerConsumer

Log = logging.getLogger(__name__)


class PCDConsumer(iWebServerConsumer):
    def __init__(self):
        super().__init__()

    def _on_mqtt_msg_cb(self, topic, msg):
        self.send(msg)

    def _handle_ws_message(self, text_data_json: dict=None, bytes_data=None):
        return self.send(text_data=json.dumps({'message': 'succeed'}))

    def _get_sub_topic_list(self):
        #TODO:
        return None
