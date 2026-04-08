

from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return render(request, 'shop/index.html')

def about(request):
    return HttpResponse("We are in about")

def contact(request):
    return HttpResponse("We are in contact")


def tracker(request):
    return HttpResponse("We are in tracker")

def search(request):
    return HttpResponse("We are in contact")

def productView(request):
    return HttpResponse("We are in productview")

def checkOut(request):
    return HttpResponse("We are going to do checkout")




