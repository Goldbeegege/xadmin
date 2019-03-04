# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig
from django.conf import settings


class XadminConfig(AppConfig):
    name = 'Xadmin'
    def ready(self):
        for app_config_path in settings.INSTALLED_APPS:
            app_name = app_config_path.split(".",1)[0]
            try:
                module_path = app_name + ".xadmin"
                module_obj = __import__(module_path).xadmin
            except Exception as e:
                pass
