import logging
from interface.utils.http_util import HTTPRequestUtil
from interface.utils.tools import CommonTools
from pcd.config import iWebServerConfig

Log = logging.getLogger(__name__)


class JanusHTTPRequestUtil(HTTPRequestUtil):
    def __init__(self):
        super().__init__(base_url=iWebServerConfig.IWEBSERVER_JANUS_BASE_URL)

    def __is_successful_response(self, result):
        try:
            return result['janus'] == 'success'
        except Exception:
            return False

    def create_session(self):
        result = self.do_post(url='', data={"janus": "create", "transaction": CommonTools.getRamdomString(16)})
        if(result == None or not self.__is_successful_response(result)):
            Log.error('create session failed')
            return None
        try:
            session_id = result['data']['id']
            Log.info('got session id is {}'.format(session_id))
            return session_id
        except Exception as err:
            Log.exception('parse session info err:[' + str(err) + ']')
        return None

    def attach_video_room(self, session_id):
        if(session_id == None):
            Log.error('invalid session_id')
            return None
        data = {
            "janus": "attach",
            "plugin": "janus.plugin.videoroom",
            "opaque_id": "screensharingtest-{}".format(CommonTools.getRamdomString(12)),
            "transaction": CommonTools.getRamdomString(12)
        }
        result = self.do_post(url='/{}'.format(session_id), data=data)
        if(result == None or not self.__is_successful_response(result)):
            Log.error('attach video room failed')
            return None
        try:
            attach_id = result['data']['id']
            Log.info('got attach id is {}'.format(attach_id))
            return attach_id
        except Exception as err:
            Log.exception('parse attach info err:[' + str(err) + ']')
        return None

    def create_video_room(self, roomId: int, roomJoinPin):
        if(roomId == None or roomJoinPin == None or roomJoinPin == ''):
            Log.error('invalid paras')
            return None
        session_id = self.create_session()
        if(session_id != None):
            attach_id = self.attach_video_room(session_id)
            if(attach_id != None):
                data = {
                    "janus": "message",
                    "body": {
                        "request": "create",
                        "room": roomId,
                        "description": "PCD Room {}".format(roomId),
                        "fir_freq": 10,
                        "audiocodec": "opus,g722,pcmu,pcma,isac32,isac16",
                        "videocodec": "h264,vp8,vp9",
                        "record": False,
                        "notify_joining": True,
                        "permanent": True,
                        "secret": roomJoinPin,
                        "bitrate": 9000000,
                        "publishers": 100
                    },
                    "transaction": CommonTools.getRamdomString(12)
                }
                result = self.do_post(url='/{}/{}'.format(session_id, attach_id), data=data)
                if (result == None or not self.__is_successful_response(result)):
                    Log.error('create video room failed')
                    return None
                Log.info('create room {} succeed'.format(roomId))
                return True
        Log.error('create video room failed')
        return False

    def destroy_video_room(self, roomId: int, roomJoinPin):
        if(roomId == None or roomJoinPin == None or roomJoinPin == ''):
            Log.error('invalid paras')
            return None
        session_id = self.create_session()
        if(session_id != None):
            attach_id = self.attach_video_room(session_id)
            if(attach_id != None):
                data = {
                    "janus": "message",
                    "body": {
                        "request": "destroy",
                        "room": roomId,
                        "permanent": True,
                        "secret": roomJoinPin
                    },
                    "transaction": CommonTools.getRamdomString(12)
                }
                result = self.do_post(url='/{}/{}'.format(session_id, attach_id), data=data)
                if (result == None or not self.__is_successful_response(result)):
                    Log.error('destroy video room failed')
                    return None
                Log.info('destroy room {} succeed'.format(roomId))
                return True
        Log.error('destroy video room failed')
        return False


