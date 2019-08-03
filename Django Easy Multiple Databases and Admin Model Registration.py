## For version-specific data, see:
##  https://docs.djangoproject.com/en/dev/topics/db/multi-db/

# === settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
    'YOUR_APP_DB_NAME_1_db': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
    'YOUR_APP_DB_NAME_2'_db: {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

DATABASE_ROUTERS = ['CORE_APP.db_routers.YOUR_DB_Router_i',
                    'CORE_APP.db_routers.YOUR_DB_Router_ii',]


# === db_routers.py
class YOUR_DB_Router_i(object):
    '''
    DB Router to govorn access to alternate databases
    '''
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'YOUR_APP_DB_NAME_1':
            return 'YOUR_APP_DB_NAME_1_db'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'YOUR_APP_DB_NAME_1':
            return 'YOUR_APP_DB_NAME_1_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'YOUR_APP_DB_NAME_1' or \
           obj2._meta.app_label == 'YOUR_APP_DB_NAME_1':
            return False  # or True if you want to allow it
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth app only appears in the 'auth_db'
        database.
        """
        if app_label == 'YOUR_APP_DB_NAME_1':
            return db == 'YOUR_APP_DB_NAME_1_db'
        return None


class YOUR_DB_Router_ii(object):
    '''
    DB Router to govorn access to alternate databases
    '''
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'YOUR_APP_DB_NAME_2':
            return 'YOUR_APP_DB_NAME_2_db'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'YOUR_APP_DB_NAME_2':
            return 'YOUR_APP_DB_NAME_2_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'YOUR_APP_DB_NAME_2' or \
           obj2._meta.app_label == 'YOUR_APP_DB_NAME_2':
            return False  # or True if you want to allow it
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth app only appears in the 'auth_db'
        database.
        """
        if app_label == 'YOUR_APP_DB_NAME_2':
            return db == 'YOUR_APP_DB_NAME_2_db'
        return None


# === YOUR_APP_DB_NAME_#/admin.py
from django.contrib import admin
from YOUR_APP_DB_NAME.models import *
import YOUR_APP_DB_NAME.models
import inspect
from django.db.models.base import ModelBase
from django.contrib.admin.sites import AlreadyRegistered


class defaultListSearch(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields if field.name != "id"]
        self.search_fields = [field.name for field in model._meta.fields if field.name != "id" and not field.rel and not field.get_internal_type() == "DateTimeField"]
        super(defaultListSearch, self).__init__(model, admin_site)


class MultiDBModelAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields if field.name != "id"]
        self.search_fields = [field.name for field in model._meta.fields if field.name != "id" and not field.rel and not field.get_internal_type() == "DateTimeField"]
        super(MultiDBModelAdmin, self).__init__(model, admin_site)

    # A handy constant for the name of the alternate database.
    using = 'YOUR_APP_DB_NAME'

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super(MultiDBModelAdmin, self).get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super(MultiDBModelAdmin, self).formfield_for_foreignkey(
            db_field, request=request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super(MultiDBModelAdmin, self).formfield_for_manytomany(
            db_field, request=request, using=self.using, **kwargs)


def create_modeladmin(model, adminclass, name=None):
    attrs = {'__module__': '', 'Meta': ''}

    newadmin = type(name, (adminclass,), attrs)
    admin.site.register(model, newadmin)


for name, obj in inspect.getmembers(YOUR_APP_DB_NAME.models):
    if inspect.isclass(obj):
        if isinstance(obj, ModelBase):
            if not obj._meta.abstract:
                if obj._meta.app_label is not "YOUR_APP_DB_NAME":
                    pass
                else:
                    try:
                        admin.site.register(obj, MultiDBModelAdmin)
                    except AlreadyRegistered:
                        pass


# === CORE_APP/admin.py
from django.contrib import admin
from CORE_APP.models import *
import CORE_APP.models
from CORE_APP.report_ugrad import ugradRow
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


for name, obj in inspect.getmembers(CORE_APP.models):
    if inspect.isclass(obj):
        if isinstance(obj, ModelBase):
            if not obj._meta.abstract:
                try:
                    adminname = ''.join((obj._meta.model_name, "Admin"))
                    create_modeladmin(obj, defaultListSearch, adminname)
                except AlreadyRegistered:
                    pass
