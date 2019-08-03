from __future__ import unicode_literals
from krynncal import krynndatetime as datetime
from krynncal.krynndateparse import (
    parse_date, parse_datetime, parse_time,
)
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.forms.fields import BaseTemporalField
from django.forms.widgets import DateTimeInput
from django.utils import formats


class KrynnDateTimeFormField(BaseTemporalField):
    widget = DateTimeInput
    input_formats = formats.get_format_lazy('DATETIME_INPUT_FORMATS')
    default_error_messages = {
        'invalid': _('Enter a valid date/time.'),
    }

    def prepare_value(self, value):
        return value

    def to_python(self, value):
        """
        Validates that the input can be converted to a datetime. Returns a
        Python datetime.datetime object.
        """
        if value in self.empty_values:
            return None
        if isinstance(value, datetime.datetime):
            return from_current_timezone(value)
        if isinstance(value, datetime.date):
            return datetime.datetime(value.year, value.month, value.day)
        if isinstance(value, list):
            # Input comes from a SplitDateTimeWidget, for example. So, it's two
            # components: date and time.
            if len(value) != 2:
                raise ValidationError(self.error_messages['invalid'], code='invalid')
            if value[0] in self.empty_values and value[1] in self.empty_values:
                return None
            value = '%s %s' % tuple(value)
        result = super(KrynnDateTimeFormField, self).to_python(value)
        return result

    def strptime(self, value, format):
        return datetime.datetime.strptime(force_str(value), format)


class KrynnDateTimeField(models.DateTimeField):
    default_error_messages = {
        'invalid': _("'%(value)s' value has an invalid format. It must be in "
                     "YYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ] format."),
        'invalid_date': _("'%(value)s' value has the correct format "
                          "(YYY-MM-DD) but it is an invalid date."),
        'invalid_datetime': _("'%(value)s' value has the correct format "
                              "(YYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]) "
                              "but it is an invalid date/time."),
    }
    description = _("Krynn Date (with time)")

    # __init__ is inherited from DateField, and is fine.

    def db_type(self, connection):
        return 'char(20)'

    def _check_fix_default_value(self):
        """
        Adds a warning to the checks framework stating, that using an actual
        date or datetime value is probably wrong; it's only being evaluated on
        server start-up.

        For details see ticket #21905
        """
        return []

    def get_internal_type(self):
        return "KrynnDateTimeField"

    def to_python(self, value):
        if value is None:
            return value
        if isinstance(value, datetime.datetime):
            return value
        if isinstance(value, datetime.date):
            return datetime.datetime(value.year, value.month, value.day)

        try:
            parsed = parse_datetime(value)
            if parsed is not None:
                return parsed
        except ValueError:
            raise exceptions.ValidationError(
                self.error_messages['invalid_datetime'],
                code='invalid_datetime',
                params={'value': value},
            )

        try:
            parsed = parse_date(value)
            if parsed is not None:
                return datetime.datetime(parsed.year, parsed.month, parsed.day)
        except ValueError:
            raise exceptions.ValidationError(
                self.error_messages['invalid_date'],
                code='invalid_date',
                params={'value': value},
            )

        raise exceptions.ValidationError(
            self.error_messages['invalid'],
            code='invalid',
            params={'value': value},
        )

    def pre_save(self, model_instance, add):
        return super(KrynnDateTimeField, self).pre_save(model_instance, add)

    # contribute_to_class is inherited from DateField, it registers
    # get_next_by_FOO and get_prev_by_FOO

    # get_prep_lookup is inherited from DateField

    def get_prep_value(self, value):
        value = super(KrynnDateTimeField, self).get_prep_value(value)
        value = self.to_python(value)
        return value

    def get_db_prep_value(self, value, connection, prepared=False):
        # Casts datetimes into the format expected by the backend
        if not prepared:
            value = self.get_prep_value(value)
        return connection.ops.adapt_datetimefield_value(value)

    def value_to_string(self, obj):
        val = self.value_from_object(obj)
        return '' if val is None else val.isoformat()

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.CharField}
        defaults.update(kwargs)
        return super(KrynnDateTimeField, self).formfield(**defaults)


