from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from scheduleView.models import order, job
from input.models import product, proccessesList, machine, procces
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from scheduleView.processData import printProduct, updateTimesByCreated, updateOrderTime 
from .forms import orderForm
from plotly.offline import plot
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
import time 
from plotly.figure_factory import create_gantt
import json
from scheduleView.serilizer import DateTimeEncoder
from datetime import datetime
from dash import Dash, dcc, html, Input, Output
from django_plotly_dash import DjangoDash

def DecodeDateTime(empDict):
    if 'start' in empDict:
        empDict["start"] = datetime.fromisoformat(empDict["end"])
        return empDict
    elif 'end' in empDict:
        empDict["end"] = datetime.fromisoformat(empDict["end"])
        return empDict

#newdate = datetime.fromisoformat('2020-01-08T15:29:52.040435')

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

            procesList = procces.objects.exclude(proccessesLis__isnull = True) 

            for prod in range(procesList.count()):  # loop thoguh all processes 
                new = procesList[prod].proccessesLis.product
                if productMake == new:  # check if processes and order product match up 
                    list.append(procesList[prod].name) # store in list
                    jobNew = job(order = ord, quantity = ord.quantity, proccess = procesList[prod], rank = procesList[prod].rankOrder)   #create a new job for the order
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

def compleatedText(compleated):
    if compleated:
        return "Job started"
    else:
        return "Job not Started"

def order_plot_view(request):
    num = updateTimesByCreated()
    updateOrderTime() 
    #data automatically set by project
    data =order.objects.filter(completedOrder = False)
    if data.count() > 0:
        gantt_data = [
            {
                'Name': "Order " + str(x.pk),
                'start':x.startedTime,
                'endTime': x.endTime,
                'product': x.productAdd
            } for x in data
        ]
    else:
        gantt_data = [
            {
                'Name': 0,
                'start': 0,
                'endTime': 0,
                'order': 0,
                'Color': 'red'
            }
        ]
    
    #create initial frame for gantt chart data
    df = pd.DataFrame(gantt_data)

    fig1 =px.timeline(df, x_start="start", x_end="endTime", y="Name" )
    fig1.update_yaxes(autorange="reversed")
    fig1.update_traces(width=0.61)
    plot_div = plot(fig1, output_type='div')
    #= plot({'data': graphs, 'layout': layout},output_type='div')
    context={'plot_div': plot_div}
    return render(request, 'schedule/schedulePlot.html', context)


def jobs_plot_view(request):
    num = updateTimesByCreated()
    #data automatically set by project
    data =job.objects.filter(completedJob = False)
    if data.count() > 0:
        gantt_data = [
            {
                'Name': x.proccess.name,
                'Start':x.startTime,
                'End Time': (x.endTime),
                'Order': "Order " + str(x.order.pk),
                'Color': findColor(x.proccess),
                'Resource': str(x.quantity)
            } for x in data
        ]
    else:
        gantt_data = [
            {
                'Name': 0,
                'Start': 0,
                'End Time': 0,
                'Order': 0,
                'Color': 'red'
            }
        ]
    
    #create initial frame for gantt chart data
    df = pd.DataFrame(gantt_data)
    cm = {x:x for x in df.Color.unique()}
    fig1 =px.timeline(df, x_start="Start", x_end="End Time", y="Order", color="Name",  hover_name = "Resource", labels = "Name")
    fig1.update_yaxes(autorange="reversed")
    fig1.update_traces(width=0.61)
    plot_div = plot(fig1, output_type='div')
    #= plot({'data': graphs, 'layout': layout},output_type='div')
    context={'plot_div': plot_div}
    return render(request, 'schedule/schedulePlot.html', context)

def machine_plot_view(request):
    num = updateTimesByCreated()
    #data automatically set by project
    dataJobs = job.objects.filter(completedJob = False)
    data =[]

    for jobs in dataJobs:
        newData = json.loads(jobs.machData)
        data2 = {}
       
        for x in newData:
            res = list(x.keys())[0]
            data2['Name'] =  res
            data2['Start'] = datetime.fromisoformat(x[res]['start'])
            data2['End Time'] = datetime.fromisoformat(x[res]['end'])
            data2['Order'] = "Order " + str(x[res]['order'])
            data2['Color'] = "Order " + str(x[res]['order']) 
            data2['Resource'] = jobs.proccess.name + " for order: " + str(x[res]['order']) + " - using " + x[res]['worker'] #newData[x]['quant']
            data2['info'] = x[res]['info']
            data2['text'] = "<a href=\"https://plot.ly/\">Edit</a>"
            copyDict = data2.copy()  # copy to make possible to append
            data.append(copyDict)

    gantt_data = data
    #create initial frame for gantt chart data
    df = pd.DataFrame(gantt_data)
    #cm = {x:x for x in df.Color.unique()}
    now =datetime.now()
    fig1 =px.timeline(df, x_start="Start", x_end="End Time", y="Name", color="Color",  hover_name = "Resource", labels = "Name", title= "Gantt chart of machines plot", text = "text")

    fig1.update_traces(width=0.61)
    fig1.update_xaxes(
        rangeslider_visible=True,
        rangebreaks=[
            #dict(bounds=["sat", "mon"]),  # hide weekends, eg. hide sat to before mon
            dict(bounds=[18, 24], pattern="hour"),  # hide hours outside of 9.30am-4pm
            dict(bounds=[2, 9], pattern="hour"),],
        dtick=3600000,
        tickformat="%H:%M\n%d-%m-%y",
        showgrid=True, 
        ticklabelmode="period"
    )
    fig1.update_yaxes(autorange="reversed")
    plot_div = plot(fig1, output_type='div')
    #= plot({'data': graphs, 'layout': layout},output_type='div')
    context={'plot_div': plot_div}
    return render(request, 'schedule/schedulePlot.html', context)


def worker_plot_view(request):
    # {'seconds': x, 'start': timeFinal[index], 'end': finishTime[index], 'automated': auto, 
    #'endSetUp': timeSetUpend[index], 'startPost': timeStartPost[index], 'order': firstOrderPk}
    num = updateTimesByCreated()
    #data automatically set by project
    dataJobs = job.objects.filter(completedJob = False)
    data =[]
    for jobs in dataJobs:
        if jobs.proccess.automated:
            newData = json.loads(jobs.workData)
            data2 = {}
            for x in newData:
                res = list(x.keys())[0]
                data2['Name'] =  res + " starts pre process for " + jobs.proccess.name + " - on " + x[res]['mach']
                data2['worker'] = res
                data2['Start'] = datetime.fromisoformat(x[res]['start'])
                data2['End Time'] = datetime.fromisoformat(x[res]['endSetUp'])
                data2['Order'] = "Order " + str(x[res]['order'])
                data2['Color'] = "Order " + str(x[res]['order']) 
                data2['Resource'] = 1 #newData[x]['quant']
                copyDict = data2.copy()  # copy to make possible to append
                data.append(copyDict)
                data2 = {}
                data2['Name'] =  res + " starts post process for " + jobs.proccess.name + " - on " + x[res]['mach']
                data2['worker'] = res
                data2['Start'] = datetime.fromisoformat(x[res]['startPost'])
                data2['End Time'] = datetime.fromisoformat(x[res]['end'])
                data2['Order'] = "Order " + str(x[res]['order'])
                data2['Color'] = "Order " + str(x[res]['order']) 
                data2['Resource'] = 1 #newData[x]['quant']
                copyDict = data2.copy()  # copy to make possible to append
                data.append(copyDict)
        else:
            newData = json.loads(jobs.workData)
            data2 = {}
            for x in newData:
                res = list(x.keys())[0]
                data2['Name'] =  res + " starts " + jobs.proccess.name + " on " + x[res]['mach']
                data2['worker'] = res
                data2['Start'] = datetime.fromisoformat(x[res]['start'])
                data2['End Time'] = datetime.fromisoformat(x[res]['end'])
                data2['Order'] = "Order " + str(x[res]['order'])
                data2['Color'] = "Order " + str(x[res]['order']) 
                data2['Resource'] = 1 #newData[x]['quant']
                copyDict = data2.copy()  # copy to make possible to append
                data.append(copyDict)

    gantt_data = data

    #create initial frame for gantt chart data
    df = pd.DataFrame(gantt_data)
    cm = {x:x for x in df.Color.unique()}
    fig1 =px.timeline(df, x_start="Start", x_end="End Time", y="worker", color="Color",  hover_name = "Name", labels = "Name")
    fig1.update_yaxes(autorange="reversed")
    fig1.update_traces(width=0.61)
    plot_div = plot(fig1, output_type='div')
    #= plot({'data': graphs, 'layout': layout},output_type='div')
    context={'plot_div': plot_div}
    return render(request, 'schedule/schedulePlot.html', context)



app = DjangoDash('SimpleExample')   # replaces dash.Dash

app.layout = html.Div([
    html.H4('Graph title'),
    dcc.Graph(id="time-series-chart"),
    html.P("Select day:"),
    dcc.Dropdown(
        id="ticker",
        options=["Day 1", "Day 2", "Day 3"],
        value="Day 1",
        clearable=False,
    ),
])

@app.callback(
    Output("time-series-chart", "figure"), 
    Input("ticker", "value"))

def display_time_series(ticker):
    df = worker_plot_view_V2(ticker) # replace with your own data source
    fig = px.line(df, x='date', y=ticker)
    return fig


def worker_plot_view_V2(ticker):
    # {'seconds': x, 'start': timeFinal[index], 'end': finishTime[index], 'automated': auto, 
    #'endSetUp': timeSetUpend[index], 'startPost': timeStartPost[index], 'order': firstOrderPk}
    num = updateTimesByCreated()
    daynow = datetime.now()
    #data automatically set by project
    dataJobs = job.objects.filter(completedJob = False)
    data_1 =[]
    data_2 =[]
    data_3 =[]
    data_4 =[]
    for jobs in dataJobs:
        if jobs.proccess.automated:
            newData = json.loads(jobs.workData)
            data2 = {}
            for x in newData:
                res = list(x.keys())[0]
                data2['Name'] =  res + " starts pre process for " + jobs.proccess.name + " - on " + x[res]['mach']
                data2['worker'] = res
                data2['Start'] = datetime.fromisoformat(x[res]['start'])
                data2['End Time'] = datetime.fromisoformat(x[res]['endSetUp'])
                data2['Order'] = "Order " + str(x[res]['order'])
                data2['Color'] = "Order " + str(x[res]['order']) 
                data2['Resource'] = 1 #newData[x]['quant']
                copyDict = data2.copy()  # copy to make possible to append
                data3 = {}
                data3['Name'] =  res + " starts post process for " + jobs.proccess.name + " - on " + x[res]['mach']
                data3['worker'] = res
                data3['Start'] = datetime.fromisoformat(x[res]['startPost'])
                data3['End Time'] = datetime.fromisoformat(x[res]['end'])
                data3['Order'] = "Order " + str(x[res]['order'])
                data3['Color'] = "Order " + str(x[res]['order']) 
                data3['Resource'] = 1 #newData[x]['quant']
                copyDict2 = data3.copy()  # copy to make possible to append
                if data2['Start'].day == daynow.day:
                    data_1.append(copyDict2)
                    data_1.append(copyDict)
                elif data2['Start'] == (daynow + timedelta(1)).day:
                    data_2.append(copyDict2)
                    data_2.append(copyDict)
                elif data2['Start'] == (daynow + timedelta(2)).day:
                    data_3.append(copyDict2)
                    data_3.append(copyDict)
                else:
                    data_4.append(copyDict2)
                    data_4.append(copyDict)
        else:
            newData = json.loads(jobs.workData)
            data2 = {}
            for x in newData:
                res = list(x.keys())[0]
                data2['Name'] =  res + " starts " + jobs.proccess.name + " on " + x[res]['mach']
                data2['worker'] = res
                data2['Start'] = datetime.fromisoformat(x[res]['start'])
                data2['End Time'] = datetime.fromisoformat(x[res]['end'])
                data2['Order'] = "Order " + str(x[res]['order'])
                data2['Color'] = "Order " + str(x[res]['order']) 
                data2['Resource'] = 1 #newData[x]['quant']
                copyDict = data2.copy()  # copy to make possible to append
                data_1.append(copyDict)

    gantt_data_1 = data_1
    gantt_data_2 = data_2
    gantt_data_3 = data_3
    gantt_data_4 = data_4
    #create initial frame for gantt chart data
    df1 = pd.DataFrame(gantt_data_1)
    df2 = pd.DataFrame(gantt_data_2)
    df3 = pd.DataFrame(gantt_data_3)
    df4 = pd.DataFrame(gantt_data_4)
    dt = df1
    if ticker == "Day 1":
        df = df1
    elif ticker == "Day 2":
        df = df2
    elif ticker == "Day 3":
        df = df3
    elif ticker == "Day 4":
        df = df4

    fig1 =px.timeline(df, x_start="Start", x_end="End Time", y="worker", color="Color",  hover_name = "Name", labels = "Name")
    fig1.update_yaxes(autorange="reversed")
    fig1.update_traces(width=0.61)
    plot_div = plot(fig1, output_type='div')
    #= plot({'data': graphs, 'layout': layout},output_type='div')
    context={'plot_div': plot_div}
    
    return fig1