from django.contrib import admin
from .models import ReadNum,ReadDetail
# Register your models here.
@admin.register(ReadNum)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('read_num','content_object')

@admin.register(ReadDetail)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('date','content_object','read_num')
