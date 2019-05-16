from django.contrib import admin
from .models import Blog,BlogType

# Register your models here.
@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('id','type_name')
    ordering = ('id',)
    
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id','title','blog_type','read_num','author','created_time','last_update_time')

