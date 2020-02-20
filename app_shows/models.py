from django.db import models
import re
import bcrypt


class UserManager(models.Manager): #validation for user login/registration
    def register_validator(self, post_data): #validator for registration form
        user_errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(post_data['first_name']) < 2: #if first name is less than 2 characters
            user_errors['first_name'] = 'Please enter a valid first name.'
        if len(post_data['last_name']) < 2: #if last name is less than 2 characters
            user_errors['last_name'] = 'Please enter a valid last name.'
        if not EMAIL_REGEX.match(post_data['email']): # tests whether a field matches the pattern
            user_errors['email'] = "Please enter a valid email address."
        all_user = User.objects.filter(username=post_data['username']) #defines variable for specific user
        if len(all_user) > 0: #if they are using a username that is already in the system
            user_errors['duplicate_username'] = "That username is already taken." #display this error message
        if len(post_data['username']) < 6: #if username is less than 6 characters
            user_errors['username'] = 'Username must be more than 6 characters.' #error message for username less than 6 characters
        if len(post_data['password']) < 6: #if password is less than 6 characters
            user_errors['password'] = "Password must be more than 6 characters." #error message for password less than 6 characters
        if post_data['password'] != post_data['confirm_pw']: #checks if password and confirm password match
            user_errors['confirm_pw'] = "Passwords do not match. Try again."
        return user_errors
    
    def login_validator(self, post_data): #validator for login form
        errors = {}
        current_user = User.objects.filter(username=post_data['username']) #defines variable for user
        if len(current_user) < 1: #checks if username is in the database and matches user input
            errors['username'] = 'Username does not exist.'
        elif not bcrypt.checkpw(post_data['password'].encode(), current_user[0].password.encode()): #takes in what user puts in the password field and checks if password matches with username in the database
            errors['password'] = "Username and password do not match."
        return errors

class ShowManager(models.Manager): #validation for show entered
    def show_validator(self, post_data):
        errors = {} 
        if len(post_data['show_title']) < 1:
            errors['show_title'] = 'Please enter a title.'
        all_title = Show.objects.filter(title=post_data['show_title']) #validator to avoid any duplicates in the database
        if len(all_title) > 0: #checks if a title already exists in the database
            errors['duplicate_title'] = "Oh no! That show is already in the portal."
        if len(post_data['show_network']) < 1: #if the network is less than 1 character
            errors['show_network'] = 'Please enter a network.' #error message for network 
        if len(post_data['show_release_date']) < 1: #if user does nto enter a release date for the show
            errors['show_release_date'] = 'Please enter a release date.' #error message for release date
        if len(post_data['show_desc']) < 1: #if user does not enter a description
            errors['show_desc'] = 'Please enter a description.' #error message for description
        return errors

class User(models.Model): #class for the user
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Show(models.Model): #show database
    title = models.CharField(max_length = 255)
    network = models.CharField(max_length = 255)
    release_date = models.DateField()
    desc = models.TextField()
    users_who_like = models.ManyToManyField(User, related_name='liked_shows')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ShowManager()


class Review(models.Model): #class for the review and reviews created by a specific user
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_by = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    show = models.ForeignKey(Show, related_name='reviews', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)