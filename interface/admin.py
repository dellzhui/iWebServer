from django.contrib import admin
from interface.models import RequestRecordInfo


@admin.register(RequestRecordInfo)
class RequestRecordInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'requestUserId', 'requestUsername', 'requestUrl', 'requestMethod', 'requestData', 'responseCode', 'responseContent', 'createTime', 'updateTime')
    search_fields = ('requestUserId', 'requestUsername', 'requestUrl')
    list_filter = ('requestMethod', 'responseCode')
