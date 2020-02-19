from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

def index(request): #homepage
    return render(request, 'index.html')

def register(request): #registration form
    return render(request, 'registration.html')

def process_registration(request): #process for registration form + validation
    form = request.POST
    errors_returned = User.objects.register_validator(form)
    if len(errors_returned) > 0:
        request.session['register_error'] = True
        for single_error in errors_returned.values():
            messages.error(request, single_error)
        return redirect('/register')
    hashed_pw = bcrypt.hashpw('test'.encode(), bcrypt.gensalt()).decode() #hashes password so it doesn't display on the database
    new_user = User.objects.create(first_name=form['first_name'], last_name=form['last_name'], email=form['email'], username=form['username'],  password=hashed_pw)
    return redirect('/shows')

def login(request): #login form
    return render(request, 'login.html')

def process_login(request): #process for login form + validation
    form = request.POST
    current_user = User.objects.filter(username=form['username']) #GETTING ERROR*****
    if len(current_user) < 1:
        request.session['register_error'] = False
        messages.error(request, 'Username does not exist.')
        return redirect('/login')
    if not bcrypt.checkpw(form['password'].encode(), current_user[0].password.encode()):
        request.session['register_error'] = False
        messages.error(request, "Username and password do not match.")
        return redirect('/login')
    return redirect('/shows')

def logout(request): #logout (***FIX so user doesn't have access to content unless they log back in.)
    request.session.clear() 
    return redirect('/')

def shows(request): #table with tv show list
    context = {
        "shows": Show.objects.all(),
        # "users": User.objects.get(id=id) #GETTING ERROR****
    }
    return render(request, 'shows.html', context)

def shows_new(request): #form
    return render(request, 'shows_new.html')

def shows_create(request): #process for form + error validation for unfilled fields
    form = request.POST
    all_errors = Show.objects.show_validator(form)
    print(all_errors)
    if len(all_errors) > 0:
        for form_error in all_errors.values():
            messages.error(request, form_error)
        return redirect('/shows/new')
    show=Show.objects.create(title=form['show_title'], network=form['show_network'], release_date=form['show_release_date'], desc=form['show_desc'])
    return redirect(f'/shows/{show.id}')

def show_info(request, id): #information regarding a show (also destination for newly added show from form)
    context = {
        "show": Show.objects.get(id=id)
    }
    return render(request, 'show_info.html', context)

def show_edit(request, id): #page containing form to edit particular show
    context = {
        "show": Show.objects.get(id=id)
    }
    return render(request, 'show_edit.html', context)

def show_update(request, id): #processes the information that went through the form and redirects to the show info page
    form = request.POST
    show=Show.objects.get(id=id)
    show.title=form['show_title']
    show.network=form['show_network']
    show.release_date=form['show_release_date']
    show.desc=form['show_desc']
    show.save()
    return redirect(f'/shows/{show.id}')

def destroy(request, id): #deletes the show from the database
    delete_show = Show.objects.get(id=id)
    delete_show.delete()
    return redirect('/shows')
