/**
 * Created by lee on 16/10/17.
 */

(function (jq) {
    jq.fn.extend({
        valid:function () {
            //给submit绑定一个点击事件的方法
            //this 就是form
            $(this).find(':button').bind('click', function () {
                // this  就是submit 这个 input

                $('.item span').remove();  //先移除之前的span信息
                var flag = true;


                $('.item input[type=text],.item input[type=password]').each(function () {
                    // 如果已经发现了错误,那就不在继续向下执行检测了
                    // 这里其实可有可无,规范点,我决定留着
                    if(flag == false){
                        return false;  // 注意这里必须return false 才能完全跳出这个each() method
                    }

                    tag_value = $(this).val();


                    if($(this).attr("required")){
                        if($(this).val().trim().length <= 0){
                            //验证不合法,新建一个span标签放在当前标签的后面,作为提示的字母
                            //this  当前标签, dom对象
                            //$(this) 当前标签,jquery对象
                            var span_tag = document.createElement("span");
                            span_tag.innerText = $(this).attr("label") + "不能为空";
                            $(this).after(span_tag)
                            //$(this).parent().append(span_tag);
                            flag = false;
                            return false;  //跳出each循环
                        }
                    }

                    if($(this).attr("len_min")){
                        var min_len = parseInt($(this).attr("len_min"));
                        if(tag_value.length < min_len){
                            // 长度不够
                            // var span_tag = document.createElement("span");
                            // span_tag.innerText = $(this).attr("label") + "长度不能小于" + min_len;
                            // $(this).after(span_tag)
                            //$(this).parent().append(span_tag);
                            msg = $(this).attr("label") + "长度不能小于" + min_len + "位";
                            showMessage($(this), msg);
                            flag = false;
                            return false;  //跳出each循环
                        }

                    }


                    if($(this).attr("len_max")){
                        var len_max = parseInt($(this).attr("len_max"));
                        if (tag_value.length > len_max){
                            msg = $(this).attr("label") + "长度不能大于" + len_max + "位";
                            showMessage($(this), msg);
                            flag = false;
                            return false;
                        }
                    }

                    if($(this).attr("phone")){
                        phoneReg = /^1\d{10}$/;
                        if(!phoneReg.test(tag_value)){
                            msg = "手机号的格式不对哦"
                            showMessage(this, msg);
                            flag = false;
                            return false;
                        }
                    }



                }) //forEach()

                //如果前端验证通过,执行ajax函数
                if(flag){
                    ajaxSubmit();
                }
                return flag;  //调试阶段全部返回false  现在把外面的submit 换成了button,就算前段验证成功也不会跳转,只有等ajax跳转
            });

        },
        valid2:function () {
            console.log("this is test $.fn.extends({})");
            console.log(this[0])
        },
    });

    //一个把错误信息显示在当前标签后面的函数
    function showMessage(ths, msg) {
        var span_tag = document.createElement("span");
        span_tag.innerText = msg;
        $(ths).after(span_tag);
        //$(this).parent().append(span_tag);
    }


    function ajaxSubmit() {
            alert("ajax request in js extends");
            $.ajax({
                url:"jd_like/ajax_demo/",
                type:"POST",
                data:{"username":$('#id_username').val(),
                    "password":$('#id_password').val(),
                    "phone":$('#id_phone').val(),
                },
                success:function (data) {
                    console.log(data)
                    if(data == "ok"){
                        location.href = "/jd_like/jd_main_page/"
                    }else {
                        alert("后端验证失败（ajax）-- 用户名已经存在");
                        return false
                    }
                },
            });
        }


})($)
