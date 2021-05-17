from sre_constants import error
from django.http import request
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Trip
import bcrypt

def add(request):
    if not 'userid' in request.session:
        return redirect('/')
    else:
        context = {
            'user' : User.objects.get(id=request.session['userid'])
        }
        return render(request,'create.html',context)

def create(request):
    if request.method == 'POST':
        errors = Trip.objects.validation(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/add')
        else:
            Trip.objects.create(
                destination = request.POST['destination'],
                owner = User.objects.get(id=request.session['userid']),
                start_date = request.POST['start_date'],
                end_date = request.POST['end_date'],
                plan = request.POST['plan'])
            return redirect ('/dashboard')
    else:
        return redirect('/')

def dashboard(request):
    if not 'userid' in request.session:
        return redirect('/')
    else:
        context = {
            'user' : User.objects.get(id=request.session['userid']),
            'owners' : Trip.objects.filter(owner=User.objects.get(id=request.session['userid'])), #This might create a bug if user doesn't own a trip.
            'members' : Trip.objects.filter(member=User.objects.get(id=request.session['userid'])),
            'others' : Trip.objects.exclude(owner=User.objects.get(id=request.session['userid'])),
        }
        return render(request,'dashboard.html',context)

def delete(request,trip_id):
        if 'userid' in request.session:
            trip_to_delete = Trip.objects.get(id=trip_id)
            trip_to_delete.delete()
            return redirect('/dashboard')

def details(request,trip_id):
    if not 'userid' in request.session:
        return redirect ('/')
    else:
        context ={
            'user' : User.objects.get(id=request.session['userid']),
            'trip' : Trip.objects.get(id = trip_id),
        }
        return render(request,'details.html',context)

def edit(request,trip_id):
    if not 'userid' in request.session:
        return redirect('/')
    else:
        context = {
            'user' : User.objects.get(id=request.session['userid']),
            'trip' : Trip.objects.get(id = trip_id),
        }
    return render(request, 'edit.html', context)

def index(request):
    return render(request,'index.html')

def login(request):
    if request.method == 'POST':
        errors = User.objects.login_validation(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        logged_user = User.objects.filter(email = request.POST['email'])
        request.session['userid'] = logged_user[0].id
        return redirect ('/dashboard')
    else:
        return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

def register(request):
    if request.method == 'POST':
        errors = User.objects.register_validation(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            password = request.POST['password']
            hash_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            User.objects.create(
                first_name = request.POST['first_name'],
                last_name = request.POST['last_name'],
                email = request.POST['email'],
                password = hash_pw)
            request.session['userid'] = User.objects.last().id
            return redirect('/dashboard')
    else:
        return redirect('/')

def save(request, trip_id):
    if request.method == 'POST':
        errors = Trip.objects.validation(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            update_trip = Trip.objects.get(id = trip_id)
            update_trip.destination = request.POST['destination']
            update_trip.start_date = request.POST['start_date']
            update_trip.end_date = request.POST['end_date']
            update_trip.plan = request.POST['plan']
            update_trip.save()
            return redirect('/dashboard')
    else:
        return redirect('/')