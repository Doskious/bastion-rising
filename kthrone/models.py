from __future__ import unicode_literals

from django.db import models
from stdimage.models import StdImageField
from stdimage.utils import UploadToAutoSlugClassNameDir


class NonPlayerCharacter(models.Model):
    name = models.CharField(max_length=250)
    image = models.ImageField(max_length=255)

    class Meta:
        verbose_name='NPC'
        verbose_name_plural = "NPCs"

    def __unicode__(self):
        return u'{0}'.format(self.name)
