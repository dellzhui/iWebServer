import logging
from django.contrib.auth.models import User
from django.db import models
from pcd.config import iWebServerConfig
from interface.models import ModelCommonInfo
from django.utils.translation import gettext as _

Log = logging.getLogger(__name__)


DEVICE_TYPE_CHOICES = (
    ('hub', _('HUB')),
    ('container', _('Container')),
    ('stb', _('STB'))
)


class WorkstationInfo(ModelCommonInfo):
    class Meta:
        verbose_name = _('Workstation Info')
        verbose_name_plural = _('Workstation Info')
        permissions = (
            (iWebServerConfig.IWEBSERVER_PERMISSION_WORKSTATION_ACCESS, 'can access workstation'),
        )

    name = models.CharField(null=True, blank=True, db_index=True, max_length=256, verbose_name=_('Workstation Name'))

    owner = models.ForeignKey(User, null=True, blank=True, related_name="workstations", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def to_dict(self):
        return {'workstationId': self.id, 'workstationName': self.name, 'createTime': self.createTime, 'updateTime': self.updateTime}

    def do_delete(self):
        for device in self.devices.all():
            device.do_delete()
        for room in self.rooms.all():
            room.do_delete()
        super().do_delete()


class RoomInfo(ModelCommonInfo):
    class Meta:
        verbose_name = _('Room Info')
        verbose_name_plural = _('Room Info')
        permissions = (
            (iWebServerConfig.IWEBSERVER_PERMISSION_ROOM_ACCESS, 'can access room'),
        )

    name = models.CharField(null=True, blank=True, db_index=True, max_length=256, verbose_name=_('Room Name'))
    roomId = models.BigIntegerField(null=True, blank=True, db_index=True, verbose_name=_('Room Id'))
    roomJoinPin = models.CharField(null=True, blank=True, max_length=256, verbose_name=_('Room Secret'))
    isPrivate = models.BooleanField(null=True, blank=True, default=True, db_index=True, verbose_name=_('Is Private'))

    workstation = models.ForeignKey(WorkstationInfo, null=True, blank=True, related_name="rooms", on_delete=models.CASCADE)
    owner = models.ForeignKey(User, null=True, blank=True, related_name="rooms", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def to_dict(self):
        return {'workstationId': self.workstation_id, 'roomId': self.roomId, 'roomName': self.name, 'roomJoinPin': self.roomJoinPin, 'createTime': self.createTime, 'updateTime': self.updateTime}

    def do_delete(self):
        for device in self.devices.all():
            device.do_delete()
        super().do_delete()


class DeviceInfo(ModelCommonInfo):
    class Meta:
        verbose_name = _('Device Info')
        verbose_name_plural = _('Device Info')
        permissions = (
            (iWebServerConfig.IWEBSERVER_PERMISSION_DEVICE_ACCESS, 'can access device'),
        )

    productKey = models.CharField(null=True, blank=True, db_index=True, max_length=256, verbose_name=_('Product Key'))
    deviceName = models.CharField(null=True, blank=True, db_index=True, max_length=256, verbose_name=_('Device Name'))
    deviceSecret = models.CharField(null=True, blank=True, max_length=256, verbose_name=_('Device Secret'))
    macAddress = models.CharField(null=True, blank=True, db_index=True, max_length=256, verbose_name=_('Mac Address'))
    serialNumber = models.CharField(null=True, blank=True, db_index=True, max_length=256, verbose_name=_('Serial Number'))
    deviceType = models.CharField(null=True, blank=True, db_index=True, choices=DEVICE_TYPE_CHOICES, max_length=32, verbose_name=_('Device Type'))
    nameSpace = models.CharField(null=True, blank=True, db_index=True, max_length=256, verbose_name=_('Name Space'))

    # ICE
    turnServer = models.CharField(null=True, blank=True, max_length=256, verbose_name=_('TURN Server'))
    turnUserName = models.CharField(null=True, blank=True, max_length=256, verbose_name=_('TURN User Name'))
    turnCredential = models.CharField(null=True, blank=True, max_length=256, verbose_name=_('Turn Credential'))
    rtcbotConnectUrl = models.CharField(null=True, blank=True, max_length=1024, verbose_name=_('RTCBot Url'))
    noVNCConnectUrl = models.CharField(null=True, blank=True, max_length=1024, verbose_name=_('noVNC Url'))

    room = models.ForeignKey(RoomInfo, null=True, blank=True, related_name="devices", on_delete=models.CASCADE)
    workstation = models.ForeignKey(WorkstationInfo, null=True, blank=True, related_name="devices", on_delete=models.CASCADE)
    owner = models.ForeignKey(User, null=True, blank=True, related_name="devices", on_delete=models.CASCADE)

    def __str__(self):
        return self.macAddress

    def to_dict(self):
        return {
            'workstationId': self.workstation_id,
            'roomId': self.room.roomId if(self.room != None) else None,
            'deviceId': self.id,
            'deviceName': self.deviceName,
            'macAddress': self.macAddress,
            'serialNumber': self.serialNumber,
            'deviceType': self.deviceType,
            'createTime': self.createTime,
            'updateTime': self.updateTime
        }

    def is_container(self):
        return self.deviceType is not None and self.deviceType == 'container'

    def is_hub(self):
        return self.deviceType is not None and self.deviceType == 'hub'

    def is_stb(self):
        return self.deviceType is not None and self.deviceType == 'stb'

    def get_bound_devices(self):
        try:
            result = {}
            hubs = self.room.devices.filter(deviceType='hub')
            if(hubs.count() > 1):
                Log.error('more than one hubs')
                return None
            result['hub'] = hubs.last()

            containers = self.room.devices.filter(deviceType='container')
            if (containers.count() > 1):
                Log.error('more than one containers')
                return None
            result['container'] = containers.last()

            stbs = self.room.devices.filter(deviceType='stb')
            if (stbs.count() > 1):
                Log.error('more than one stbs')
                return None
            result['stb'] = stbs.last()
            return result
        except Exception as err:
            Log.exception('get_bound_devices err:[' + str(err) + ']')
        return None

    def to_regisitr_request_data(self):
        device_type_info = {'hub': 'HUB', 'container': 'Container', 'stb': 'STB'}
        try:
            return {
                'DeviceType': device_type_info[self.deviceType],
                'Mac': self.macAddress,
                'SerialNumber': self.serialNumber,
                'roomId': self.room.roomId,
                'roomJoinPin': self.room.roomJoinPin
            }
        except Exception as err:
            Log.exception('to_regisitr_request_data err:[' + str(err) + ']')
        return None
