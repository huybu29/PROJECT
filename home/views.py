from django.shortcuts import render
from .forms import RegistrationForm
from django.http import HttpResponseRedirect

 # Create your views here.
def index(request):
  return render(request, 'pages/product.html')
def body(request):
  return render(request, 'pages/body.html')
def register(request):
  form = RegistrationForm()
  if request.method =='POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      form.save()
      return HttpResponseRedirect('/blog/')
  return render(request,'pages/register.html', {'form':form}) 
