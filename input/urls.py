from django.urls import path
from .views import productCreateView
from . import views  # imports views file from same folder

urlpatterns = [
    path('', views.home.as_view(), name= "input.home"),
    # path('order', views.orderCreateView.as_view(), name= "input.order"),
    # path('product', views.productCreateView.as_view(), name="input.product"),
]