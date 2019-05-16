from django.shortcuts import render,redirect
from django.urls import reverse
import random,string,time
from django.contrib import auth
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.http import JsonResponse
from user_module.form import LoginForm,RegForm,ChangeNicknameForm,BindEmailForm,ChangePasswordForm,ForgetPasswordForm
from .models import Profile
# Create your views here.
# 这个是没有用django form的做法
def login_old(request):
    username = request.POST.get('username','')
    password = request.POST.get('password','')
    user = auth.authenticate(request,username=username,password=password)
    # 获取请求的页面 reverse是通过我们在view里面命名的，返向解析到对应的连接页面
    referer = request.META.get("HTTP_REFERER",reverse('index'))
    if user is not None:
        auth.login(request,user)
        return redirect(referer)
    else:
        return render(request,'error.html',{'message':'用户名或密码不正确'})

def login(request):
    if request.method =='POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # username = login_form.cleaned_data['username']
            # password = login_form.cleaned_data['password']
            # user = auth.authenticate(request,username=username,password=password)
            user = login_form.cleaned_data['user']
            auth.login(request,user)
            return redirect(request.GET.get('from',reverse('index')))
    else:
        login_form = LoginForm()


    context = {
        "login_form":login_form
    }
    return render(request,'user_module/login.html',context)

def register(request):
    if request.method=='POST':
        reg_form = RegForm(request.POST,request=request)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            user = User.objects.create_user(username,email,password)
            user.save()
            # 清楚session
            del request.session['register_email_code']
            # 顺便登录用户 
            user = auth.authenticate(username=username,password=password)
            auth.login(request,user)
            # 跳转到之前进入注册的页面
            return redirect(request.GET.get('from',reverse('index')))
    else:
        reg_form = RegForm()
    
    context = {
        "reg_form":reg_form
    }
    return render(request,'user_module/register.html',context)


def user_info(request):
    context = {
    }
    return render(request,'user_module/user_info.html',context)

def logout(request):
    auth.logout(request);
    return redirect(request.GET.get('from',reverse('index')))

def change_nickname(request):
    redirect_url = request.GET.get('from',reverse('index'))
    if request.method=='POST':
        form = ChangeNicknameForm(request.POST,user=request.user)
        if form.is_valid():
            nickname = form.cleaned_data['nickname']
            profile,created = Profile.objects.get_or_create(user = request.user)
            profile.nickname = nickname
            profile.save()
            return redirect(redirect_url)
    else:
        form = ChangeNicknameForm()

    context = {
        'form':form,
        'page_title':"修改昵称",
        'form_title':"修改昵称",
        'submit_text':"修改",
        'return_back_url':redirect_url,
    }
    return render(request,'form.html',context)

def bind_email(request):
    redirect_url = request.GET.get('from',reverse('index'))
    if request.method=='POST':
        form = BindEmailForm(request.POST,request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            request.user.email = email
            request.user.save()
            # 清楚session
            del request.session['bind_email_code']
            return redirect(redirect_url)
    else:
        form = BindEmailForm()

    context = {
        'form':form,
        'page_title':"绑定邮箱",
        'form_title':"绑定邮箱",
        'submit_text':"绑定",
        'return_back_url':redirect_url,
    }
    return render(request,'user_module/bind_email.html',context)

def send_verification_code(request):
    email = request.GET.get('email','')
    send_for = request.GET.get('send_for','')
    data={}
    if email!='':
        now = int(time.time())
        send_code_time = request.session.get('send_code_time',0)
        if now - send_code_time <30:
            data['status'] = "FAILD"
        else:
            # 保存发送时间
            request.session['send_code_time'] = now
            # 生成验证码
            code = ''.join(random.sample(string.ascii_letters+string.digits,4))
            # 一般有效期是两个星期
            request.session[send_for] = code
            # 发送邮件
            send_mail(
                '绑定邮箱验证码',
                '验证码:%s' % code,
                '282976305@qq.com',
                [email],
                fail_silently=False,
            )
            data['status'] = "SUCCESS"
    else:
        data['status'] = "FAILD"
    return JsonResponse(data)


def change_password(request):
    redirect_url = reverse('index')
    if request.method=='POST':
        form = ChangePasswordForm(request.POST,user=request.user)
        if form.is_valid():
            user = request.user
            new_password = form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()
            auth.logout(request)
            return redirect(redirect_url)
    else:
        form = ChangePasswordForm()
    
    context = {
        'form':form,
        'page_title':"修改密码",
        'form_title':"修改密码",
        'submit_text':"修改",
        'return_back_url':redirect_url,
    }
    return render(request,'form.html',context)

def forget_password(request):
    redirect_url = reverse('user_module:login')
    if request.method=='POST':
        form = ForgetPasswordForm(request.POST,request=request)
        if form.is_valid():
            print(222)
            email = form.cleaned_data['email']
            new_password = form.cleaned_data['new_password']
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
             # 清楚session
            del request.session['forget_email_code']
            return redirect(redirect_url)
    else:
        form = ForgetPasswordForm()
    
    context = {
        'form':form,
        'page_title':"忘记密码",
        'form_title':"忘记密码",
        'submit_text':"提交",
        'return_back_url':redirect_url,
    }
    return render(request,'user_module/forget_password.html',context)
