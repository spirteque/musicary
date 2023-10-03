from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, "main/welcome_page.html")


def terms(request):
    return render(request, 'main/terms.html')
