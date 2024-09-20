from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
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
    
def edit(request, file_id):
    new_name = request.POST.get('name')
    new_type = request.POST.get('type')
    
    try: 
        file = File.objects.get(pk=file_id)
    except File.DoesNotExist:
        raise Http404('File not found')
    
    # update the current file name and type 
    if new_name:
        file.name = new_name
        
    if new_type:
        file.file_type = new_type
    
    # save the updated file
    file.save()
    
    return redirect('files')