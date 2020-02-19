from django.urls import path
from . import views

urlpatterns = [
    path('', views.index), #landing page
    path('shows/', views.shows), #homepage - lists shows
    path('shows/new', views.shows_new), #form to add a new show
    path('shows/create', views.shows_create), #processes add show, leads to show info
    path('shows/<int:id>', views.show_info), #path for show's info
    path('shows/<int:id>/edit', views.show_edit), #form to edit show
    path('shows/<int:id>/update', views.show_update), #processes edit show, leads to show info
    path('shows/<int:id>/destroy', views.destroy) #deletes show
]
