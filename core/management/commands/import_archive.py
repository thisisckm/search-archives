# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 the search-archive authors and contributors
# <see AUTHORS file>
#
# This is part of search-archive and is released under


from django.core.management.base import BaseCommand
from core import services
from core.exceptions import ArchiveAlreadyExistsException, ArchiveIDNotFoundException

class Command(BaseCommand):
    
    help = "Import the archive details from National Archive services"
    "for the given archive id"

    
    def add_arguments(self, parser) -> None:
         parser.add_argument('id', type=str, help="Valid archive id")
    
    def handle(self, *args, **kwargs) -> None:
        
        self.stdout.write('Archive import started')
        archive_id = kwargs['id']
        try:
            if services.import_archive(archive_id):
                self.stdout.write('Archive import completed')
        except ArchiveAlreadyExistsException as ex:
            self.stdout.write(f"Archive ID {archive_id} is already imported")
        except ArchiveIDNotFoundException as ex:
            self.stdout.write(f"Archive ID {archive_id} is not found")
        except Exception as ex:
            self.stdout.write("Unexpected exceptions")
        