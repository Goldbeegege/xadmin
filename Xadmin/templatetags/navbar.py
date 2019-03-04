# -*-coding:utf-8-*-
# @author: JinFeng
# @date: 2018/11/12 20:46

from django import template
import re
from django.utils.safestring import mark_safe
register = template.Library()

@register.simple_tag
def generate_navbar(request,self):

    re_list = re.findall(r"\w+",request.path_info)
    if re.match(r"\d+",re_list[-1]):
        re_list = re_list[:-1]
    temp = """<ol class="breadcrumb">
                    <li><a href="/%s/">Home</a></li>
                """ % (re_list[0])
    if len(re_list) > 2:
        for i,j in enumerate(re_list[1:-1]):
            i += 2
            href = "%s/"*i
            href = href%(tuple(re_list[:i]))
            temp += '<li><a href="/%s">%s</a></li>'%(href,j)

    temp += '<li class="active">%s</li></ol>'%(re_list[-1])
    return mark_safe(temp)