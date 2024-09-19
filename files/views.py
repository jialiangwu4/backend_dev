from django.http import Http404, HttpResponse
from django.shortcuts import render
from .models import File

def index(request):
    return render(request, 'files/index.html')

def files(request):
    file = File.objects.all()
    return render(request, 'files/files.html', {'data': file})


def file(request, file_id):
    try: 
        file = File.objects.get(pk=file_id)
    except File.DoesNotExist:
        raise Http404('File not found')
        
    return render(request,
                  'files/file.html',
                  {'file': file}
                  )