import datetime
import json
from json import JSONEncoder
from django.db import models
from django.db.models.base import ModelState
from django.utils.translation import gettext as _
from interface.datatype.config import iWebServerBaseConfig


class IdmsModelEncoder(JSONEncoder):
    def default(self, value):
        try:
            if (isinstance(value, datetime.datetime)):
                return '{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}.{:03d}'.format(value.year, value.month, value.day, value.hour, value.minute, value.minute, int(value.microsecond / 1000))
            if (isinstance(value, ModelState)):
                return ''
            return value.__dict__
        except Exception:
            return None


class ModelCommonInfo(models.Model):
    class Meta:
        abstract = True

    createTime = models.DateTimeField(null=True, blank=True, auto_now_add=True, verbose_name=_('Create Time'))
    updateTime = models.DateTimeField(null=True, blank=True, auto_now=True, verbose_name=_('Update Time'))

    def to_json(self):
        try:
            return json.dumps(self, cls=IdmsModelEncoder)
        except Exception:
            return None

    def to_dict(self):
        try:
            return json.loads(self.to_json())
        except Exception:
            return None

    def from_json(self, json_str):
        try:
            self.from_dict(json.loads(json_str))
        except Exception:
            return

    def from_dict(self, info):
        try:
            for key, value in info.items():
                if isinstance(value, (list, tuple)):
                    setattr(self, key, [ModelCommonInfo(x) if isinstance(x, dict) else x for x in value])
                else:
                    setattr(self, key, ModelCommonInfo(value) if isinstance(value, dict) else value)
        except Exception:
            return


class UserControl(ModelCommonInfo):
    Name = models.CharField(null=True, max_length=255)
    Desc = models.CharField(null=True, max_length=256)
    AreaName = models.CharField(null=True, max_length=256)
    Config = models.CharField(null=True, max_length=2048)
    Level = models.IntegerField(null=True, default=1)

    super_control = models.ForeignKey('self', null=True, blank=True, related_name='subs', on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('UserControl')
        verbose_name_plural = _('UserControl')
        permissions = (
            (iWebServerBaseConfig.IWEBSERVER_PERMISSION_ADMIN_ACCESS, 'can access all '),
            (iWebServerBaseConfig.IWEBSERVER_PERMISSION_REGULAR_ACCESS, 'can access regular ')
        )


class RequestRecordInfo(ModelCommonInfo):
    requestUserId = models.BigIntegerField(null=True, blank=True, db_index=True, verbose_name=_('Request UserId'))
    requestUsername = models.CharField(null=True, blank=True, max_length=256, verbose_name=_('Request UserName'))
    requestUrl = models.CharField(null=True, blank=True, max_length=2048, verbose_name=_('Request Url'))
    requestMethod = models.CharField(null=True, blank=True, db_index=True, max_length=16, verbose_name=_('Request Method'))
    requestData = models.TextField(null=True, blank=True, verbose_name=_('Request Data'))
    responseCode = models.IntegerField(null=True, blank=True, verbose_name=_('Response Code'))
    responseContent = models.TextField(null=True, blank=True, verbose_name=_('Response Content'))

    def from_request_and_response(self, request, response):
        if (request != None):
            self.requestUserId = request.user.id
            self.requestUsername = request.user.username
            self.requestUrl = '{}{}'.format(request.META["PATH_INFO"], f'?{request.META["QUERY_STRING"]}' if (request.META["QUERY_STRING"] != '') else '')
            self.requestMethod = request.method
            self.requestData = json.dumps(request.data) if (isinstance(request.data, dict)) else str(request.data)

        if (response != None):
            self.responseCode = response.status_code
            self.responseContent = response.content.decode('utf-8') if (isinstance(response.content, bytes)) else str(response.content)
