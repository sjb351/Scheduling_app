from django.contrib import admin

from . import models

# Register your models here.

class jobsAdmin(admin.ModelAdmin):
    pass
class orderAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.job, jobsAdmin)
admin.site.register(models.order, orderAdmin)