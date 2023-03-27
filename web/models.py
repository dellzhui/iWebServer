from django.db import models
from django.utils.translation import gettext as _
from interface.models import ModelCommonInfo


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
            ('all_access', 'can access all '),
            ('regular_access', 'can access regular ')
        )
