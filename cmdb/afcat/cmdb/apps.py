from django.apps import AppConfig


class CmdbConfig(AppConfig):
    name = 'afcat.cmdb'

    def ready(self):
        from afcat.cmdb.packages import cmdbsignals