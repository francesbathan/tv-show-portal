from django.db import models

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