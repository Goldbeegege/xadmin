# -*-coding:utf-8-*-
# @author: JinFeng
# @date: 2018/11/14 18:47


from django import template
from django.forms.models import ModelMultipleChoiceField,ModelChoiceField
from django.urls import reverse
from django.utils.safestring import mark_safe


register = template.Library()

@register.simple_tag
def is_pop(bfield):
    tag = ""
    if isinstance(bfield.field,ModelChoiceField) or isinstance(bfield.field,ModelMultipleChoiceField):
        model_obj = bfield.field.queryset.model
        rel_app_name = model_obj._meta.app_label
        rel_model_name = model_obj._meta.model_name
        _url = reverse("%s_%s_add"%(rel_app_name,rel_model_name))
        new_url = _url + "?target=id_%s"%bfield.name
        tag += """<span target=%s class='pop'><i class="fa fa-plus" aria-hidden="true"></i></span>"""%new_url
    return mark_safe(tag)