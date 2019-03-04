# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=64,verbose_name=u"书名")
    summary = models.CharField(max_length=128,verbose_name=u"简介")
    press= models.ForeignKey(to="Press")
    author = models.ManyToManyField(to="Author")

    def __str__(self):
        return self.title

class Press(models.Model):
    name = models.CharField(max_length=64,verbose_name=u"出版社名称")
    addr = models.CharField(max_length=64,verbose_name=u"地址")
    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=64,verbose_name=u"姓名")
    gender = models.BooleanField(verbose_name=u"性别")
    def __str__(self):
        return self.name