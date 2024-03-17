from django.shortcuts import render

def products(request):
    return render(request, 'page/products-details.html')
