from django.urls import path
from . import views
app_name = 'blog'

urlpatterns = [
    path('',views.blog_list,name='bloglist'),
    path('<int:blog_id>/',views.blog_detail,name='blog_detail'),
    path('blog_type/<int:blog_type_id>',views.blogs_with_type,name='blog_with_type'),
    path('date/<int:year>/<int:month>',views.blogs_with_date,name="blogs_with_date"),
]