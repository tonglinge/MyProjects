# coding:utf-8

import os
import sys
import django.core.handlers.wsgi

os.environ['DJANGO_SETTINGS_MODULE'] = 'Server.settings'
os.environ['PYTHON_EGG_CACHE'] = '/tmp/.python-eggs'
current_dir = os.path.dirname(__file__)
if current_dir not in sys.path:
    sys.path.append(current_dir)
application = django.core.handlers.wsgi.WSGIHandler()
django.setup()