from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    nickname = models.CharField(max_length=20,verbose_name="昵称")

    def __str__(self):
        return '<Profile:%s for %s>' %(self.nickname,self.user.username)

# 下面的要注意⚠️
# 将此方法赋值给user的一个方法，这样就可以直接调用user的get_nickname来获取信息
def get_nickname(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.nickname
    else:
        return ""

def get_nickname_or_username(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.nickname
    else:
        return self.username

def has_nickname(self):
       return Profile.objects.filter(user=self).exists()

User.get_nickname = get_nickname
User.has_nickname = has_nickname
User.get_nickname_or_username = get_nickname_or_username