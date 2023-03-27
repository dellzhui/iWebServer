import datetime
import json
from json import JSONEncoder
from django.db import models
from django.db.models.base import ModelState
from django.utils.translation import gettext as _

# Create your models here.


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
