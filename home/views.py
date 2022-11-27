from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from django.contrib.auth.decorators import login_required
from .models import mqttData
import json
from django.http import JsonResponse
#from basicApp.settings import client as mqtt_client
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
#def home(request):
#    return HttpResponse('Hello World  <br>  new line testing')

class homeView(TemplateView):
    template_name = 'home/welcome.html'
    #extra_context = {'mqtts': mqtt_data}

class AuthorisedView(LoginRequiredMixin, TemplateView):
    template_name = 'home/AuthorisedWelcom.html'
    login_url = '/admin'


#old non class view method
#def home(request):
#    mqtt_data = mqttData.objects.all()
#    return render(request, 'home/welcome.html', {'mqtts': mqtt_data})

#@login_required(login_url='/admin')
#def authHome(request):
#    return render(request, 'home/AuthorisedWelcom.html', {})


# def publish_message(request):
#     request_data = json.loads(request.body)
#     rc, mid = mqtt_client.publish(request_data['topic'], request_data['msg'])
#     return JsonResponse({'code': rc})