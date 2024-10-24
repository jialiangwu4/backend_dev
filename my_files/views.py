from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from .serializers import FileSerializer, UserSerializer
from .forms import UploadForm
from .models import File
import os
from urllib.parse import urlparse
import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate

def index(request):
    return render(request, 'files/index.html')

@login_required
def files(request):
    # files = File.objects.all()
    user = request.user
    if user.is_authenticated:
        files = user.file_set.all()
    return render(request, 'files/files.html', {'data': files, 'user': user})

@login_required
def file(request, file_id):
    try: 
        # file = File.objects.get(pk=file_id)
        file = request.user.file_set.get(pk=file_id)
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
    form = UploadForm()
    
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            # file = form.save(commit=False)
            # file.user = request.user
            form.save()
            
            return redirect('files')
        
    return render(request, 'files/upload.html', {'form': form})
    
    
def download_file(request, file_id):
    def _get_ext(url):
        path = urlparse(url).path
        ext = os.path.splitext(path)[1]
        return ext
    
    try: 
        file = File.objects.get(pk=file_id)
    except File.DoesNotExist:
        raise Http404('File not found')
    
    s3_url = file.file.url
    
    # use the name field as the file name for download
    file_name = file.name + _get_ext(s3_url)
    
    # use StreamingHttpResponse for larger files.
    
    # response = requests.get(s3_url, stream=True)
    
    # file_response = StreamingHttpResponse(
    #     response.iter_content(chunk_size=8192),  # Stream the file in chunks
    #     content_type=response.headers.get("Content-Type")
    # )
    # # Set the Content-Disposition header to force download, use the file name that's set by the user 
    # file_response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    
    
    # when files size are small, typically less than 10MB. use HttpResponse
    response = requests.get(s3_url)

    if response.status_code == 200:
        # Use HttpResponse to return the file content
        file_response = HttpResponse(
            response.content,  # Entire file content
            content_type=response.headers.get("Content-Type")  # Content type
        )
        # Set the Content-Disposition header to force download
        file_response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        return file_response
    
    
    return file_response



# api endpoinds

@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def files_api(request, format=None): # the format keyword is to support url suffix 
    if request.method == 'GET':
        try:
            files = request.user.file_set.all() # get files specific to that user
            # files = File.objects.all()
        except AttributeError as e:
            return Response('Please Log in', status=status.HTTP_401_UNAUTHORIZED)  
            
        serializer = FileSerializer(files, many=True)
        return Response({'files':serializer.data})

@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def file_api(request, file_id, format=None):
    # request handling for single file
    try:
        file = request.user.file_set.get(pk=file_id) # get files specific to that user
        # file = File.objects.get(pk=file_id)
    except File.DoesNotExist:
        return Response('File does not exist or you do not have permission', status=status.HTTP_404_NOT_FOUND)
    except AttributeError as e:
            return Response('Please Log in', status=status.HTTP_401_UNAUTHORIZED)  
    
    if request.method == 'GET':
        serializer = FileSerializer(file)
        return Response(serializer.data)
    
    elif request.method == 'PATCH': # use patch to update partial data
        serializer = FileSerializer(file, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        file.delete()
        return Response(status=status.HTTP_200_OK)
    

@api_view(['POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def upload_api(request, format=None):
    if request.method == 'POST':
        serializer = FileSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])        
def register_api(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)