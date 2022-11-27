from django.shortcuts import render
from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView
from .models import product, proccessesList, proccess
from .forms import processForm, processListForma,productForm
# Create your views here.

class home(TemplateView):
    template_name = 'input/home.html'

# class orderCreateView(CreateView):
#     model = order
#     success_url = 'input.order'
#     template_name = 'input/order.html'
#     form_class = orderForm
    
#class processCreateView(CreateView):
#    model = proccess
#    success_url = 'input.process'
#    template_name = 'input/process.html'
#    form_class = processForm

class productCreateView(CreateView):
    model = product
    success_url = 'input.product'
    template_name = 'input/product.html'
    form_class = productForm

#class processListCreateView(CreateView):
#    model = proccessesList
#    success_url = 'input.processList'
#    template_name = 'input/processList.html'
#    form_class = processListForma

def processListCreateView(request):
    model = proccessesList
    context ={}
    form = processListForma(request.POST or None)
    context['form'] = form
    return render(request, "input/processList.html", context)

def processCreateView(request):
    model = proccess
    context = {}
    form = processForm(request.POST or None)
    context['form'] = form
    return render(request, "input/product.html", context)

#class listViewClass(ListView):
#    model = order
#    context_object_name = "jobs"
#    template_name = 'schedule/jobs.html'

#class jobsUpdateView(UpdateView):
#    model = jobData
#    success_url = 'schedule.home'
#    template_name = 'schedule/jobForm.html'
#    form_class = jobForm