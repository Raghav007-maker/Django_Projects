

from django.shortcuts import render
from django.http import HttpResponse
from .models import Product
from math import ceil
# Create your views here.

def index(request):
    products = Product.objects.all()
    n = len(products)

    # Keep 4 products per carousel slide.
    nSlides = ceil(n / 4) if n else 1
    params = {'no_of_slides': nSlides, 'range': range(1, nSlides), 'product': products}
    return render(request,"shop/index.html", params)

def about(request):
    return render(request, 'shop/about.html')
    

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




