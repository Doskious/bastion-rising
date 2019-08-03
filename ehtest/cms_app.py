from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

class EndlessHallsApphook(CMSApp):
    name = _("Endless Halls Apphook")
    urls = ["ehtest.urls"]

apphook_pool.register(EndlessHallsApphook)