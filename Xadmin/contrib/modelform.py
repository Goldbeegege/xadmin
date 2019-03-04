# -*-coding:utf-8-*-
# @author: JinFeng
# @date: 2018/11/6 18:33

from django.forms import ModelForm

def create_model_form(model_name):
    class Meta:
        model=model_name
        fields="__all__"

    def __new__(cls, *args, **kwargs):
        for field in cls.base_fields:
            form_field = cls.base_fields[field]
            form_field.widget.attrs.update({"class":"form-control"})
        return ModelForm.__new__(cls)

    dynamic_form = type("CustomForm",(ModelForm,),{"Meta":Meta,"__new__":__new__})
    return dynamic_form
        
