from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import order, jobList, jobs

# @receiver(post_save, sender=order)
# def create_new_jobs(sender, instance, created, **kwargs):
#     if created:
#         jobNeeded = instance.productAdd.proccessesList.proccess.all()
#         for jobs in jobNeeded:
#             print()