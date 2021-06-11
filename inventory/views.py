from django.http.response import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from datetime import date, datetime
from .forms import UploadFileForm
from .models import *
from .functions import *
from io import StringIO
import csv


# Create your views here.
def index(request):
    # TODO: testing
    """returns landing page to choose library, and loads the libraries
    dashboard after selection
    """

    if request.method == 'GET':

        # get availabe library instances
        libraries = Library.objects.all()

        return render(request, "inventory/landing.html", {
            "libraries": libraries
        })

    else:

        library_id = int(request.POST["library"])

        # load librarie's dashboard
        return HttpResponseRedirect(reverse("load_library", args=(library_id,)))


def load_library(request, library_id):

    """returns all information needed to load a library including all classifications
    and a list w/ number of books done so far showing 10 of the latest scans
    pre: library name
    post: returns all information needed to land the library's dashboard
    """

    # library instance
    try:
        library = Library.objects.get(pk=library_id)
    except Library.DoesNotExist:
        raise Http404("Library with ID does not exist")

    # all classifications
    classifications = {
        "file_pass": library.objects.filter(status=file_pass).count(), 
        "fail": library.objects.filter(status=fail).count(), 
        "meta_call": library.objects.filter(status=meta_call).count(), 
        "meta_ttl": library.objects.filter(status=meta_ttl).count(), 
        "meta_vol": library.objects.filter(status=meta_vol).count(), 
        "pull_stat": library.objects.filter(status=pull_stat).count(), 
        "pull_loc": library.objects.filter(status=pull_loc).count(), 
        "pull_supp": library.objects.filter(status=pull_supp).count(), 
        "pull_hsup": library.objects.filter(status=pull_hsup).count(), 
        "pull_due": library.objects.filter(status=pull_due).count(), 
        "pull_mult": library.objects.filter(status=pull_mult).count(), 
    }

    context = {
        "files_num": library.files.count(),
        "books_scanned": library.library_books.order_by("-date"),
        "classifications": classifications
    }

    return render(request, "inventory/index.html", context)


def log_file(request, library_id):
    # TODO: clear up the description and function and then finish code
    # TODO: testing
    """Function receives a file containing books and then creates a file instance for the current library
        - this file instance is used to bulk upload books into memory
    """


    # get a library instance
    try:
        library = Library.objects.get(pk=library_id)
    except Library.DoesNotExist:
        raise Http404("Library with current id unavailable!")


    if request.method == 'GET':
        form = UploadFileForm()
        form.date = datetime.date.today()
        form.library = library.name
        

        return render(request, "inventory/upload.html", {
            "form": form
        })

    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
        books_file = request.FILES['file']
        date = form.changed_data['date']
        
        process_book_file(books_file, library, date)

        # reload library dashboard
        return HttpResponseRedirect(reverse("load_library", args=(library.id,)))

