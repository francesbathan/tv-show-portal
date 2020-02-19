from django.db import models
import re
import bcrypt

class ShowManager(models.Manager): #validation for show entered
    def show_validator(self, post_data):
        errors = {}
        if len(post_data['show_title']) < 1:
            errors['show_title'] = 'Please enter a title.'
        all_title = Show.objects.filter(title=post_data['show_title']) #validator to avoid any duplicates in the database
        if len(all_title) > 0:
            errors['duplicate_title'] = "Oh no! That show is already in the portal."
        if len(post_data['show_network']) < 1:
            errors['show_network'] = 'Please enter a network.'
        if len(post_data['show_release_date']) < 1:
            errors['show_release_date'] = 'Please enter a release date.'
        if len(post_data['show_desc']) < 1:
            errors['show_desc'] = 'Please enter a description.'
        return errors

class Show(models.Model): #show database
    title = models.CharField(max_length = 255)
    network = models.CharField(max_length = 255)
    release_date = models.DateField()
    desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ShowManager()

class UserManager(models.Manager): #validation for user login/registration
    def register_validator(self, post_data): #validator for registration form
        user_errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(post_data['first_name']) < 2:
            user_errors['first_name'] = 'Please enter a valid first name.'
        if len(post_data['last_name']) < 2:
            user_errors['last_name'] = 'Please enter a valid last name.'
        if not EMAIL_REGEX.match(post_data['email']): # tests whether a field matches the pattern            
            user_errors['email'] = "Please enter a valid email address."
        all_user = User.objects.filter(username=post_data['username'])
        if len(all_user) > 0:
            user_errors['duplicate_username'] = "That username is already taken."
        if len(post_data['username']) < 6:
            user_errors['username'] = 'Username must be more than 6 characters.'
        if len(post_data['password']) < 6:
            user_errors['password'] = "Password must be more than 6 characters."
        if post_data['password'] != post_data['confirm_pw']:
            user_errors['confirm_pw'] = "Passwords do not match. Try again."
        return user_errors
    
    def login_validator(self, post_data): #validator for login form
        errors = {}
        current_user = User.objects.filter(username=post_data['username'])
        if len(current_user) < 1:
            errors['username'] = 'Username does not exist.'
        elif not bcrypt.checkpw(post_data['password'].encode(), current_user[0].password.encode()):
            errors['password'] = "Username and password do not match."
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Review(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_by = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    show = models.ForeignKey(Show, related_name='reviews', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)