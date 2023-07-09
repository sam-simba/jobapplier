from django.shortcuts import render, redirect
from .models import Job, Application, Field
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, Group
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import ApplicationForm, JobPostForm
from django.contrib.auth.decorators import login_required
from datetime import datetime


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username not found in the database')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Login failed!')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    page = 'register'
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error('An error occurred during registration.')

    context = {'page': page, 'form': form}
    return render(request, 'base/login_register.html', context)


def home(request):
    fields = Field.objects.all()

    q = request.GET.get('q') if request.GET.get('q') != None else ''
    jobs = Job.objects.filter(
        Q(name__icontains=q) |
        Q(field__name__icontains=q) |
        Q(description__icontains=q)
    )

    f = request.GET.get('f') if request.GET.get('f') != None else ''
    jobs_by_field = Job.objects.filter(Q(field__name__icontains=f))

    if jobs.count() == 0:
        jobs_count = 'No'
    else:
        jobs_count = jobs.count()

    context = {'jobs': jobs, 'fields': fields, 'jobs_by_field': jobs_by_field, 'jobs_count': jobs_count}
    return render(request, 'base/home.html', context)

@login_required(login_url='login')
def userProfile(request, pk):
    user = User.objects.get(id=pk)
    jobs = Job.objects.all()

    context = {'user': user, 'jobs': jobs}
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def usersPage(request):
    users = User.objects.all()
    my_groups = Group.objects.all()
    # q = request.GET.get('q') if request.GET.get('q') != None else ""
    # users = User.objects.filter(Q(user__groups__icontains = q))

    # def is_applicant(user):
    #     return user.groups.filter(name='Applicant').exists()
    # def is_admin(user):
    #     return user.groups.filter(name='admin').exists()
    # def is_hirer(user):
    #     return user.groups.filter(name='Hirer').exists()
    

    applicants = []
    for user in users:
        # if is_applicant(user):
        if user.applicants:
            applicants.append(user)
    
    admins = []
    for user in users:
        # if is_admin(user):
        if user.is_superuser:
            admins.append(user)
    
    hirers = []
    for user in users:
        # if is_hirer(user):
        if user.groups.name == 'Hirers':
            hirers.append(user)

    groups = []
    for group in my_groups:
        groups.append(group.name.capitalize())

    context = {'users': users, 'groups': groups, 'applicants': applicants, 'admins': admins, 'hirers': hirers}
    return render(request, 'base/users.html', context)


def job(request, pk):
    job = Job.objects.get(id=pk)
    applicants = job.applicants.all()
    applications = job.application_set.all()

    my_application = None
    for application in applications:
        if request.user.id == application.applicant.id:
            my_application = application 

    context = {'job': job, 'applicants': applicants, 'applicants_count': applicants.count(), 'applications': applications, 'my_application': my_application}
    return render(request, 'base/job.html', context)

@login_required(login_url='login')
def apply(request, pk):
    job = Job.objects.get(id=pk)
    applicants = job.applicants.all()

    if request.method == 'POST':
        application = Application.objects.create(
            applicant = request.user,
            job = job,
            interest = request.POST.get('interest')
        )
        job.applicants.add(request.user)
        return redirect('job', pk=job.id)
    
    context = {'job': job, 'user': request.user, 'applicants': applicants}
    return render(request, 'base/apply.html', context)

def application(request, pk):
    application = Application.objects.get(id=pk)
    print(application)
    
    context = {'application': application}
    return render(request, 'base/application.html', context)

@login_required(login_url='login')
def deleteApplication(request, pk):
    job = Job.objects.get(id=pk)
    applicants = job.applicants.all()
    user = request.user

    if request.method == 'POST':
        job.applicants.remove(request.user)
        return redirect('job', pk=job.id)

    context = {'job': job, 'user': user, 'applicants': applicants}
    return render(request, 'base/apply.html', context)


def postJobPage(request):
    form = JobPostForm()
    user = request.user

    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.hiring_mgr = request.user
            job.save()
            return redirect('job', pk=job.id)

    context = {'form': form, 'user': user}
    return render(request, 'base/post_job.html', context)

def deleteJob(request, pk):
    job = Job.objects.get(id=pk)
    form = JobPostForm(instance=job)

    if request.method == 'POST':
        job.delete()
        return redirect('home')
    context = {'form': form}
    return render(request, 'base/delete_job.html', context)

@login_required(login_url='login')
def editJob(request, pk):
    job = Job.objects.get(id=pk)
    form = JobPostForm(instance=job)

    if request.method == 'POST':
        form = JobPostForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('job', pk=job.id)

    context = {'form': form}
    return render(request, 'base/edit_job.html', context)

def deleteApplication(request, pk):
    context = {}
    return render(request, 'base/delete_application.html', context)