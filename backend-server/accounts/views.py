from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
# request -> response

def test_hello(request):
    return HttpResponse('Test Hello World!')