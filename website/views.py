from django.shortcuts import render

def index(request):
    return render(request, 'website/index.html')

def about(request):
    return render(request, 'website/about.html')

def service(request):
    return render(request, 'website/service.html')

def portfolio(request):
    return render(request, 'website/portfolio.html')

def contact(request):
    return render(request, 'website/contact.html')
