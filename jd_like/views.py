from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from . import models

# Create your views here.


USER_INFO_LIST = []
ASSETS_INFO_LIST = []


def template(request):
    USER_INFO_LIST = models.User.objects.all()
    return render(request, "jd_like/template.html", {"user_info_list":USER_INFO_LIST})


def userinfo(request):
    USER_INFO_LIST = models.User.objects.all()
    return render(request, "jd_like/userinfo.html", {"user_info_list":USER_INFO_LIST})


def assets(request):
    global ASSETS_INFO_LIST
    ASSETS_INFO_LIST.clear()
    for i in range(50):
        tmp = {}
        tmp.setdefault("hostname","host_"+str(i))
        tmp.setdefault("ip","192.168.1."+str(i + 1))
        ASSETS_INFO_LIST.append(tmp)

    return render(request, "jd_like/assets.html", {"assets_info_list":ASSETS_INFO_LIST})


def ajax_demo_register(request):
    if request.method == "GET":
        return render(request, "jd_like/ajax_demo_register.html")
    else:
        # POST
        print(request.POST)
        print("---------ajax-request---")

        username = request.POST.get("username")
        password = request.POST.get("password")
        phone = request.POST.get("phone")

        flag = models.User.objects.filter(username=username).count()
        if flag :
            # 数据库中查到了相关的记录,那给客户端返回失败
            return HttpResponse("failure")
        else:
            # 数据库钟没有查到记录,那么把当前数据插入数据库,然后返回注册成功
            models.User.objects.create(username=username, password=password, phone=phone)
            return HttpResponse("ok")


def ajax_demo_login(request):
    if request.method == "GET":
        return render(request, "jd_like/ajax_demo_login.html")
    else:
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        flag = models.User.objects.filter(username=username, password=password).count()
        if flag:
            # 数据库中有记录,且用户名和密码正确
            return HttpResponse("ok")
        else:
            # 数据库中没有相应的记录
            return HttpResponse("failure")


def jd_main_page(request):
    return render(request, "jd_like/jd_main_page.html")


def index(request):
    return render(request, "jd_like/index.html");