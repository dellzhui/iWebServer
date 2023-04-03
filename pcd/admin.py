from django.contrib import admin
from pcd.models import WorkstationInfo, RoomInfo, DeviceInfo


@admin.register(WorkstationInfo)
class WorkstationInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner', 'createTime', 'updateTime')
    search_fields = ('name',)
    list_filter = ('owner',)


@admin.register(RoomInfo)
class RoomInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'roomId', 'roomJoinPin', 'isPrivate', 'workstation', 'owner', 'createTime', 'updateTime')
    search_fields = ('name', 'roomId')
    list_filter = ('owner', 'workstation')


@admin.register(DeviceInfo)
class DeviceInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'macAddress', 'productKey', 'deviceName', 'deviceSecret', 'serialNumber', 'deviceType', 'nameSpace', 'owner', 'room', 'workstation', 'createTime', 'updateTime')
    search_fields = ('macAddress', 'deviceName')
    list_filter = ('deviceType', 'owner', 'room', 'workstation')
