from django.db import models
from django.db.models.signals import post_save
import datetime

# Create your models here.

class User(models.Model):
    first_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)

    def __str__(self):
        return self.first_name + " | " + self.email

class Subscriber(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.first_name

class Inactive(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.first_name

class Blog(models.Model):
    heading = models.CharField(max_length=50)
    article = models.TextField()
    date = models.DateTimeField(default=datetime.datetime.now())

    def __str__(self):
        return self.heading

#signal to auto-subscribe new user

def subscribe_default(sender, **kwargs):
    if kwargs['created']:
        user = User.objects.latest('pk')
        s = Subscriber(user=user)
        s.save()

post_save.connect(subscribe_default, sender=User)

