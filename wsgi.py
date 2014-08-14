import os, sys, site, django.core.handlers.wsgi

SITE_DIR = '/home/ubuntu/web/www.tcharleshanley.com/app/tomblog'
site.addsitedir(SITE_DIR)
sys.path.append(SITE_DIR)

os.environ['DJANGO_SETTINGS_MODULE'] = 'tomblog.settings'

from django.core.wsgi import get_wsgi_application
from dj_static import Cling

application = Cling(get_wsgi_application())
