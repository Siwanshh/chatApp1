from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
class Topic(models.Model):
    name=models.TextField(max_length=50,default="Django")
    def __str__(self):
        return self.name 
class Room(models.Model):
    host=models.ForeignKey(User,on_delete=models.CASCADE,null=True, blank=True)
    topic=models.ForeignKey(Topic,on_delete=models.CASCADE,related_name="room_set",null=True, blank=True)
    name=models.CharField(max_length=200,default="Unknown",blank=False)
    description=models.TextField(null=True,blank=True)
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)
    participants=models.ManyToManyField(User,related_name='rooms')
    def __str__(self):
        return self.name
    class Meta:
        ordering=['-updated','-created']
    
class Message(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True, blank=True)
    room=models.ForeignKey(Room,on_delete=models.CASCADE)
    body=models.TextField(max_length=1000)
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png')
    email=models.EmailField(blank=True,null=True)
    def __str__(self):
        return f"{self.user.username}'s Profile"        

