from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .models import User
import types
from django.conf import settings
from django.core.files.storage import FileSystemStorage

# registers user infor if all info is valid
def register(request):
    if request.method != 'POST':
        return redirect(reverse('gym_rat:index'))
    else: 
        user = User.objects.register(request.POST)
        if isinstance(user, list):
            for error in user:
                messages.error(request, error)
            return redirect(reverse('gym_rat:index'))
        else:
            request.session['user_id'] = user.id 
            return redirect(reverse('gym_rat:dashboard'))

# logs in user if user info is valid and saves info into a session
def login(request):
    if request.method != 'POST':
        return redirect(reverse('gym_rat:index'))
    else:
        user = User.objects.login(request.POST)
        if not user:
            messages.error(request, "Invalid email or password!")
            return redirect(reverse('gym_rat:index'))
        else:
            request.session['user_id'] = user.id
            request.session['first_name'] = user.first_name
            request.session['last_name'] = user.last_name
            return redirect(reverse('gym_rat:dashboard'))

# logs out a user and deletes session containing user info
def logout(request):
    if 'workout' in request.session:
        del request.session['workout']
    User.objects.logout(request.session['user_id'])
    return redirect(reverse('gym_rat:index'))

# saves a profile picture linked to a user
def profile_pic(request):
    if request.method == 'POST' and request.FILES['profile_pic']:
        user = User.objects.get(id=request.session['user_id'])
        profile_pic = request.FILES['profile_pic']
        fs = FileSystemStorage()
        filename = fs.save(profile_pic.name, profile_pic)
        uploaded_file_url = fs.url(filename)
        user.profile_pic = uploaded_file_url
        user.save()
        context = {
            'user': user
        }
    return render(request, 'edit_profile.html', context)