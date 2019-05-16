import datetime
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum
from django.core.cache import cache
from django.contrib import auth
from django.utils import timezone
from django.urls import reverse
from django.shortcuts import render,redirect
from read_statist.utils import get_sevendays_read_data, \
                                get_today_hot_data,get_yesterday_hot_data
from blog.models import Blog

# 获取7天的数据，如果简单按照今天明天的方法，会得到一些重复id的数据，
# 所以必须按照下面的方式去获取，在Blog里面用了GenericRelation方法来反向获取信息
def get_seven_day_hot_data():
    today = timezone.now().date()
    day = today-datetime.timedelta(days=7)
    blogs = Blog.objects.\
                filter(read_detail__date__lte=today,read_detail__date__gte=day) \
                .values('id','title') \
                .annotate(read_num_sum = Sum('read_detail__read_num')) \
                .order_by('-read_num_sum')
    return blogs
def index(request):
    content_type = ContentType.objects.get_for_model(Blog)
    days,seven_day_read_nums = get_sevendays_read_data(content_type)
    today_hot_date = get_today_hot_data(content_type)
    yesterday_hot_data = get_yesterday_hot_data(content_type)

    # 获取7天热门blog的缓存数据
    seven_day_hot_data = cache.get('seven_day_hot_data')
    if seven_day_hot_data is None:
        seven_day_hot_data = get_seven_day_hot_data()
        cache.set('seven_day_hot_data',seven_day_hot_data,3600)

    context={
        'days':days,
        'seven_day_read_nums':seven_day_read_nums,
        'today_hot_date':today_hot_date,
        'yesterday_hot_data':yesterday_hot_data,
        'seven_day_hot_data':seven_day_hot_data
    }
    return render(request,'index.html',context)


