from django.urls import path
from . import views
app_name = 'comment'

urlpatterns = [
    path('',views.commit_comment,name='commit_comment'),
]