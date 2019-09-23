from django.contrib import admin
from . import  models
# Register your models here.
admin.site.register(models.User)
admin.site.register(models.Subscriber)
admin.site.register(models.Inactive)
admin.site.register(models.Blog)