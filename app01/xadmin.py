# -*-coding:utf-8-*-
# @author: JinFeng
# @date: 2018/10/30 19:37


from Xadmin.contrib.xadmin import site
from Xadmin.contrib.xadmin import BaseAdmin
import models


class AuthorClass(BaseAdmin):
    list_display = ["id","name"]
    list_display_links = ["name"]

class BookClass(BaseAdmin):
    list_display = ["id","title","summary","press"]
    search_fields = ["title","summary"]
    filter_list = ["press","author"]





site.register(models.Author,AuthorClass)
site.register(models.Press)
site.register(models.Book,BookClass)