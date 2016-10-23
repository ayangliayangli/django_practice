from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.core.exceptions import ValidationError
from chouti_like import models
from django import forms

# Create your views here.


class SessionRegisterForm(forms.Form):
    user_type_choices = models.UserType.objects.all().values_list("id", "caption")

    username = forms.CharField(max_length=16)
    password = forms.CharField(max_length=16)
    phone = forms.IntegerField()
    email = forms.EmailField()
    user_type_id = forms.IntegerField(widget=forms.Select(choices=user_type_choices))

    def __init__(self, *args, **kwargs):
        super(SessionRegisterForm, self).__init__(*args, **kwargs)
        self.fields["user_type_id"].widget.choices=models.UserType.objects.all().values_list("id", "caption")


def session_login(request):
    pass

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

                # clean_data["user_type_id__id"] = clean_data.get("user_type_id", 1)
                # del clean_data["user_type_id"]
                # print("---after:", clean_data)

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


def add_user_type(request):
    models.UserType.objects.create(caption="CEO")
    models.UserType.objects.create(caption="COO")
    models.UserType.objects.create(caption="CXO")
    return HttpResponse("ok")