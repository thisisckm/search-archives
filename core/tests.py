# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 the search-archive authors and contributors
# <see AUTHORS file>
#
# This is part of search-archive and is released under

from time import time

from django.test import TestCase

from core import services
from core.exceptions import (ArchiveAlreadyExistsException,
                             ArchiveIDNotFoundException,
                             InvalidArchiveIDException)
from core.models import Archive


class ArchiveTests(TestCase):
    """
    This test cases is to test the Archive model create functionality.

    Inherit:
        TestCase
    """
    
    @classmethod
    def setUpTestData(cls):
        cls.archive_title = Archive.objects.create(archive_id=str(time()), title="title")
        cls.archive_scope_content_description = Archive.objects.create(
            archive_id=str(time()),
            scope_content_description="scope_content_description"
        )
        cls.archive_citable_reference = Archive.objects.create(
            archive_id=str(time()),
            citable_reference="citable_reference"
        )
        cls.archive_insufficient_informatiomn = Archive.objects.create(archive_id=str(time()))

    def test_archive_model(self):
        """
        Since the save method of the Archive model is override with the primary requirment
        of the this model.
        """
        
        self.assertEqual(self.archive_title.display, "title", 
                                                  "Display is not set or match the expected result")
    
        self.assertEqual(self.archive_scope_content_description.display, "scope_content_description", 
                                                  "Display is not set or match the expected result")
    
        self.assertEqual(self.archive_citable_reference.display, "citable_reference", 
                                                  "Display is not set or match the expected result")
        
        self.assertEqual(self.archive_insufficient_informatiomn.display, "Not sufficient information", 
                                                  "Display is not set or match the expected result")
        

class ServiceTests(TestCase):
    """
    These test cases are used to test the primary function of pull_from_service
    and import_archive
    Inherit:
        TestCase
    """
    
    def test_seervice_pull_from_service(self):
        """
        This test case is test the various asspect of the pull_from_service
        """
        
        with self.assertRaises(InvalidArchiveIDException) as ex: 
            services.pull_from_service("0")
        self.assertEqual(str(ex.exception), "Invaild archive id 0")
        
        with self.assertRaises(InvalidArchiveIDException) as ex: 
            services.pull_from_service(None)
        self.assertEqual(str(ex.exception), "Invaild archive id None")
        
        result = services.pull_from_service("251cd289-2f0d-48fc-8018-032400b67a56")
        expected_result = {
            "archive_id": "251cd289-2f0d-48fc-8018-032400b67a56",
            "title": "Titanic and Lusitania disasters.",
            "scope_content_description": None,
            "citable_reference": "364LWD/26/2",
        }
        self.assertEqual(result, expected_result, "Unexpected result of pull_from_service")
        
    def test_service_import_archive(self):
        """
        This test case is test the various asspect of the import_archive
        """
        
        with self.assertRaises(InvalidArchiveIDException) as ex: 
            services.import_archive("0")
        self.assertEqual(str(ex.exception), "Invaild archive id 0")
        
        with self.assertRaises(InvalidArchiveIDException) as ex: 
            services.import_archive(None)
        self.assertEqual(str(ex.exception), "Invaild archive id None")
        
        archive_id = "my-random-archive_id"
        
        with self.assertRaises(ArchiveIDNotFoundException) as ex: 
            services.import_archive(archive_id)
        self.assertEqual(str(ex.exception), f"Archive ID {archive_id} is not found")
        
        
        archive_id = "251cd289-2f0d-48fc-8018-032400b67a56"
        result = services.import_archive(archive_id)
        self.assertEqual(result, True, "Unexpected result of import_archive")

        with self.assertRaises(ArchiveAlreadyExistsException) as ex: 
            services.import_archive(archive_id)
        self.assertEqual(str(ex.exception), f"Archive {archive_id} is already imported")
