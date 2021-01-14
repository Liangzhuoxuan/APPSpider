from django.db import models

# Create your models here.

class App(models.Model):
    appStore = models.CharField(max_length=255)
    appName = models.CharField(max_length=255)
    version = models.CharField(max_length=255)
    updateTime = models.DateTimeField()
    author = models.CharField(max_length=255)
    downloadUrl = models.CharField(max_length=255)
    icon = models.CharField(max_length=255)
    introduction = models.CharField(max_length=1500)
    inList = models.CharField(max_length=25)
    platform = models.CharField(max_length=25)
    insertTime = models.DateTimeField()
    keyword = models.CharField(max_length=25)
