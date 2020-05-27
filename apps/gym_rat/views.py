from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .models import Exercise, Set, Workout
from ..login_registration.models import User
import types 
import datetime

# displays user login/registration page
def index(request):
    return render(request, 'index.html')

# displays user dashboard with current user's profile info and list of workouts the user has completed
def dashboard(request):
    user = User.objects.get(id=request.session['user_id'])
    try:
        workouts = Workout.objects.filter(user=request.session['user_id']).order_by('created_at')
    except Workout.DoesNotExist:
        workouts = None
    today = datetime.date.today()
    age = (today - user.birthdate) / 365
    if user.height:
        feet = int(user.height / 12)
        inches = user.height % 12
        height = "{}'{}\"".format(feet, inches)
    else:
        height = None
    context = {
        'user': user,
        'workouts': workouts,
        'age': age.days,
        'height': height
    }
    return render(request, 'dashboard.html', context)

# displays page where user can update their own profile
def user_profile(request):
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user
    }
    return render(request, 'edit_profile.html', context)

# updates current user's profile
def edit_profile(request):
    user = User.objects.get(id=request.session['user_id'])
    if request.POST['first_name']:
        user.first_name = request.POST['first_name']
    if request.POST['last_name']:
        user.last_name = request.POST['last_name']
    if request.POST['current_weight']:
        user.current_weight = request.POST['current_weight']
    if request.POST['goal_weight']:
        user.goal_weight = request.POST['goal_weight']
    if request.POST['height_ft'] and request.POST['height_in']:
        user.height = (int(request.POST['height_ft']) * 12) + int(request.POST['height_in'])
    if 'gender' in request.POST:
        user.gender = request.POST['gender']
    user.save()
    return redirect('gym_rat:dashboard')

# displays exercise database listed alphabetically
def exercises(request):
    exercises = Exercise.objects.all().order_by('name')
    context = {
        'exercises': exercises
    }
    return render(request, 'exercises.html', context)

# displays page with name and description of specific exercise
# allows user to add exercise to their current workout
def exercise(request, id):
    exercise = Exercise.objects.get(id=id)
    if 'workout' in request.session:
        sets = Set.objects.filter(exercise=id, workout=request.session['workout']).order_by('created_at')
    else:
        sets = None
    context = {
        'exercise': exercise,
        'sets': sets
    }
    return render(request, 'exercise.html', context)

# searches for a specific exercise in the database
def search(request):
    exercises = Exercise.objects.filter(name__icontains=request.GET['search']).order_by('name')
    context = {
        'exercises': exercises
    }
    return render(request, 'exercises.html', context)

# creates a new workout for the current user
def create(request):
    workout = Workout.objects.add_workout(request.session['user_id'])
    request.session['workout'] = workout.id
    return redirect('gym_rat:show_workout', id=workout.id)

# displays selected workout list
def show_workout(request, id):
    workout = Workout.objects.get(id=id)
    sets = Set.objects.filter(workout_id=workout.id).order_by('created_at')
    context = {
        'workout': workout,
        'sets': sets
    }
    return render(request, 'workout.html', context)

# adds sets of a specific exercise to the current workout
def add_set(request, id):
    if request.method != 'POST':
        return redirect('gym_rat:exercise', id=id)
    else:
        Set.objects.add_sets(id, request.session['workout'], request.POST)
        return redirect('gym_rat:exercise', id=id)

# updates a specific set for the current workout
def edit_set(request, id):
    edit_set = Set.objects.get(id=id)
    edit_set.weight = request.POST['weight']
    edit_set.reps = request.POST['reps']
    edit_set.save()
    return redirect('gym_rat:exercise', id=edit_set.exercise.id)

# deletes a specific set for the current workout
def del_set(request, id):
    Set.objects.get(id=id).delete()
    return redirect('gym_rat:show_workout', id=request.session['workout'])

# completes the current workout
def finish(request):
    workout = Workout.objects.get(id=request.session['workout'])
    del request.session['workout']
    return redirect('gym_rat:show_workout', id=workout.id)

# updates the chosen workout
def edit_workout(request, id):
    workout = Workout.objects.get(id=id)
    request.session['workout'] = workout.id
    return redirect('gym_rat:show_workout', id=workout.id)

# deletes the chosen workout
def del_workout(request, id):
    Workout.objects.get(id=id).delete()
    if 'workout' in request.session:
        del request.session['workout']
    return redirect('gym_rat:dashboard')