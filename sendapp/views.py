from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.contrib.auth import logout as django_logout
from django.conf import settings

def welcome(request):
    return HttpResponse('Welcome to the Send-It app.')

@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)

    return render(request,'profile/profile.html',{'user':user,'profile':profile})

@login_required
def profile_edit(request,username):
    user = get_object_or_404(User, username=username)
    profile = user.profile
    form = EditProfileForm(instance=profile)
    
    if request.method == "POST":
        form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = user
            data.save()
            return HttpResponseRedirect(reverse('profile', args=[username]))
        else:
            form = EditProfileForm(instance=profile)
    legend = 'Edit Profile'
    return render(request, 'profile/update.html', {'legend':legend, 'form':EditProfileForm})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.job_title = form.cleaned_data.get('job_title')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def signin(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request,user)
        return redirect(request,'/')

    return render(request, '/django_registration/login.html')

@login_required
def logout(request):
    return HttpResponseRedirect('/')