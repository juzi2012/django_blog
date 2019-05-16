import datetime
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum
from django.utils import timezone
from .models import ReadNum,ReadDetail

def read_statist_once_read(request,blog):
    content_type = ContentType.objects.get_for_model(blog)
    key = "%s_%s_read" % (content_type.model,blog.pk)
    if not request.COOKIES.get(key):
        # 总阅读数+1
        readnum, created = ReadNum.objects.get_or_create(content_type=content_type,object_id=blog.pk)        
        readnum.read_num+=1
        readnum.save()
        # 每天的阅读+1
        date=timezone.now().date()
        detail_read_num, created = ReadDetail.objects.get_or_create(content_type=content_type,object_id=blog.pk,date=date)
        detail_read_num.read_num+=1
        detail_read_num.save()

    return key

def get_sevendays_read_data(content_type):
    today = timezone.now().date()
    read_num = []
    days = []
    for i in range(6,-1,-1):
        date = today-datetime.timedelta(days=i)
        days.append(date.strftime('%m/%d'))
        read_details = ReadDetail.objects.filter(content_type=content_type,date = date)
        # 聚合计算，把read_details里面所有的元素的read_num求和
        result = read_details.aggregate(read_num_sum = Sum('read_num'))
        read_num.append(result['read_num_sum'] or 0)
    
    return days,read_num

def get_today_hot_data(content_type):
    today = timezone.now().date()
    read_details = ReadDetail.objects.filter(content_type=content_type,date = today)
    return read_details.order_by('-read_num')[:7]

def get_yesterday_hot_data(content_type):
    today = timezone.now().date()
    yesterday = today-datetime.timedelta(days=1)
    read_details = ReadDetail.objects.filter(content_type=content_type,date = yesterday)
    return read_details.order_by('-read_num')[:7]
        