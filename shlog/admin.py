from django.contrib import admin
from .models import JournalEntry, JournalSection, SectionGroup, JournalAuthor, CharacterStatus, AssociatedCampaign


admin.site.register(JournalEntry)
admin.site.register(JournalSection)
admin.site.register(SectionGroup)
admin.site.register(JournalAuthor)
admin.site.register(CharacterStatus)
admin.site.register(AssociatedCampaign)
