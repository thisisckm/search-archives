from core.models import Archive
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def home(request):
    """Home page to display search result of Archive Details
    Args:
        request (_type_): 

    Returns:
        HttpResponse: return the rendered HttpResponse
    """
    context = {}

    # If no search key is enter, then list top 10 archives details
    archive_id = None
    if request.method == 'POST':
        archive_id = request.POST['search']
        if archive_id:
            context['search_key'] = archive_id
            
    context['archives'] = Archive.objects.search_archive(archive_id)
    
    return render(request, "home.html", context=context)
