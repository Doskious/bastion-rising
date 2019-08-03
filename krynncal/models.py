from __future__ import unicode_literals
from django.db import models
from krynncal.krynndateparse import parse_datetime


class CampaignDate(models.Model):
	date_str = models.CharField(max_length=20)

	@property
	def current_date(self):
		return parse_datetime(self.date_str)

	def __unicode__(self):
		return self.current_date.ctime()
