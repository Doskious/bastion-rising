from __future__ import absolute_import
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

