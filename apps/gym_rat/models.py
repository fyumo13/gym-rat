from django.db import models
from datetime import datetime
from ..login_registration.models import User

class Exercise(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class WorkoutManager(models.Manager):
    # creates new Workout object linked to a specific user
    def add_workout(self, user):
        user = User.objects.get(id=user)
        workout = Workout.objects.create(user=user)
        return workout

class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sets = models.ManyToManyField(Exercise, through='Set')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = WorkoutManager()

    def __str__(self):
        return datetime.strftime(self.created_at, '%m/%d/%Y')

class SetManager(models.Manager):
    # creates a new Set object linked to a specific exercise and workout
    def add_sets(self, exercise_id, workout_id, postData):
        exercise = Exercise.objects.get(id=exercise_id)
        workout = Workout.objects.get(id=workout_id)
        sets = Set.objects.create(
            exercise=exercise,
            workout=workout,
            weight=postData['weight'],
            reps=postData['reps']
        )
        return sets

class Set(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    weight = models.IntegerField()
    reps = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = SetManager()

    def __str__(self):
        return self.exercise