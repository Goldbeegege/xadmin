# -*-coding:utf-8-*-
# @author: JinFeng
# @date: 2018/10/30 19:53
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from django.conf.urls import url
from django.shortcuts import HttpResponse,render,redirect
from django.utils.safestring import mark_safe
from modelform import create_model_form
from paginator import XadminPagintor
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
import copy
from urllib import urlencode
from django.db.models import ManyToManyField


class BaseAdmin(object):

    def bacth_delete(self,request, queryset):
        for query in  queryset:
            query.delete()
        return True

    list_display = []
    list_display_links = []
    search_fields = []
    default_action_list = [bacth_delete]
    action_list = []
    bacth_delete.desc = "批量删除"
    filter_list = []


    def __init__(self,model):
        self.model = model
        self.app_name = self.model._meta.app_label
        self.model_name = self.model._meta.model_name

    @property
    def get_table_header(self):
        self.header_list = []
        if self.list_display:
            #获取表头信息
            for field in self.list_display:
                if callable(field):
                    self.header_list.append(field(self))
                else:
                    self.header_list.append(field)
        else:
            self.list_display.append(self.model_name)
            self.header_list += self.list_display
        return self.header_list

    def get_table_body(self,obj):
        body_list = []
        tag = "<a class='pk' pk='%s' href='/xadmin/%s/%s/change/%s/'>%s</>"
        for field in self.list_display:
            if callable(field):
                body_list.append(field(self,obj=obj,header=False))
            else:
                try:
                    val = getattr(obj,field)
                    body_list.append(val)
                except AttributeError as e:
                    body_list.append(obj.__str__())
        if not self.list_display_links:
            body_list[0] = mark_safe(tag%(obj.pk,self.app_name,self.model_name,obj.pk,body_list[0]))
        else:
            for link in self.list_display_links:
                index = self.header_list.index(link)
                body_list[index] = mark_safe(tag%(obj.pk,self.app_name,self.model_name,obj.pk,body_list[index]))
        return body_list


    def get_page(self,request,model_list,body_list):
        """
        处理分页信息
        :param request:
        :return:
        """
        page = request.GET.get("page", 1)
        total_length = model_list.count()
        pg = XadminPagintor(total_length=total_length, amount_per_page=3,current_page=page)
        current_page = pg.current_page
        num_range = pg.page_num()
        start, end = pg.content_range()
        self.display_body_list = body_list[start:end]
        return current_page,num_range,pg.total_page

    def generate_page_html(self,request,model_list,body):
        """
        生成分页的html
        :param request:
        :param model_list:
        :param body:
        :return:
        """
        current_page, num_range,total_page = self.get_page(request,model_list,body)
        params = copy.deepcopy(request.GET)
        temp = ""
        for page in num_range:
            params["page"] =page
            if page == current_page:
                temp += "<li class='active' pk='%s'><a href='?%s'>%s</a></li>"%(page,params.urlencode(),page)
            else:
                temp += "<li pk='%s'><a href='?%s'>%s</a></li>" % (page,params.urlencode(), page)
        return mark_safe(temp),total_page,current_page

    def search_func(self,request):
        q = Q()
        q.connector = "or"
        self.key_word = request.GET.get("kw","")
        if self.search_fields:
            for field in self.search_fields:
                q.children.append((field+"__contains",self.key_word))
        return q


    @property
    def action(self):
        if self.action_list:
            self.default_action_list.extend(self.action_list)
        new_action_list = []
        for action in self.default_action_list:
            try:
                nick_name = action.desc
            except Exception as e:
                nick_name = action.__name__

            new_action_list.append({"name":action.__name__,"nick_name":nick_name})
        return new_action_list

    def filter_func(self,request):
        params = copy.deepcopy(request.GET)
        if params.get("page"):del params["page"]
        if self.filter_list:
            fc_temp = {}
            for field in self.filter_list:
                field_obj = self.model._meta.get_field(field)
                try:
                    rel_obj = field_obj.rel.to.objects.all()
                    each = self.get_related_html(field,params,rel_obj )
                    fc_temp[field] = each
                except Exception as e:
                    print e
                    raise Exception("%s has no related objects"%field_obj)
            return fc_temp

    def get_related_html(self,field,params,rels=None):
        temp = []
        fc = params.get(field + "_id","")
        if not fc:
            temp.append(mark_safe("<a class='active' href='?%s'>%s</a>" % (urlencode(params), "ALL")))
        else:
            del params[field + "_id"]
            temp.append(mark_safe("<a href='?%s'>%s</a>" % (urlencode(params), "ALL")))
        for rel in rels:
            if str(rel.id) == str(fc):
                cls="class='active'"
            else:
                cls =""
            params.update({field + "_id":rel.id})
            href = urlencode(params)
            temp.append(mark_safe("<a %s href='?%s'>%s</a>" % (cls,href, rel)))
        params[field + "_id"] = fc
        return temp

    def filter_new_func(self,request):
        params = copy.deepcopy(request.GET)
        q = Q()
        for param in params:
            if param.endswith("_id"):
                re_param = param.split("_",1)[0]
                field_obj = self.model._meta.get_field(re_param)
                if params[param]:
                    pid = params[param]
                    if isinstance(field_obj,ManyToManyField):
                        param = re_param
                    q.children.append((param,pid))
                else:
                    continue

        return q

    @csrf_exempt
    def view(self,request):
        # action
        new_action_list = self.action
        if request.method == "GET":
            # 搜索
            conditions = self.search_func(request)
            model_list = self.model.objects.filter(conditions)
            #过滤
            filter_conditions = self.filter_func(request)
            model_conditions = self.filter_new_func(request)
            model_list = model_list.filter(model_conditions).all()
            header_list = self.get_table_header
            body_list = []
            for obj in model_list:
                ret = self.get_table_body(obj)
                body_list.append(ret)
            #分页
            temp, total_page,current_page = self.generate_page_html(request,model_list,body_list)
        elif request.method == "POST":
            action = request.POST.get("action")
            pk_list = json.loads(request.POST.get("pk_list"))
            queryset = []
            for pk in pk_list:
                pk_obj = self.model.objects.filter(id=pk).first()
                queryset.append(pk_obj)
            func = getattr(self,action)
            if func(request,queryset):
                return JsonResponse({"status":True})

        return render(request, "view.html", locals())

    def add(self,request):
        form_obj = create_model_form(self.model)
        if request.method == "POST":
            form_obj = form_obj(request.POST)
            if form_obj.is_valid():
                obj = form_obj.save()
                target = request.GET.get("target","")
                if target:
                    val = obj.id
                    text = str(obj)
                    return render(request,"temp.html",locals())
                return redirect("/xadmin/{}/{}/".format(self.app_name,self.model_name))
        return render(request, "add.html",locals())

    def change(self,request,nid):
        instance = self.model.objects.filter(id=nid).first()
        form = create_model_form(self.model)
        form_obj = form(instance=instance)
        if request.method == "POST":
            form_obj = form(instance=instance,data=request.POST)
            if form_obj.is_valid():
                form_obj.save()
                return redirect("/xadmin/{}/{}/".format(self.app_name,self.model_name))
            else:
                return render(request, "add.html", locals())
        return render(request, "add.html",locals())

    def delete(self,request,nid):
        del_obj = self.model.objects.filter(id=nid).first()
        if request.method == "POST":
            del_obj.delete()
            return redirect("/xadmin/{}/{}/".format(self.app_name,self.model_name))
        return render(request, "delete.html",locals())

    def get_next_urls(self):
        next_url_list = [
            url(r"^$", self.view),
            url(r"^add/$", self.add,name="%s_%s_add"%(self.app_name,self.model_name)),
            url(r"^change/(\d+)/$", self.change),
            url(r"^delete/(\d+)/$", self.delete)
        ]
        return next_url_list

    @property
    def next_urls(self):
        return self.get_next_urls(),None,None

class AdminSite(object):
    def __init__(self):
        self.enable_apps = {}

    def get_urls(self):
        url_list = []
        for each in self.enable_apps.values():
            for model_name,admin_class in each.items():
                app_name = admin_class.model._meta.app_label
                _url = url(r"%s/%s/"%(app_name,model_name),admin_class.next_urls)
                url_list.append(_url)
        return url_list

    @property
    def urls(self):
        return self.get_urls(),None,None

    def register(self,model,admin_class=None):
        app_name = model._meta.app_label
        if app_name not in self.enable_apps:
            self.enable_apps[app_name] = {}
        if not admin_class:
            admin_class = BaseAdmin
        model_name = model._meta.model_name
        self.enable_apps[app_name][model_name] = admin_class(model)
        admin_class.model = model

site = AdminSite()

def show(request,*args,**kwargs):
    table_dict = site.enable_apps
    if args[0]:
        new_table = {args[0]:table_dict[args[0]]}
    else:
        new_table = table_dict
    return render(request,"show_all.html",locals())
