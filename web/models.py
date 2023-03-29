from django.contrib.auth.models import User
from django.db import models
from interface.datatype.config import iWebServerBaseConfig
from interface.models import ModelCommonInfo
from django.utils.translation import gettext as _


class WorkstationInfo(ModelCommonInfo):
    class Meta:
        verbose_name = _('WorkstationInfo')
        verbose_name_plural = _('WorkstationInfo')
        permissions = (
            (iWebServerBaseConfig.IWEBSERVER_PERMISSION_WORKSTATION_ACCESS, 'can access workstation'),
        )

    name = models.CharField(null=True, blank=True, db_index=True, max_length=256, verbose_name=_('Workstation Name'))

    owner = models.ForeignKey(User, null=True, blank=True, related_name="workstations", on_delete=models.CASCADE)


class RoomInfo(ModelCommonInfo):
    class Meta:
        verbose_name = _('RoomInfo')
        verbose_name_plural = _('RoomInfo')
        permissions = (
            (iWebServerBaseConfig.IWEBSERVER_PERMISSION_ROOM_ACCESS, 'can access room'),
        )

    name = models.CharField(null=True, blank=True, db_index=True, max_length=256, verbose_name=_('Room Name'))
    roomId = models.BigIntegerField(null=True, blank=True, db_index=True, verbose_name=_('Room Id'))
    roomJoinPin = models.BigIntegerField(null=True, blank=True, db_index=True, verbose_name=_('Room Join Pin'))

    owner = models.ForeignKey(User, null=True, blank=True, related_name="rooms", on_delete=models.CASCADE)
