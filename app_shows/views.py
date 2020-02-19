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
    hashed_pw = bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt()).decode() #hashes password so it doesn't display on the database
    new_user = User.objects.create(first_name=form['first_name'], last_name=form['last_name'], email=form['email'], username=form['username'],  password=hashed_pw)
    request.session['user_id'] = new_user.id
    return redirect('/shows')

def login(request): #login form
    return render(request, 'login.html')

def process_login(request): #process for login form + validation
    form = request.POST
    login_errors = User.objects.login_validator(form)
    if len(login_errors) > 0:
        request.session['register_error'] = False
        for login_error in login_errors.values():
            messages.error(request, login_error)
        return redirect('/login')
    user_id = User.objects.get(username=form['username']).id
    request.session['user_id'] = user_id
    return redirect('/shows')

def shows(request): #table with tv show list
    if 'user_id' not in request.session:
        return redirect('/login')
    context = {
        "shows": Show.objects.all(),
        "current_user": User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'shows.html', context)

def shows_new(request): #form
    if 'user_id' not in request.session:
        return redirect('/login')
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
    if 'user_id' not in request.session:
        return redirect('/login')
    context = {
        "show": Show.objects.get(id=id)
    }
    return render(request, 'show_info.html', context)

def process_review(request, show_id):
    form = request.POST
    current_user = User.objects.get(id=request.session['user_id'])
    current_show = Show.objects.get(id=show_id)
    Review.objects.create(title=form['title'], content=form['content'], show=current_show, created_by=current_user)
    return redirect(f'/shows/{current_show.id}')

def show_edit(request, id): #page containing form to edit particular show
    if 'user_id' not in request.session:
        return redirect('/login')
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

def logout(request): #logout (***FIX so user doesn't have access to content unless they log back in.)
    request.session.clear() 
    return redirect('/login')