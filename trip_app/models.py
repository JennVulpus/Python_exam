from sre_constants import error
from django.db import models
import re
import bcrypt 
from datetime import datetime

class UserManager(models.Manager):
    def register_validation(self,form):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        used_email = User.objects.filter(email = form['email'])
        if len(form['first_name']) < 1:
            errors['first_name'] = 'Invalid First Name'
        if len(form['last_name']) < 1:
            errors['last_name'] = 'Invalid Last Name'
        if not EMAIL_REGEX.match(form['email']):
            errors['email'] = 'Invalid Email'
        elif used_email:
            errors['used'] = 'Email already in use'
        if len(form['password']) < 6:
            errors['password'] = 'Password should be 6 characters long'
        elif form['password'] != form['confirmpw']:
            errors['confirmpw'] = 'Passwords do not match'
        return errors
    
    def login_validation(self,form):
        errors = {}
        email = User.objects.filter(email = form['email'])
        if not email or not bcrypt.checkpw(form['password'].encode(), email[0].password.encode()):
            errors['wrong'] = 'Email or Password is wrong'
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class TripManager(models.Manager):
    def validation(self,form):
        errors = {}
        if len(form['destination']) < 1:
            errors['destination'] = 'Trip must have a destination'
        if datetime.strptime(form['start_date'], '%Y-%m-%d') < datetime.now():
            errors['start_past'] = 'Trip cannot start in the past'
        elif datetime.strptime(form['start_date'], '%Y-%m-%d') > datetime.strptime(form['end_date'], '%Y-%m-%d'):
            errors['after'] = 'Trip cannot start after it has ended'
        if datetime.strptime(form['end_date'], '%Y-%m-%d') < datetime.now():
            errors['end_past'] = 'Trip cannot end in the past'
        if len(form['plan']) < 10:
            errors['plan'] = 'Plan should be at least 10 characters'
        return errors

class Trip(models.Model):
    destination = models.CharField(max_length=60)
    owner = models.ForeignKey(User, related_name='owned_trips', on_delete=models.CASCADE)
    member = models.ManyToManyField(User, related_name='trips')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    plan = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now= True)
    objects = TripManager()
