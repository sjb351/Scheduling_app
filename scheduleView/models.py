from django.db import models
from input.models import proccess, proccessesList, product, machine, worker
from datetime import datetime, timedelta
from django.utils import timezone, timesince
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

d0 = timedelta(days =0, seconds = 0)

class order(models.Model):
    idNumber = models.PositiveBigIntegerField()
    createdTime = models.DateTimeField(auto_now_add = True)
    productAdd = models.ForeignKey(product, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)
    completedOrder = models.BooleanField(default=False)

    def __int__(self):
        return 'Order - ' + str(self.idNumber)

# @receiver(post_save, sender=order)
# def create_new_jobs(sender, instance, created, **kwargs):
#     print("Created new order")
#     if created:
#         print("Created new order")
#         jobNeeded = instance.productAdd.proccessesList.proccess.all()
#         for jobs in jobNeeded:
#             print(jobs)

class jobs(models.Model):
    proccess =  models.ForeignKey(proccess, on_delete=models.CASCADE,null=True, blank =True)
    order = models.ForeignKey(order, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField()

    startTime = models.DateTimeField(default=timezone.now)
    endTime = models.DateTimeField(default=timezone.now)
    actualEnd = models.DateTimeField(default=timezone.now)
    delayTime = models.DurationField(default = d0) 

    startedJob = models.BooleanField(default = False, null=True, blank=True)
    completedJob = models.BooleanField(default = False, null=True, blank=True)
   
    machine = models.ManyToManyField(machine,  blank=True)
    worker = models.ManyToManyField(worker,  blank=True)
    rank = models.PositiveBigIntegerField()

    def __str__(self):
        return self.proccess.name + ' for: ' + str(self.order.idNumber)
    
    # @property
    # def rankOrder(self):
    #     return self.proccess.rankOrder

