from django.shortcuts import render,redirect
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.http import JsonResponse
from .models import Comment
from .forms import CommentForm
# Create your views here.

def commit_comment(request):
    # 获取请求的页面 reverse是通过我们在view里面命名的，返向解析到对应的连接页面
    # 这个是老方法，没有用到django form
    '''redirect_to = request.META.get("HTTP_REFERER",reverse('index'))
    if not request.user.is_authenticated:
        return render(request,'error.html',{'message':'请先登录','redirect_to':redirect_to})

    text = request.POST.get('text','').strip()# 去除空格
    if text == '':
        return render(request,'error.html',{'message':'请填写内容','redirect_to':redirect_to})

    try:
        content_type = request.POST.get('content_type','')
        object_id = int(request.POST.get('object_id',''))

        # 得到Blog的class
        model_class = ContentType.objects.get(model = content_type).model_class()
        model_obj = model_class.objects.get(id = object_id)
    except Exception as e:
        return render(request,'error.html',{'message':'评论错误','redirect_to':redirect_to})

    comment = Comment(comment_user=request.user,text=text,content_object=model_obj)
    comment.save()

    return redirect(redirect_to)'''

    redirect_to = request.META.get("HTTP_REFERER",reverse('index'))
    comment_form = CommentForm(request.POST,user=request.user)
    if comment_form.is_valid():
        comment = Comment(comment_user=comment_form.cleaned_data['user'],text=comment_form.cleaned_data['text'],content_object=comment_form.cleaned_data['content_object'])
        comment.save()
        data = {
            'status':'SUCCESS',
            'username':comment.comment_user.username,
            'comment_time':comment.comment_time.strftime('%Y-%m-%d %H:%M:%S'),
            'text':comment.text
        }
        # return redirect(redirect_to)
    else:
        data = {
            'status':'FAILED',
            'message':list(comment_form.errors.values())[0][0]
        }
        # return render(request,'error.html',{'message':comment_form.errors,'redirect_to':redirect_to})
    return JsonResponse(data)

