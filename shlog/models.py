from django.db import models
from django.utils import timezone
from cms.models.pluginmodel import CMSPlugin


class Hello(CMSPlugin):
    guest_name = models.CharField(max_length=50, default='Stranger')

    def __unicode__(self):
        return u'{0}'.format(self.guest_name)


class AssociatedCampaign(models.Model):
    name = models.CharField(max_length=250)

    def __unicode__(self):
        return u'{0}'.format(self.name)


class CharacterStatus(models.Model):
    status = models.CharField(max_length=16)

    class Meta:
            verbose_name_plural = "character statuses"

    def __unicode__(self):
        return u'{0}'.format(self.status)


class JournalAuthor(models.Model):
    name = models.CharField(max_length=128)
    kind = models.ForeignKey('CharacterStatus', default=2)

    def __unicode__(self):
        return u'{0}'.format(self.name)


class SectionGroup(models.Model):
    group_name = models.CharField(max_length=128)
    for_campaign = models.ForeignKey('AssociatedCampaign', default=1)

    def __unicode__(self):
        return u'{0}'.format(self.group_name)


class JournalSection(models.Model):
    journal_section = models.CharField(max_length=128)
    section_group = models.ForeignKey('SectionGroup')

    def __unicode__(self):
        return u'{0}'.format(self.journal_section)


class JournalEntry(models.Model):
    author = models.ForeignKey('JournalAuthor')
    title = models.CharField(max_length=60)
    subtext = models.CharField(max_length=42, default="", blank=True)
    context = models.CharField(max_length=128, default="Ship's Log: The Allegiance", blank=True)
    section = models.ForeignKey('JournalSection')
    journal_date = models.CharField(max_length=10, default="4715/MM/DD")
    body = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    class Meta:
            verbose_name_plural = "journal entries"

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __unicode__(self):
        return u'{0}'.format(self.title)

