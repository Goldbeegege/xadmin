# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Fruit(models.Model):
    name = models.CharField(max_length=64, verbose_name=u"名字")
    origin = models.CharField(max_length=128, verbose_name=u"产地")
