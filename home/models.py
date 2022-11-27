from django.db import models


# Create your models here.

class mqttData(models.Model):
    jobName= models.CharField(max_length=200)
    createdTime = models.DateTimeField(auto_now_add = True)
    startedTime = models.DateTimeField()
    length = models.FloatField()

