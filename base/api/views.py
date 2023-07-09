from base.models import Job, Application
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import jobSerializer, applicationSerializer
from django.http import Http404
from django.contrib.auth import login, logout, authenticate

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/jobs',
        'GET /api/job/:id',
        'GET /api/applications',
        'GET /api/applications/:id',
    ]
    return Response(routes)

@api_view(['GET'])
def getJobs(request):
    jobs = Job.objects.all()
    serializer = jobSerializer(jobs, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getJob(request, pk):
    try:
        job = Job.objects.get(id=pk)
        serializer = jobSerializer(job, many=False)
        return Response(serializer.data)
    except Job.DoesNotExist:
        raise Http404('This job does not exist!')

@api_view(['GET'])
def getApplications(request):
    applications = Application.objects.all()
    serializer = applicationSerializer(applications, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getApplication(request, pk):
    try:
        application = Application.objects.get(id=pk)
        serializer = applicationSerializer(application, many=False)
        return Response(serializer.data)
    except Application.DoesNotExist:
        raise Http404("This application doesn't exist!")

@api_view(['POST'])
def loginAPI(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        login(request, user)
        return Response({'message': 'Login successful'})
    else:
        return Response({'message': 'Invalid credentials'})

@api_view(['POST'])
def logoutAPI(request):
    logout(request)
    return Response({'message': 'Logout successful'})

