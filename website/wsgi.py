"""
WSGI config for website project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import sys
import os

app_name = 'website'
app_dir = os.path.dirname(__file__)
env_name = '/home/doskious/.virtualenvs/newallegiance'
sys.path.append(app_dir)
sys.path.append("/".join((app_dir, app_name)))

INTERP = env_name + "/bin/python"
# INTERP is present twice so the target interpreter knows the actual executable path
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

sys.path.insert(0, env_name + '/bin')
sys.path.insert(0, env_name + '/lib/python2.7/site-packages/django')
sys.path.insert(0, env_name + '/lib/python2.7/site-packages')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")

from django.conf import settings

packages = settings.INSTALLED_APPS
for package in packages:
    if "." not in package:
        sys.path.insert(0, env_name + '/lib/python2.7/site-packages' + package)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

