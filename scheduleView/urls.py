from django.urls import path

from . import views

urlpatterns = [
    path('test', views.listOrder, name= "schedule.home"),
    path('order', views.order_plot_view, name="schedule.show"),
    path('jobs', views.jobs_plot_view, name="schedule.show"),
    path('new_order', views.orderCreateView.as_view(), name="new-order"),
    path('new', views.orderNew, name="new-order2")
    #path('jobs', views.orderCreateView.as_view(), name= "schedule.jobs"),
    #path('update', views.UpdateView.as_view(), name="schedule.update"),
]