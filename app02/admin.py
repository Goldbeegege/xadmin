# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from app01 import models

# Register your models here.

class AdminClass(admin.ModelAdmin):
    list_display = ["name","gender"]
admin.site.register(models.Author,AdminClass)
admin.site.register(models.Press)
admin.site.register(models.Book)