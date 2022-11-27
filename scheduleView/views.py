from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from scheduleView.models import order, jobs
from input.models import product, proccessesList, machine, proccess
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from scheduleView.processData import printProduct, updateTimesByCreated
from .forms import orderForm
from plotly.offline import plot
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
    
def listOrder(request):
    order_data = order.objects.all()
    proces = printProduct()
    product_data = order_data

    return render(request, 'schedule/orderDisplay.html', {'order': order_data })

# def newOrder(request):
#     order_data = order.objects.all()
#     proces = printProduct()
#     product_data = order_data
#     return render(request, 'schedule/orderDisplay.html', {'order': order_data })


class orderCreateView(CreateView):
    model = order
    success_url = 'schedule/order'
    template_name = 'schedule/order.html'
    form_class = orderForm

def orderNew(request):
    if request.method == 'POST':
        # POST, generate form with data from the request
        form = orderForm(request.POST)
        # check if it's valid:
        if form.is_valid():
            # process data, insert into DB, generate email,etc
            # redirect to a new url:
            #request.object
            x = form.save()
            list = []
            ord = order.objects.get(pk = x.id)
            productMake=order.objects.get(pk = x.id).productAdd 
            #proccess.objects.exclude(proccessesLis__isnull = True) 

            procesList = proccess.objects.exclude(proccessesLis__isnull = True) 

            for prod in range(procesList.count()):  # loop thoguh all processes 
                new = procesList[prod].proccessesLis.product
                if productMake == new:  # check if processes and order product match up 
                    list.append(procesList[prod].name) # store in list
                    jobNew = jobs(order = ord, quantity = ord.quantity, proccess = procesList[prod], rank = procesList[prod].rankOrder)   #create a new job for the order
                    #jobNew = procesList[prod]    # assisgn more vlaues to new job from process found
                    jobNew.order = ord
                    jobNew.save()

            num = updateTimesByCreated()
            
            return render(request, 'schedule/jobs.html', {'orderId': ord.idNumber, 'jobs': list, 'number': num })

            #return HttpResponseRedirect('/schedule/demo')
    else:
        # GET, generate blank form
        form = orderForm()
    return render(request, 'schedule/order.html', {'form': form })

def findColor(proc):
    match proc.rankOrder:
        case 1:
            return 'red'
        case 2:
            return 'blue'
        case 3:
            return 'grey'
        case 4:
            return 'orange'


def order_plot_view(request):
    num = updateTimesByCreated()
    #data automatically set by project
    data =order.objects.all()
    gantt_data = [
        {
            'Name': x.idNumber,
            'start':x.createdTime,
            'endTime': (x.createdTime + timedelta(hours=0, minutes=x.quantity, seconds =0)),
            'product': x.productAdd
        } for x in data
    ]

    #create initial frame for gantt chart data
    df = pd.DataFrame(gantt_data)

    fig1 =px.timeline(df, x_start="start", x_end="endTime", y="Name" )
    fig1.update_yaxes(autorange="reversed")

    plot_div = plot(fig1, output_type='div')
    #= plot({'data': graphs, 'layout': layout},output_type='div')
    context={'plot_div': plot_div}
    return render(request, 'schedule/schedulePlot.html', context)

def jobs_plot_view(request):
    num = updateTimesByCreated()
    #data automatically set by project
    data =jobs.objects.all()
    gantt_data = [
        {
            'Name': x.proccess.name,
            'start':x.startTime,
            'endTime': (x.endTime),
            'order': x.order.pk,
            'Color': findColor(x.proccess)
        } for x in data
    ]

    #create initial frame for gantt chart data
    df = pd.DataFrame(gantt_data)
    cm = {x:x for x in df.Color.unique()}
    fig1 =px.timeline(df, x_start="start", x_end="endTime", y="order", color="Color", color_discrete_map =cm)
    fig1.update_yaxes(autorange="reversed")
    plot_div = plot(fig1, output_type='div')
    #= plot({'data': graphs, 'layout': layout},output_type='div')
    context={'plot_div': plot_div}
    return render(request, 'schedule/schedulePlot.html', context)