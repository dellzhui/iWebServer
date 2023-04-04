import sys
from interface.utils.log_utils import loggerr
from standalong.mqtt_subscriber_service.mqtt_subscriber_service import MQTTSubscriberService

Log = loggerr(__name__).getLogger()


def main(argv):
    service = MQTTSubscriberService()
    service.start_sync()



if __name__ == '__main__':
    main(sys.argv[0:])
