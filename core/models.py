# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 the search-archive authors and contributors
# <see AUTHORS file>
#
# This is part of search-archive and is released under


from django.db import models
from django.db.models.query import QuerySet

class ArchiveManager(models.Manager):
    
    def search_archive(self, archive_id: str) -> QuerySet:
        """Search the archive details. 
        
        If the archive_id is none or empty, then top 10 lastest archive records is return.
        If the archive_id is not none or empty, then the search result is return.

        Args:
            archive_id (str): Valid archive id

        Returns:
            django.db.models.query.QuerySet:
        """
        if archive_id:
            return Archive.objects.filter(archive_id=archive_id)
        return Archive.objects.all().order_by('-id')[:10]


class Archive(models.Model):
    
    archive_id = models.CharField(max_length=200, unique=True)
    display = models.CharField(max_length=200)
    title = models.CharField(max_length=200, null=True)
    scope_content_description = models.CharField(max_length=200, null=True)
    citable_reference = models.CharField(max_length=200, null=True)
    
    objects = ArchiveManager()

    def save(self, *args, **kwargs):
        """The save method is overridden to apply the primary tasks of 
        this application
        """
        
        # if the title is not none or empty, then the display set with title 
        if self.title: 
            self.display = self.title
        # if the scopeContent.description is not none or empty, 
        # then the display set with scopeContent.description
        elif self.scope_content_description: 
            self.display = self.scope_content_description
        # if the citableReference is not none or empty, 
        # then the display set with citableReference
        elif self.citable_reference:
            self.display = self.citable_reference
        # If all the above condition fails,
        # then the display set with "Not sufficient information"
        else:
            self.display = "Not sufficient information"
            
        super(Archive, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.display
