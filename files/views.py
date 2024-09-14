from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request, 'files/index.html')

data = [
    {'name': 'name1.jpg'},
    {'name': 'name2.jpg'},
    {'name': 'name3.jpg'},
    {'name': 'name4.jpg'},
]


def files(request):
    return render(request, 'files/files.html', {'data': data})