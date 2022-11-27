from django.contrib import admin
# Register your models here.
from . import models


class processAdmin(admin.ModelAdmin):
    pass
class processListAdmin(admin.ModelAdmin):
    pass
class productAdmin(admin.ModelAdmin):
    pass
class workerAdmin(admin.ModelAdmin):
    pass
class machineAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.proccess, processAdmin)
admin.site.register(models.proccessesList, processListAdmin)
admin.site.register(models.product, productAdmin)
admin.site.register(models.worker, workerAdmin)
admin.site.register(models.machine, machineAdmin)
