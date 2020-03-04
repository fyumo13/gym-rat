from django.conf.urls import url
from . import views

app_name = 'gym_rat'

urlpatterns = [
    # displays user login page
    url(r'^$', views.index, name='index'),
    # displays user dashboard
    url(r'^dashboard$', views.dashboard, name='dashboard'),
    # displays page where user can update their own profile
    url(r'^user_profile$', views.user_profile, name='user_profile'),
    # updates current user profile
    url(r'edit_profile$', views.edit_profile, name='edit_profile'),
    # displays exercise database
    url(r'^exercises$', views.exercises, name='exercises'),
    # displays exercise-specific page
    url(r'^exercises/(?P<id>\d+)$', views.exercise, name='exercise'),
    # searches for a specific exercise in the database
    url(r'^search$', views.search, name='search'),
    # creates new workout
    url(r'^create$', views.create, name='create'),
    # displays previous workout
    url(r'^workout/(?P<id>\d+)$', views.show_workout, name='show_workout'),
    # add sets of a specific exercise to the current workout
    url(r'^add_set/(?P<id>\d+)$', views.add_set, name='add_set'),
    # updates a specific set for the current workout
    url(r'^edit_set/(?P<id>\d+)$', views.edit_set, name='edit_set'),
    # deletes a specific set for the current workout
    url(r'^del_set/(?P<id>\d+)$', views.del_set, name='del_set'),
    # completes the current workout
    url(r'^finish$', views.finish, name='finish'),
    # updates the chosen workout
    url(r'^edit_workout/(?P<id>\d+)$', views.edit_workout, name='edit_workout'),
    # deletes the chosen workout
    url(r'^del_workout/(?P<id>\d+)$', views.del_workout, name='del_workout')
]