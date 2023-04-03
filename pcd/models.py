from django.contrib.auth.models import User
from django.db import models
from pcd.config import iWebServerConfig
from interface.models import ModelCommonInfo
from django.utils.translation import gettext as _


DEVICE_TYPE_CHOICES = (
    ('hub', _('HUB Device')),
    ('container', _('Container')),
    ('stb', _('STB Device'))
)


class WorkstationInfo(ModelCommonInfo):
    class Meta:
        verbose_name = _('WorkstationInfo')
        verbose_name_plural = _('WorkstationInfo')
        permissions = (
            (iWebServerConfig.IWEBSERVER_PERMISSION_WORKSTATION_ACCESS, 'can access workstation'),
        )

    name = models.CharField(null=True, blank=True, db_index=True, max_length=256, verbose_name=_('Workstation Name'))

    owner = models.ForeignKey(User, null=True, blank=True, related_name="workstations", on_delete=models.CASCADE)

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
        verbose_name = _('RoomInfo')
        verbose_name_plural = _('RoomInfo')
        permissions = (
            (iWebServerConfig.IWEBSERVER_PERMISSION_ROOM_ACCESS, 'can access room'),
        )

    name = models.CharField(null=True, blank=True, db_index=True, max_length=256, verbose_name=_('Room Name'))
    roomId = models.BigIntegerField(null=True, blank=True, db_index=True, verbose_name=_('Room Id'))
    roomJoinPin = models.CharField(null=True, blank=True, max_length=256, verbose_name=_('Room Secret'))
    isPrivate = models.BooleanField(null=True, blank=True, default=True, db_index=True, verbose_name=_('Is Private'))

    workstation = models.ForeignKey(WorkstationInfo, null=True, blank=True, related_name="rooms", on_delete=models.CASCADE)
    owner = models.ForeignKey(User, null=True, blank=True, related_name="rooms", on_delete=models.CASCADE)

    def to_dict(self):
        return {'workstationId': self.workstation_id, 'roomId': self.roomId, 'roomName': self.name, 'roomJoinPin': self.roomJoinPin, 'createTime': self.createTime, 'updateTime': self.updateTime}

    def do_delete(self):
        for device in self.devices.all():
            device.do_delete()
        super().do_delete()


class DeviceInfo(ModelCommonInfo):
    class Meta:
        verbose_name = _('DeviceInfo')
        verbose_name_plural = _('DeviceInfo')
        permissions = (
            (iWebServerConfig.IWEBSERVER_PERMISSION_DEVICE_ACCESS, 'can access device'),
        )

    productKey = models.CharField(null=True, blank=True, db_index=True, max_length=256, verbose_name=_('Product Key'))
    deviceName = models.CharField(null=True, blank=True, db_index=True, max_length=256, verbose_name=_('Device Name'))
    deviceSecret = models.CharField(null=True, blank=True, db_index=True, max_length=256, verbose_name=_('Device Secret'))
    macAddress = models.CharField(null=True, blank=True, db_index=True, max_length=256, verbose_name=_('Mac Address'))
    serialNumber = models.CharField(null=True, blank=True, db_index=True, max_length=256, verbose_name=_('Serial Number'))
    deviceType = models.CharField(null=True, blank=True, db_index=True, choices=DEVICE_TYPE_CHOICES, max_length=32, verbose_name=_('Device Type'))
    nameSpace = models.CharField(null=True, blank=True, db_index=True, max_length=256, verbose_name=_('Name Space'))

    room = models.ForeignKey(RoomInfo, null=True, blank=True, related_name="devices", on_delete=models.CASCADE)
    workstation = models.ForeignKey(WorkstationInfo, null=True, blank=True, related_name="devices", on_delete=models.CASCADE)
    owner = models.ForeignKey(User, null=True, blank=True, related_name="devices", on_delete=models.CASCADE)

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
