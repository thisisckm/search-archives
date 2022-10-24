from django.db import models

class Archive(models.Model):
    
    display = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    scope_content_description = models.CharField(max_length=200)
    citable_reference = models.CharField(max_length=200)
