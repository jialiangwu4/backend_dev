from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from files.forms import UploadForm
from files.models import File
from django.conf import settings

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
    
    try: 
        file = File.objects.get(pk=file_id)
    except File.DoesNotExist:
        raise Http404('File not found')
    
    # update the current file name and type 
    if new_name:
        file.name = new_name
    
    # save the updated file
    file.save()
    
    return redirect('files')

def delete(request, file_id):
    try: 
        file = File.objects.get(pk=file_id)
    except File.DoesNotExist:
        raise Http404('File not found')
    
    file.delete()
    return redirect('files')   
    
def upload(request):
    return render(request, 'files/upload.html', {'form': UploadForm})

def create(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            # this setting enable users to download contents cross site, i.e., not from the same server. (files are hosted in S3, server is on EC2)
            settings.AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400', 'ContentDisposition': 'attachment; filename="' + request.FILES['file'].name + '"'}
            form.save()
    
    return redirect('files')    
    
    