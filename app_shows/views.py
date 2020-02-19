from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages

def index(request): #homepage
    return render(request, 'index.html')

def shows(request): #table with tv show list
    context = {
        "shows": Show.objects.all()
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
