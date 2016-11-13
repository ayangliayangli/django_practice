from django.shortcuts import render, HttpResponse, HttpResponseRedirect
import json, sys, os
from django import forms
from lib import pager
from django.core.exceptions import ValidationError
from . import models
from django.core.urlresolvers import reverse  # reverse name ---> url
from django_practice import settings
from lib import pager

# Create your views here.


# Form block
#
#
#
def phone_validator(phone):
    import re
    ret = re.findall(r"1[3587]\d{9}", str(phone))
    if not ret:
        raise ValidationError("手机号格式不正确")


class SessionRegisterForm(forms.Form):
    user_group_choices = models.UserGroup.objects.all().values_list("id", "name")

    username = forms.CharField(max_length=16, error_messages={"required": "用户名必须填写"})
    password = forms.CharField(max_length=16)
    phone = forms.IntegerField(validators=[phone_validator, ])
    email = forms.EmailField(error_messages={"invalid": "请正确填写邮箱格式"})
    user_group = forms.IntegerField(widget=forms.Select(choices=user_group_choices))

    def __init__(self, *args, **kwargs):
        # 解决新增了用户类型字段,没有及时显示的bug
        # 后来自己写的前端,在view中获取所有的usertype, 不存在这个问题了, 这里留着以后备用
        super(SessionRegisterForm, self).__init__(*args, **kwargs)
        self.fields["user_group"].widget.choices=models.UserGroup.objects.all().values_list("id", "name")


class SessionLoginForm(forms.Form):
    username = forms.CharField(max_length=16, error_messages={"required": "用户名必须填写"})
    password = forms.CharField(max_length=16)


class HostForm(forms.Form):
    hostname = forms.CharField(max_length=32)
    ip = forms.GenericIPAddressField()
    port = forms.IntegerField()
    host_user_name = forms.CharField(max_length=32)
    host_password = forms.CharField(max_length=32)
    # host_key_path = forms.CharField(max_length=128,)
    host_group = forms.IntegerField(widget=forms.Select(choices=()))

    def __init__(self, *args, **kwargs):
        super(HostForm, self).__init__(*args, **kwargs)
        self.fields["host_group"].widget.choices = models.HostGroup.objects.all().values_list("id", "name")


# view block
#
#
def index(request):
    if  request.method == "GET":
        data_to_tpl_dic = {"username":"", }

        username = request.session.get("username", None)
        data_to_tpl_dic["username"] = username

        if username:
            # if user is login , show hosts belong the user
            # handle pager
            item_total = models.Host.objects.filter(user__username=username).all().count()
            item_per_page = 2
            cur_page = int(request.GET.get("cur_page", 1))
            cur_page_start = int(request.GET.get("cur_page_start", 1))
            cur_page_step = 3

            res_pager_dict = pager.get_pager(item_total=item_total,
                                             item_per_page=item_per_page,
                                             cur_page=cur_page,
                                             cur_page_start=cur_page_start,
                                             cur_page_step=cur_page_step,)
            data_to_tpl_dic["pager"] = res_pager_dict

            # slice
            start = res_pager_dict["start"]
            end = res_pager_dict["end"]
            hosts = models.Host.objects.filter(user__username=username).all()[start:end]
            data_to_tpl_dic["hosts"] = hosts

        return render(request, "guanyin/index.html", data_to_tpl_dic)
    else:
        pass


def del_host_relationship_via_hostid(request):
    if  request.method == "POST":
        ret_to_front_dic = {}  # data return to front-end

        host_id = request.POST.get("host_id")
        username = request.session.get("username", None)
        print("---del info:", host_id, username)

        ret_db = models.User.objects.get(username=username).hosts.remove(*[host_id, ])
        print("---ret", ret_db)

        ret_to_front_dic["status"] = True
        return HttpResponse(json.dumps(ret_to_front_dic))


def add_host(request):
    if request.method == "GET":
        # get form
        ret_tpl_dic = {}
        form_get = HostForm()
        ret_tpl_dic["form"] = form_get

        all_host_group = models.HostGroup.objects.all()
        ret_tpl_dic["all_host_group"] = all_host_group

        return render(request, "guanyin/add_host.html", ret_tpl_dic)
    else:
        # post
        # action ---> addhost
        ret_frontend_dict = {"status":False, }
        username = request.session.get("username", "nologin")

        # handle host key file
        host_key_obj = request.FILES.get("host_key_path")
        if host_key_obj:
            host_key_name = host_key_obj.name
            host_key_path = os.path.join(settings.HOST_KEY_DIR, username + "_" + host_key_name)
            host_key_abs_path = os.path.join(settings.BASE_DIR, host_key_path)
            print("---host_key_path", host_key_path)
            with open(host_key_abs_path, "wb") as fp:
                for chunk in host_key_obj.chunks():
                    fp.write(chunk)

        form_post = HostForm(request.POST)
        if form_post.is_valid():
            # form validation is success
            cleaned_data = form_post.cleaned_data
            if host_key_obj:
                cleaned_data["host_key_path"] = host_key_path
            # print("---cleaned_data", type(cleaned_data), cleaned_data)

            # add host in db
            host_group_obj = models.HostGroup.objects.get(pk=cleaned_data["host_group"])
            cleaned_data["host_group"] = host_group_obj
            host_obj = models.Host.objects.create(**cleaned_data)
            models.User.objects.get(username=username).hosts.add(host_obj.id)
            ret_frontend_dict["status"] = True

        else:
            # form validate failure
            errors = json.loads(form_post.errors.as_json())
            print("---errors:", errors)
            ret_frontend_dict["errors"] = errors

        return HttpResponse(json.dumps(ret_frontend_dict))





def logout(request):
    request.session.delete(request.session.session_key)
    view_name = "guanyin:index"
    redirect_url = reverse(view_name)
    print(redirect_url)
    return HttpResponseRedirect(redirect_url)


def session_register(request):
    if request.method == "GET":
        to_tpl_dict = {}  # 传输到template的数据字典
        avatar_path = os.path.join("/", "statics", "img", "avatar", "github_header.jpg")
        to_tpl_dict["avatar"] = avatar_path

        # 获取所有的用户组,供前段选择
        all_user_groups = models.UserGroup.objects.all()
        to_tpl_dict["all_user_groups"] = all_user_groups

        return render(request, "guanyin/session_register.html", to_tpl_dict)
    else:

        # POST METHOD
        ret_frontend_dict = {"status": False,}
        avatar_path = os.path.join("/", "statics", "img", "avatar", "github_header.jpg")
        ret_frontend_dict["avatar"] = avatar_path

        # post 提交数据

        # handle avatar pic first
        username = request.POST.get("username")
        upload_file_obj = request.FILES.get("img")
        if upload_file_obj:
            # 当传了大头贴过来的时候才处理
            upload_file_path = os.path.join("statics", "img", "avatar", username + upload_file_obj.name)
            with open(upload_file_path, "wb") as fp:
                for chunk in upload_file_obj.chunks():
                    fp.write(chunk)
            avatar_path = os.path.join("/", upload_file_path)  # 更新avatar_path
            ret_frontend_dict["avatar"] = avatar_path  # 把头像的路径放在字典中,晚点传到前端

        # handle check_code
        # if checkcode auth is failure, return the result right now
        if request.session.get("check_code").upper() != request.POST.get("check_code").upper():
            ret_frontend_dict["status"] = False
            messages = {"check_code": [{"message": "验证码不正确"}]}
            ret_frontend_dict["messages"] = messages
            return HttpResponse(json.dumps(ret_frontend_dict))

        # handle Form
        form_post = SessionRegisterForm(request.POST)
        form_auth_flag = form_post.is_valid()
        if form_auth_flag:
            # from验证成功
            clean_data = form_post.clean()  # dict
            print("---clean_data:", type(clean_data), clean_data)
            is_user_exist = models.User.objects.filter(username=clean_data.get("username")).count()
            if is_user_exist:
                # user is exist
                exist_flag = True
                ret_frontend_dict["exist_flag"] = exist_flag
                return HttpResponse(json.dumps(ret_frontend_dict))
            else:
                # user is not exist
                # create a user
                # redirect to index html

                # 想通过双下划线来处理外键的问题
                # print("---clean_data", clean_data)
                # clean_data["user_type_id__id"] = clean_data.get("user_type_id", 1)
                # del clean_data["user_type_id"]
                # print("---after clean_data:", clean_data)
                # models.UserInfo.objects.create(**clean_data)

                user_group_obj = models.UserGroup.objects.get(pk=clean_data.get("user_group"))
                clean_data["user_group"] = user_group_obj
                clean_data["avatar_path"] = avatar_path
                # clean_data["avatar_path"] = avatar_path
                models.User.objects.create(**clean_data)  # user_type_id 是一个外键,需要构造一下

                ret_frontend_dict["status"] = True
                return HttpResponse(json.dumps(ret_frontend_dict))
        else:
            # form验证失败
            form_errors_dict = json.loads(form_post.errors.as_json(), encoding="utf-8")
            print("---for_auth_result:", type(form_errors_dict), form_errors_dict)
            ret_frontend_dict["status"] = form_auth_flag
            ret_frontend_dict["messages"] = form_errors_dict

            return HttpResponse(json.dumps(ret_frontend_dict))


def session_login(request):


    if request.method == "GET":
        # data_to_tpl_dic = {}
        # # {form:  db_result: }  db_result{username: , password: , }
        # form_get = SessionLoginForm()
        # data_to_tpl_dic["form"] = form_get
        # print("---session_login. get", )



        return render(request, "guanyin/session_login.html")

    else:
        # POST method
        data_to_front_dict = {"status":False, "errors":{} }
        errors_dict = {}

        print(request.POST, type(request.POST))
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not models.User.objects.filter(username=username).count():
            # user is not exist
            errors_dict["username"] = "用户不存在"
        else:
            # user is exist
            if not models.User.objects.filter(username=username, password=password).count():
                # password is wrong
                errors_dict["password"] = "密码错误"
                pass
            else:
                # password is cerrect
                # login success
                request.session["username"] = username
                data_to_front_dict["status"] = True

        data_to_front_dict["errors"] = errors_dict
        return HttpResponse(json.dumps(data_to_front_dict))


def show_mylog(request):
    data_tpl_dict = {}
    logined_username = request.session.get("username", None)
    data_tpl_dict["username"] = logined_username
    # logs = models.Log.objects.filter(user__username=logined_username)
    # data_tpl_dict["logs"] = logs

    item_total = models.Log.objects.filter(user__username=logined_username).count()
    item_per_page = 6
    cur_page = int(request.GET.get("cur_page", 1))
    cur_page_start = int(request.GET.get("cur_page_start", 1))
    cur_page_step = 3

    res_pager_dict = pager.get_pager(item_total=item_total,
                                     item_per_page=item_per_page,
                                     cur_page=cur_page,
                                     cur_page_start=cur_page_start,
                                     cur_page_step=cur_page_step, )
    data_tpl_dict["pager"] = res_pager_dict

    # slice
    start = res_pager_dict["start"]
    end = res_pager_dict["end"]
    logs = models.Log.objects.filter(user__username=logined_username)[start:end]
    data_tpl_dict["logs"] = logs

    return render(request, "guanyin/log.html", data_tpl_dict)


def resume_yangli(request):
    return render(request, "guanyin/resume_yangli.html")

def my_center(request):
    data_tpl_dict = {}
    logined_username = request.session.get("username", None)
    data_tpl_dict["username"] = logined_username
    myinfo = models.User.objects.get(username=logined_username)
    data_tpl_dict["myinfo"] = myinfo

    print("---avatar_path:", myinfo.avatar_path)

    return render(request, "guanyin/my_center.html", data_tpl_dict)


def get_check_code(request):
    '''
    :param request:
    :return: 一个验证码, 同时把验证码对应的code写入session中
    '''
    import io
    from lib import check_code
    stream = io.BytesIO()
    img, code = check_code.create_validate_code()
    img.save(stream, "png")

    # set check code in session "check_code"
    request.session["check_code"] = code
    # return string , but it is a pic file, browser can show it in img tag
    return HttpResponse(stream.getvalue())


