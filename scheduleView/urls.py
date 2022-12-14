from django.urls import path

from . import views

urlpatterns = [
    path('test', views.listOrder, name= "schedule.home"),
    path('Order', views.order_plot_view, name="schedule.show.orders"),
    path('Jobs', views.jobs_plot_view, name="schedule.show.jobs"),
    path('Machine', views.machine_plot_view, name="schedule.show.machine" ),
    path('Worker', views.worker_plot_view, name="schedule.show.worker" ),
    path('new_order', views.orderCreateView.as_view(), name="new-order"),
    path('new', views.orderNew, name="new-order2")
    #path('jobs', views.orderCreateView.as_view(), name= "schedule.jobs"),
    #path('update', views.UpdateView.as_view(), name="schedule.update"),
]