
# 优化 1022

## 大原则
    
        把本次项目做成一个APP和项目来写,APP NAME : JD_LIKE
        删除了大量无关的url views models template
        删除了大量无关的statics文件
        删除了大量练习的代码


## 细化修改

            1. frontend_app/migrations/0004_user.py
             create mode 100644 frontend_app/migrations/__pycache__/0004_user.cpython-34.pyc, 这种migrations里的文件和pyc结尾的文件都可以放到gitignore文件，不需要git 上传。   
                --1022-- 已经在项目目录下面添加 .gitignore  ----> .idea/ db.sqlite*
             
            2.url的写法有点乱，我给注释起来的这两行采用最中间那个写法就好了，后面会有课程涉及到restapi的规则，到时候再改的更规范吧，目前先重点在实现功能，所以url个数也尽量简化
                --1022-- 已经优化url写法,把不必要的删除
                
            3.templates目录就放html文件的，不需要再多出来  
                 htmls
                │   ├── checkbox_select.html
                │   ├── dialog_full_screen.html
                │   └── search.html
                这堆东西都整理到templates，相对路径取用文件
                --1022-- 这个是练习代码,对本APP无用,已经移除
            
            4.html代码里的js代码也要命名规范一下，什么id1，还有带着个人特色 li下划线开通的名字都换掉，
            改成有点功能意义的名字
            <input id="id1" type="text" value="search" onfocus="li_focus();" onblur="li_blur();">
                --1022-- 已从项目中删除该文件
            
            
            5.img都放到static里面就行，怎么templates里还有？
                --1022-- templates 里面的已经删除
            
            6.开始尝试用ajax了，很好！
                --1022-- 谢谢
            7.最好把这部分作业要求的单独拆出来一个独立项目。目前看着还像个大练习，记得我和你们说过要把作业当成自己的产品做吧
            综上，这次成绩只能给到75，再修改吧。我希望看到更好的版本再给你开通新课程。
                --1022-- 已经独立成一个项目,下一次的作业我的建议是在这个project上面新建APP,你看怎么样?
