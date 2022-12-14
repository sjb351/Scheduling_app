from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta
#from adminsortable2.models import SortableMixin

d0 = timedelta(days =0, seconds = 0)

class product(models.Model):
    name = models.CharField(max_length=100)
    # models.ForeignKey(order, on_delete=models.CASCADE)
    # proccesses= models.ManyToManyField(proccess, through='ProductProcces')

    def __str__(self):
        return self.name

class proccessesList(models.Model):
    #product = models.ForeignKey(product, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    product = models.ForeignKey(product, on_delete=models.PROTECT)
    
    def __str__(self):
        return 'List of Processes for : ' + self.product.name


class procces(models.Model):
    name = models.CharField(max_length=100)
    duration = models.DurationField(default=d0)
    automated = models.BooleanField(default=False)
    WorkerSetUpTime = models.DurationField(default = d0, null=True, blank=True)
    WorkerpostProcessTime = models.DurationField(default = d0, null=True, blank=True)
    proccessesLis =  models.ForeignKey(proccessesList, on_delete=models.CASCADE,null=True, blank =True)
    rankOrder = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return 'Process: ' + self.name
    
    class meta:
        ordering = ['rank_order']
        #abstract=True # Set this model as Abstract


# Create your models here.
class machine(models.Model):
    name = models.CharField(max_length=100)
    iDnumber = models.PositiveBigIntegerField(default=0)
    useable = models.BooleanField(default=True)
    degredation = models.PositiveIntegerField(default = 0)
    proccessFor = models.ManyToManyField(procces, blank =True)
    numberParral = models.PositiveBigIntegerField(default=1)

    def __str__(self):
        return self.name

class worker(models.Model):
    name = models.CharField(max_length=100)
    iDnumber = models.PositiveBigIntegerField(default=0)
    useable = models.BooleanField(default=True)
    proccessTrainedFor = models.ManyToManyField(procces, blank =True)
    numberParral = models.PositiveBigIntegerField(default=1)

    def __str__(self):
        return self.name

# class facotryCell(models.Model):
#     machine = models.ManyToManyField(machine)
#     worker = models.ManyToManyField(worker)


    









