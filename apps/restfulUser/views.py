from django.shortcuts import render
import re
from .models import User
from django.contrib import messages
from django.contrib.messages import error
from django.shortcuts import render, HttpResponse, redirect
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

def index(request):


    context = {
        'users': User.objects.all()
    }

    return render(request, 'restfulUser/index.html', context)

def new(request):
    return render(request, "restfulUser/create.html")

def create(request):
    new_user={}

    for key,value in request.POST.items():
        if key!="csrfmiddlewaretoken":
            new_user[key]=value

    message=validate(new_user)
    print new_user

    if len(message)>1:
        messages.error(request, message)
        return redirect('/users/new')

    User.objects.create(
        first_name=new_user['first_name'],
        last_name=new_user['last_name'],
        email=new_user['email'],
    )
    return redirect('/users')

def validate(user):
    error=""
    for key in user:
            if len(user[key])<2:
                error="All fields must contain more than two characters"
            elif not re.match(EMAIL_REGEX, user["email"]):
                error="Invalid Email"

    return error

def edit(request, user_id):
    context = {
        'user': User.objects.get(id=user_id)
    }
    return render(request, 'restfulUser/update.html', context)

def update(request, user_id):
    update_user={}
    for key,value in request.POST.items():
        if key!="csrfmiddlewaretoken":
            update_user[key]=value

    print update_user
    message=validate(update_user)

    if len(message)>1:
        messages.error(request, message)
        return redirect('/users/{}/edit'.format(user_id))

    user_to_update = User.objects.get(id=user_id)
    user_to_update.first_name = update_user['first_name']
    user_to_update.last_name = update_user['last_name']
    user_to_update.email = update_user['email']
    user_to_update.save()
    return redirect('/users')

def show(request, user_id):
    context = {
        'user': User.objects.get(id=user_id)
    }
    return render(request, 'restfulUser/show.html', context)


def destroy(request, user_id):
    User.objects.get(id=user_id).delete()
    return redirect('/users')
