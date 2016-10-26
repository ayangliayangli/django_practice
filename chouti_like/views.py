from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.core.exceptions import ValidationError
from chouti_like import models
from django import forms
from lib import pager

# Create your views here.


class SessionRegisterForm(forms.Form):
    user_type_choices = models.UserType.objects.all().values_list("id", "caption")

    username = forms.CharField(max_length=16)
    password = forms.CharField(max_length=16)
    phone = forms.IntegerField()
    email = forms.EmailField()
    user_type_id = forms.IntegerField(widget=forms.Select(choices=user_type_choices))

    def __init__(self, *args, **kwargs):
        # 解决新增了用户类型字段,没有及时显示的bug
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
        form_get = SessionRegisterForm()
        return render(request, "chouti_like/session_register.html", {"form":form_get})
    else:
        # post 提交数据
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
                return render(request, "chouti_like/session_register.html", {"form": form_post, "exist_flag":exist_flag})
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

                return HttpResponseRedirect("/chouti_like/index/")
        else:
            # form验证失败
            return render(request, "chouti_like/session_register.html", {"form": form_post})


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



def add_user_type(request):
    # models.UserType.objects.create(caption="CEO")
    # models.UserType.objects.create(caption="COO")
    # models.UserType.objects.create(caption="CXO")
    for i in range(50):
        models.UserType.objects.create(caption="CCO_" + str(i))
    return HttpResponse("ok")