from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=False,blank=False)
    profile_code = models.CharField(max_length=8,null=False,blank=False)
    profile_photo = models.ImageField(null=False,blank=False,default='profile_pics/default_profile_pic.jpg',upload_to='profile_pics')
    bio = models.CharField(max_length=160,null=True,blank=True,default='Not any information was given.')

    def __str__(self):
        return str(self.user.username)


class Room(models.Model):
    room_name = models.SlugField(null=False,blank=False,max_length=100)
    profiles = models.ManyToManyField(Profile)

    def __str__(self):
        return self.room_name


class Message(models.Model):
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE,null=False,blank=False,related_name='profile')
    text = models.TextField(null=False,blank=False)
    room = models.ForeignKey(Room,null=False,blank=False,on_delete=models.CASCADE,related_name='room')
    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text