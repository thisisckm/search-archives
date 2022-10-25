# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 the search-archive authors and contributors
# <see AUTHORS file>
#
# This is part of search-archive and is released under


class ArchiveAlreadyExistsException(Exception):
        
    def __init__(self, archive_id: str):
        super().__init__(f"Archive {archive_id} is already imported")


class ArchiveIDNotFoundException(Exception):
    
    def __init__(self, archive_id: str):
        super().__init__(f"Archive ID {archive_id} is not found")


class InvalidArchiveIDException(Exception):
    
    def __init__(self, archive_id: str):
        super().__init__(f"Invaild archive id {archive_id}")
