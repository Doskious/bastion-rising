from django.contrib import admin
from ehtest.models import *
import ehtest.models
import inspect
from django.db.models.base import ModelBase
from django.contrib.admin.sites import AlreadyRegistered


class defaultListSearch(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields if field.name != "id"]
        self.search_fields = [field.name for field in model._meta.fields if field.name != "id" and not field.rel and not field.get_internal_type() == "DateTimeField"]
        super(defaultListSearch, self).__init__(model, admin_site)


def create_modeladmin(model, adminclass, name=None):
    attrs = {'__module__': '', 'Meta': ''}

    newadmin = type(name, (adminclass,), attrs)
    admin.site.register(model, newadmin)


for name, obj in inspect.getmembers(ehtest.models):
    if inspect.isclass(obj):
        if isinstance(obj, ModelBase):
            if not obj._meta.abstract:
                try:
                    adminname = ''.join((obj._meta.model_name, "Admin"))
                    create_modeladmin(obj, defaultListSearch, adminname)
                except AlreadyRegistered:
                    pass

