from django.shortcuts import get_object_or_404,render
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.db.models import Count
from read_statist.utils import read_statist_once_read
from .models import Blog,BlogType
from comment.models import Comment
from comment.forms import CommentForm
# Create your views here.
def blog_list(request):
    blog_all_lists = Blog.objects.all()
    # 设置分页器
    paginator = Paginator(blog_all_lists,6)
    # 获取请求的页码(GET请求)
    page_num = request.GET.get('page',1)
    page_of_blogs = paginator.get_page(page_num)

    current_page_num = page_of_blogs.number #当前页码
    
    context = {
        'blogs':page_of_blogs.object_list,
        'page_of_blogs':page_of_blogs,
        'blog_types':BlogType.objects.annotate(blog_count=Count('blog')),
        'blog_dates':Blog.objects.dates('created_time','month',order='DESC')
    }
    return render(request,'blog/blog_list.html',context)

def blogs_with_type(request,blog_type_id):

    blog_type =  get_object_or_404(BlogType,pk=blog_type_id)
    blog_all_lists = Blog.objects.filter(blog_type=blog_type)
    # 设置分页器
    paginator = Paginator(blog_all_lists,6)
    # 获取请求的页码(GET请求)
    page_num = request.GET.get('page',1)
    page_of_blogs = paginator.get_page(page_num)

    context = {
        'blogs':page_of_blogs.object_list,
        'blog_type':blog_type,
        'page_of_blogs':page_of_blogs,
        'blog_types':BlogType.objects.annotate(blog_count=Count('blog')),
        'blog_dates':Blog.objects.dates('created_time','month',order='DESC')
    }
    return render(request,'blog/blog_with_type.html',context)


def blog_detail(request,blog_id):
    blog = get_object_or_404(Blog,id=blog_id)
    key = read_statist_once_read(request,blog)
    blog_content_type = ContentType.objects.get_for_model(blog)
    comments = Comment.objects.filter(content_type=blog_content_type,object_id=blog_id,parent=None)

    form_init_data = {
        "content_type":blog_content_type,
        "object_id":blog_id,
        'reply_comment_id':0
    }

    context = {
        'blog':blog,
        'previous_blog':Blog.objects.filter(created_time__gt=blog.created_time).last(),
        'next_blog':Blog.objects.filter(created_time__lt=blog.created_time).first(),
        'comments':comments,
        'comment_form':CommentForm(initial=form_init_data)
    }
    response = render(request,'blog/blog_detail.html',context)
    response.set_cookie(key,'true',max_age=60)
    return response

def blogs_with_date(request,year,month):
    blog_all_lists = Blog.objects.filter(created_time__year=year,created_time__month=month)
    # 设置分页器
    paginator = Paginator(blog_all_lists,6)
    # 获取请求的页码(GET请求)
    page_num = request.GET.get('page',1)
    page_of_blogs = paginator.get_page(page_num)
    
    context = {
        'blog_with_date':"%s年%s月" %(year,month),
        'blogs':page_of_blogs.object_list,
        'page_of_blogs':page_of_blogs,
        'blog_types':BlogType.objects.annotate(blog_count=Count('blog')),
        'blog_dates':Blog.objects.dates('created_time','month',order='DESC')
    }
    return render(request,'blog/blog_with_date.html',context)