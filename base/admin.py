from django.contrib import admin
from base import models
# Register your models here.
admin.site.register(models.Profile)
admin.site.register(models.Room)
admin.site.register(models.Message)