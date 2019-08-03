from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

class ShLogApphook(CMSApp):
    name = _("Ship's Log Apphook")
    urls = ["shlog.urls"]

apphook_pool.register(ShLogApphook)