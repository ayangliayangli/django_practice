from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.core.exceptions import ValidationError
from chouti_like import models
from django import forms
from lib import pager
import json,os

# Create your views here.


def phone_validator(phone):
    import re
    ret = re.findall(r"1[3587]\d{9}", str(phone))
    if not ret:
        raise ValidationError("手机号格式不正确")


class SessionRegisterForm(forms.Form):
    user_type_choices = models.UserType.objects.all().values_list("id", "caption")

    username = forms.CharField(max_length=16, error_messages={"required":"用户名必须填写"})
    password = forms.CharField(max_length=16)
    phone = forms.IntegerField(validators=[phone_validator, ])
    email = forms.EmailField(error_messages={"invalid":"请正确填写邮箱格式"})
    user_type_id = forms.IntegerField(widget=forms.Select(choices=user_type_choices))

    def __init__(self, *args, **kwargs):
        # 解决新增了用户类型字段,没有及时显示的bug
        # 后来自己写的前端,在view中获取所有的usertype, 不存在这个问题了, 这里留着以后备用
        super(SessionRegisterForm, self).__init__(*args, **kwargs)
        self.fields["user_type_id"].widget.choices=models.UserType.objects.all().values_list("id", "caption")


class SessionLoginForm(forms.Form):
    username = forms.CharField(max_length=16)
    password = forms.CharField(max_length=16)


def session_login(request):
    if request.method == "GET":
        form_get = SessionLoginForm()
        return render(request, "chouti_like/session_login.html", {"form":form_get})
    else:
        form_post = SessionLoginForm(request.POST)
        is_valid_flag = form_post.is_valid()

        if is_valid_flag:
            # backend form auth sucess
            # start auth username and password is cerrect or not

            # 前端提交过来的数据,已经通过form验证
            clean_data = form_post.clean()  # dict {username:xxx, password:xxx}
            # 数据库信息比对结果
            data_to_tpl = {"status": False, "username": "", "password": ""}

            user_from_db = models.UserInfo.objects.filter(username=clean_data.get("username", None)).first()
            if user_from_db:
                # user exist
                if user_from_db.password != clean_data.get("password", None):
                    # password is wrong
                    data_to_tpl["password"] = "密码错误"
                else:
                    # password is right
                    # login success
                    # set session
                    request.session["username"] = clean_data.get("username")
                    return HttpResponseRedirect("/chouti_like/index/")
            else:
                # user is not exist
                data_to_tpl["username"] = "用户名不存在"
            return render(request, "chouti_like/session_login.html", {"form": form_post, "data":data_to_tpl})
        else:
            # backend form auth failure
            return render(request, "chouti_like/session_login.html", {"form": form_post})


def session_logout(request):
    request.session.delete(request.session.session_key)
    return HttpResponseRedirect("/chouti_like/index/")


def session_register(request):
    if request.method == "GET":
        user_type_all_list = models.UserType.objects.all()
        return render(request, "chouti_like/session_register.html", {"user_types":user_type_all_list})
    else:
        # post 提交数据

        # handle avatar pic first
        upload_file_obj = request.FILES.get("img")
        if upload_file_obj:
            # 当传了大头贴过来的时候才处理
            upload_file_path_name = os.path.join("statics", "img", "avatar", upload_file_obj.name)
            with open(upload_file_path_name, "wb") as fp:
                for chunk in upload_file_obj.chunks():
                    fp.write(chunk)

        # handle check_code
        if request.session.get("check_code").upper() != request.POST.get("check_code").upper():
            ret_data_dic = {}
            ret_data_dic["status"] = False
            messages = {"check_code":[{"message":"验证码不正确"}]}
            ret_data_dic["messages"] = messages
            return HttpResponse(json.dumps(ret_data_dic))

        form_post = SessionRegisterForm(request.POST)
        form_auth_flag = form_post.is_valid()
        if form_auth_flag:
            # from验证成功
            clean_data = form_post.clean()  # dict
            print("---clean_data:",type(clean_data) , clean_data)
            is_user_exist = models.UserInfo.objects.filter(username=clean_data.get("username")).count()
            if is_user_exist:
                # user is exist
                exist_flag = True
                ret_data_dic = {}
                ret_data_dic["exist_flag"] = exist_flag
                if upload_file_obj:
                    ret_data_dic["avatar"] = "/" + upload_file_path_name
                return HttpResponse(json.dumps(ret_data_dic))
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

                user_type_obj = models.UserType.objects.get(pk=clean_data.get("user_type_id"))
                clean_data["user_type_id"] = user_type_obj
                models.UserInfo.objects.create(**clean_data)  # user_type_id 是一个外键,需要构造一下

                # add session
                request.session["username"] = clean_data.get("username")

                ret_data_dic = {}
                ret_data_dic["status"] = True
                return HttpResponse(json.dumps(ret_data_dic))
        else:
            # form验证失败
            res_post_dict = {}

            form_errors_dict = json.loads(form_post.errors.as_json(), encoding="utf-8")
            print("---for_auth_result:", type(form_errors_dict), form_errors_dict)
            res_post_dict["status"] = form_auth_flag
            res_post_dict["messages"] = form_errors_dict

            if upload_file_obj:
                res_post_dict["avatar"] = "/" + upload_file_path_name

            return HttpResponse(json.dumps(res_post_dict))



def index(request):
    print("---in view.index")
    username = request.session.get("username", None)
    return render(request, "chouti_like/index.html", {"username":username})


def show_user_types(request):
    username = request.session.get("username", None)  # 登录用户名,传到前端

    item_total = models.UserType.objects.all().count()
    item_per_page = 10
    cur_page = int(request.GET.get("cur_page", 1))
    cur_page_start = int(request.GET.get("cur_page_start", 1))
    cur_page_step = 5

    # 使用库,直接计算出当前分页的所有信息
    res_page_info_dic = pager.get_pager(item_total,
                                   item_per_page=item_per_page,
                                   cur_page=cur_page,
                                   cur_page_start=cur_page_start,
                                   cur_page_step=cur_page_step,)
    print("-----", int(res_page_info_dic["start"]), int(res_page_info_dic["end"]))
    ret_data = models.UserType.objects.all()[res_page_info_dic["start"]:res_page_info_dic["end"]]
    print("----", ret_data)
    cur_page = res_page_info_dic["cur_page"]
    cur_page_start = res_page_info_dic["cur_page_start"]
    cur_page_stop = res_page_info_dic["cur_page_stop"]
    page_total = res_page_info_dic["page_total"]
    cur_page_range = range(cur_page_start, cur_page_stop+1)

    pre_page = cur_page_start - 1
    post_page = cur_page_stop + 1

    # 修正上一页,下一页
    if pre_page < 1:
        pre_page = None
    if post_page > page_total:
        post_page = None

    return render(request, "chouti_like/show_user_types.html", {"username":username,
                                                                "ret_data":ret_data,
                                                                "cur_page_range":cur_page_range,
                                                                "cur_page":cur_page,
                                                                "pre_page":pre_page,
                                                                "post_page":post_page,
                                                                "cur_page_start":cur_page_start,
                                                                "cur_page_stop":cur_page_stop,
                                                                })


def show_my_info(request):
    username = request.session.get("username", None)
    my_info = models.UserInfo.objects.filter(username=username).first()

    hobbys = my_info.hobby.all()
    all_hobbys = models.Hobby.objects.all()
    print("---debug:", type(hobbys),"+++", hobbys)

    data_to_tpl = {"my_info":my_info,"hobbys":hobbys, "all_hobbys":all_hobbys, "username":username }
    return render(request, "chouti_like/show_my_info.html", data_to_tpl)


def delete_this_hobby(request):
    username = request.session.get("username")
    hobbys = request.POST.get("hobbys", None)
    hobbys_list = json.loads(hobbys)
    print("---hobbys type:", type(hobbys_list), "+++", hobbys_list)
    ret_data_dict = {"status":False}
    if hobbys:
        user_obj = models.UserInfo.objects.get(username=username)
        user_obj.hobby.clear()
        user_obj.hobby.add(*hobbys_list)
        ret_data_dict["status"] = True
        return HttpResponse(json.dumps(ret_data_dict))


def get_check_code(request):
    import io
    from lib import check_code
    stream = io.BytesIO()
    img, code = check_code.create_validate_code()
    img.save(stream, "png")

    # set check code in session "check_code"
    request.session["check_code"] = code
    # return string , but it is a pic file, browser can show it in img tag
    return HttpResponse(stream.getvalue())




def add_user_type(request):
    # models.UserType.objects.create(caption="CEO")
    # models.UserType.objects.create(caption="COO")
    # models.UserType.objects.create(caption="CXO")
    for i in range(50):
        models.UserType.objects.create(caption="CCO_" + str(i))
    return HttpResponse("ok")


# admin-like object
def show_all_user(request):
    data_to_tpl = {}
    username = request.session.get("username", None)
    data_to_tpl["username"] = username

    all_user = models.UserInfo.objects.all()
    data_to_tpl["users"] = all_user

    yangli_obj = models.UserInfo.objects.get(username="yangli")
    print(type(yangli_obj.user_type_id), yangli_obj.user_type_id)

    return render(request, "chouti_like/show_all_user.html", data_to_tpl)


def delete_cur_user(request):
    ret_data_dict = {}
    ret_data_dict["status"] = False

    if request.method == "POST":
        user_id = request.POST.get("user_id", None)
        models.UserInfo.objects.get(pk=user_id).delete()
        ret_data_dict["status"] = True

    return HttpResponse(json.dumps(ret_data_dict))


def detail(request):
    data_to_tpl = {}
    data_to_tpl["username"] = request.session.get("username", None)

    user_types = models.UserType.objects.all()
    data_to_tpl["user_types"] = user_types

    all_hobbys = models.Hobby.objects.all()
    data_to_tpl["all_hobbys"] = all_hobbys

    user_types = models.UserType.objects.all()
    data_to_tpl["user_types"] = user_types

    if request.method == "GET":
        user_id = request.GET.get("user_id")
        user_obj = models.UserInfo.objects.get(pk=user_id)
        data_to_tpl["user"] = user_obj

        my_hobbys = user_obj.hobby.all()
        data_to_tpl["my_hobbys"] = my_hobbys

    else:
        # POST

        user_id = request.POST.get("id", None)
        # print(type(request.POST.values()), request.POST.values())

        to_update_dict = {}
        to_update_dict["password"] = request.POST.get("password")
        to_update_dict["phone"] = request.POST.get("phone")
        to_update_dict["email"] = request.POST.get("email")
        to_update_dict["user_type_id"] = request.POST.get("user_type_id")
        front_hobbys = list(request.POST.getlist("hobbys"))
        print("---front_hobbys:", front_hobbys)
        print("---to_update_dict", to_update_dict)

        # update
        models.UserInfo.objects.filter(pk=user_id).update(**to_update_dict)
        user_obj = models.UserInfo.objects.get(pk=user_id)
        user_obj.hobby.clear()
        user_obj.hobby.add(*front_hobbys)
        user_obj.save()  # save to databases

        # return real data
        data_to_tpl["user"] = user_obj
        data_to_tpl["my_hobbys"] = user_obj.hobby.all()
        data_to_tpl["status"] = True
        data_to_tpl["message"] = "更新成功"


    print("---user hobbys:", data_to_tpl["user"].hobby.all())
    return render(request, "chouti_like/show_detail.html", data_to_tpl)


