import logging

from django.contrib.auth.models import User
from guardian.shortcuts import assign_perm
from rest_framework.generics import GenericAPIView
from pcd.config import iWebServerConfig
from interface.datatype.datatype import IoTErrorResponse, IoTSuccessResponse
from interface.utils.tools import ParasUtil, CommonTools
from interface.views import iwebserver_logger
from pcd.models import RoomInfo
from pcd.utils.janus_utils import JanusHTTPRequestUtil

Log = logging.getLogger(__name__)


class iWebServerRoomView(GenericAPIView):
    @iwebserver_logger
    def get(self, request):
        try:
            if (ParasUtil.is_missing_paras(request.query_params, ['workstationId'])):
                return IoTErrorResponse.GenParasErrorResponse(error_msg='missing workstationId')

            rooms = RoomInfo.objects.filter(workstation_id=request.query_params['workstationId'], owner_id=request.user.id)
            if ('roomId' in request.query_params):
                rooms = rooms.filter(roomId=request.query_params['roomId'])
            return IoTSuccessResponse().GenResponse(data=[item.to_dict() for item in rooms])
        except Exception as err:
            Log.exception('iWebServerRoomView get err:[' + str(err) + ']')
        return IoTErrorResponse.GenResponse()

    @iwebserver_logger
    def post(self, request):
        try:
            if (ParasUtil.is_missing_paras(request.query_params, ['workstationId'])):
                return IoTErrorResponse.GenParasErrorResponse(error_msg='missing workstationId')

            if(ParasUtil.is_missing_paras(request.data, ['roomName'])):
                return IoTErrorResponse.GenParasErrorResponse(error_msg='missing roomName')

            room = RoomInfo.objects.filter(name=request.data['roomName'], workstation_id=request.query_params['workstationId'], owner_id=request.user.id).last()
            if(room != None):
                Log.error('room {} already presenced'.format(request.data['roomName']))
                return IoTErrorResponse.GenResponse(error_code=iWebServerConfig.IWEBSERVER_ERROR_CODE_ROOM_ALREADY_PRESENCED, error_msg='room {} already presenced'.format(request.data['roomName']))

            room = RoomInfo(name=request.data['roomName'], workstation_id=request.query_params['workstationId'], owner_id=request.user.id)
            room.save()
            room.roomId = room.id + 2000
            room.roomJoinPin = CommonTools.getRamdomString(16)
            janus_util = JanusHTTPRequestUtil()
            if(janus_util.create_video_room(roomId=room.roomId, roomJoinPin=room.roomJoinPin)):
                room.save()
                # assign_perm('pcd.{}'.format(iWebServerConfig.IWEBSERVER_PERMISSION_ROOM_ACCESS), User.objects.filter(id=request.user.id).last(), room)
                return IoTSuccessResponse().GenResponse(data=room.to_dict())
            room.delete()
            return IoTErrorResponse.GenResponse(error_code=iWebServerConfig.IWEBSERVER_ERROR_CODE_CREATE_ROOM_FAILED, error_msg='create janus rom failed')
        except Exception as err:
            Log.exception('iWebServerRoomView post err:[' + str(err) + ']')
        return IoTErrorResponse.GenResponse()

    @iwebserver_logger
    def put(self, request):
        try:
            if (ParasUtil.is_missing_paras(request.query_params, ['workstationId'])):
                return IoTErrorResponse.GenParasErrorResponse(error_msg='missing workstationId')

            if (ParasUtil.is_missing_paras(request.query_params, ['roomId'])):
                return IoTErrorResponse.GenParasErrorResponse(error_msg='missing roomId')
            if (ParasUtil.is_missing_paras(request.data, ['roomName'])):
                return IoTErrorResponse.GenParasErrorResponse(error_msg='missing roomName')

            if (request.data['roomName'] == ''):
                Log.error('invalid roomName')
                return IoTErrorResponse.GenResponse(error_code=iWebServerConfig.IWEBSERVER_ERROR_CODE_PASSWORD_NOT_MATCH, error_msg='invalid roomName')

            room = RoomInfo.objects.filter(roomId=request.query_params['roomId'], workstation_id=request.query_params['workstationId'], owner_id=request.user.id).last()
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
            if (ParasUtil.is_missing_paras(request.query_params, ['workstationId'])):
                return IoTErrorResponse.GenParasErrorResponse(error_msg='missing workstationId')

            if (ParasUtil.is_missing_paras(request.query_params, ['roomId'])):
                return IoTErrorResponse.GenParasErrorResponse()

            room = RoomInfo.objects.filter(roomId=request.query_params['roomId'], workstation_id=request.query_params['workstationId'], owner_id=request.user.id).last()
            if (room == None):
                Log.error('room {} not presenced'.format(request.query_params['roomId']))
                return IoTErrorResponse.GenResponse(error_code=iWebServerConfig.IWEBSERVER_ERROR_CODE_WORKSTATION_NOT_PRESENCED, error_msg='room not presenced')

            janus_util = JanusHTTPRequestUtil()
            if(janus_util.destroy_video_room(room.roomId, room.roomJoinPin)):
                room.do_delete()
                return IoTSuccessResponse().GenResponse()
            return IoTErrorResponse.GenResponse(error_code=iWebServerConfig.IWEBSERVER_ERROR_CODE_DESTROY_ROOM_FAILED, error_msg='destroy janus room failed')
        except Exception as err:
            Log.exception('iWebServerRoomView delete err:[' + str(err) + ']')
        return IoTErrorResponse.GenResponse()
