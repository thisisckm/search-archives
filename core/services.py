# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 the search-archive authors and contributors
# <see AUTHORS file>
#
# This is part of search-archive and is released under

import re
import requests
from django.db import OperationalError
from django.db.utils import IntegrityError

from core.exceptions import (ArchiveAlreadyExistsException,
                             ArchiveIDNotFoundException,
                             InvalidArchiveIDException)
from core.models import Archive

base_url = "http://discovery.nationalarchives.gov.uk/API/records/v1/details/"

TAG_RE = re.compile(r'<[^>]+>')

def pull_from_service(archive_id: str) -> dict:
    """Pull the archive details from the National Archive 
    for the given archive_id

    Args:
        archive_id (str): Valid archive id

    Raises:
        InvalidArchiveIDException: This exceptions is rised if the archive is invalid (0 or None)

    Returns:
        dict: Return a dict of archive_id, title, scope_content_description, and citable_reference
    """
    if archive_id == "0" or archive_id is None:
        raise InvalidArchiveIDException(archive_id)
    
    return_value = {}
    
    reponse = requests.get(f"{base_url}{archive_id}")
    if reponse.status_code == 200:
        json_reponse = reponse.json()
        return_value['archive_id'] = json_reponse.get('id', None)
        return_value['title'] = json_reponse.get('title', None)
        scope_content_description = json_reponse.get('scopeContent', None) \
                                                    and json_reponse['scopeContent'].get('description', None)
        return_value['scope_content_description'] = scope_content_description and TAG_RE.sub('', scope_content_description)
        return_value['citable_reference'] = json_reponse.get('citableReference', None)
    
    return return_value
    
def import_archive(archive_id: str) -> bool:
    """Store the archive details into Archive model. The details are which pulled from the
    National Archive service using pull_from_service 

    Args:
        archive_id (str): Valid archive id

    Raises:
        InvalidArchiveIDException: This exceptions is rised if the archive is invalid (0 or None)
        ArchiveAlreadyExistsException: If the archive is import already, then this exceptions is rised
        ArchiveIDNotFoundException: If the archive id is not found on the National Archive service, 
                                    then this exceptions is rised

    Returns:
        bool: _description_
    """
        
    result = pull_from_service(archive_id)
    if result:
        try:
            Archive.objects.create(**result)
            return True
        except IntegrityError as ex:
            if ex.args[0] == 1062:
                raise ArchiveAlreadyExistsException(archive_id)
            raise ex
        except OperationalError as ex:
            raise ex
    else:
        raise ArchiveIDNotFoundException(archive_id)
