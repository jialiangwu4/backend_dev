from django.http import Http404, HttpResponse
from django.shortcuts import render

def index(request):
    return render(request, 'files/index.html')

data = [
    {'id': 1, 'name': 'name1.jpg'},
    {'id': 2, 'name': 'name2.jpg'},
    {'id': 3, 'name': 'name3.jpg'},
    {'id': 4, 'name': 'name4.jpg'},
]


def files(request):
    return render(request, 'files/files.html', {'data': data})


def file(request, file_id):
    for d in data:
        if d.get('id')==file_id:
            return render(request,
                  'files/file.html',
                  {'file': d}
                  )
    raise Http404('No such file')