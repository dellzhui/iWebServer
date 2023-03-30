import logging
from rest_framework.generics import GenericAPIView
from web.config import iWebServerConfig
from interface.datatype.datatype import IoTErrorResponse, IoTSuccessResponse
from interface.utils.tools import ParasUtil
from interface.views import iwebserver_logger
from web.models import RoomInfo

Log = logging.getLogger(__name__)


class iWebServerRoomView(GenericAPIView):
    @iwebserver_logger
    def get(self, request):
        try:
            rooms = RoomInfo.objects.filter(owner_id=request.user.id)
            if ('roomId' in request.query_params):
                rooms = rooms.filter(id=request.query_params['roomId'])
            return IoTSuccessResponse().GenResponse(data=[item.to_dict() for item in rooms])
        except Exception as err:
            Log.exception('iWebServerRoomView get err:[' + str(err) + ']')
        return IoTErrorResponse.GenResponse()

    @iwebserver_logger
    def post(self, request):
        try:
            if(ParasUtil.is_missing_paras(request.data, ['roomName'])):
                return IoTErrorResponse.GenParasErrorResponse(error_msg='missing roomName')

            room = RoomInfo.objects.filter(name=request.data['roomName'], owner_id=request.user.id).last()
            if(room != None):
                Log.error('room {} already presenced'.format(request.data['roomName']))
                return IoTErrorResponse.GenResponse(error_code=iWebServerConfig.IWEBSERVER_ERROR_CODE_ROOM_ALREADY_PRESENCED, error_msg='room {} already presenced'.format(request.data['roomName']))

            room = RoomInfo(name=request.data['roomName'], owner_id=request.user.id)
            ### TODO: Call the API of janus here, create a janus room, get roomId, roomJoinPin

            room.save()
            return IoTSuccessResponse().GenResponse(data=room.to_dict())
        except Exception as err:
            Log.exception('iWebServerRoomView post err:[' + str(err) + ']')
        return IoTErrorResponse.GenResponse()

    @iwebserver_logger
    def put(self, request):
        try:
            if (ParasUtil.is_missing_paras(request.query_params, ['roomId'])):
                return IoTErrorResponse.GenParasErrorResponse(error_msg='missing roomId')
            if (ParasUtil.is_missing_paras(request.data, ['roomName'])):
                return IoTErrorResponse.GenParasErrorResponse(error_msg='missing roomName')

            if (request.data['roomName'] == ''):
                Log.error('invalid roomName')
                return IoTErrorResponse.GenResponse(error_code=iWebServerConfig.IWEBSERVER_ERROR_CODE_PASSWORD_NOT_MATCH, error_msg='invalid roomName')

            room = RoomInfo.objects.filter(roomId=request.query_params['roomId'], owner_id=request.user.id).last()
            if (room == None):
                Log.error('room {} not presenced'.format(request.query_params['roomId']))
                return IoTErrorResponse.GenResponse(error_code=iWebServerConfig.IWEBSERVER_ERROR_CODE_WORKSTATION_NOT_PRESENCED, error_msg='room not presenced')

            room.name = request.data['roomName']
            room.save()
            return IoTSuccessResponse().GenResponse(data=room.to_dict())
        except Exception as err:
            Log.exception('iWebServerRoomView put err:[' + str(err) + ']')
        return IoTErrorResponse.GenResponse()

    @iwebserver_logger
    def delete(self, request):
        try:
            if (ParasUtil.is_missing_paras(request.query_params, ['roomId'])):
                return IoTErrorResponse.GenParasErrorResponse()

            room = RoomInfo.objects.filter(roomId=request.query_params['roomId'], owner_id=request.user.id).last()
            if (room == None):
                Log.error('room {} not presenced'.format(request.query_params['roomId']))
                return IoTErrorResponse.GenResponse(error_code=iWebServerConfig.IWEBSERVER_ERROR_CODE_WORKSTATION_NOT_PRESENCED, error_msg='room not presenced')

            # TODO: clear all
            room.delete()
            return IoTSuccessResponse().GenResponse()
        except Exception as err:
            Log.exception('iWebServerRoomView delete err:[' + str(err) + ']')
        return IoTErrorResponse.GenResponse()
