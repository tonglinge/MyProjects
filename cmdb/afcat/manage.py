#! /usr/bin/env python
# encoding: utf8
import os
import sys
import re
import pymysql
from afcat import settings


def main(argv=['', 'runserver', '0.0.0.0:8000']):
    pymysql.install_as_MySQLdb()
    match_file = re.compile("initial\.py$")
    argv = argv if len(sys.argv) == 1 else sys.argv
    base_dir = os.path.dirname(os.path.abspath(__file__))
    logs_dir = os.path.join(base_dir, 'logs')
    if not all([os.path.isdir(logs_dir), not os.path.isfile(logs_dir)]):
        os.makedirs(logs_dir)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "afcat.settings")
    try:
        from django.core.management import execute_from_command_line, call_command
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    has_migrate = False
    root_dir = settings.BASE_DIR
    for app in settings.INSTALLED_APPS:
        app = app.split('.')[-1]
        app_dir = os.path.join(root_dir, app)
        if os.path.isdir(app_dir):
            migrations_dir = "%s/%s" % (app_dir, "migrations")
            if os.path.isdir(migrations_dir):
                match = any(map(lambda initial_file: match_file.search(initial_file), os.listdir(migrations_dir)))
                if not match:
                    if not has_migrate:
                        has_migrate = True
                        execute_from_command_line(['afcat_client.py', 'migrate','--database', 'cmdb'])
                    execute_from_command_line(['afcat_client.py', 'makemigrations', app])
    if has_migrate:
        execute_from_command_line(['afcat_client.py', 'migrate'])
    execute_from_command_line(argv)

if __name__ == "__main__":
    main()
