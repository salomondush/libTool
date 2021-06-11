from django.http.response import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from datetime import date, datetime
from forms import *
from models import *
from functions import *
from io import StringIO
import csv


# Create your views here.
def index(request):
    # TODO: testing
    """returns landing page to choose library, and loads the libraries
    dashboard after selection
    """

    if request.method == 'GET':
        return render(request, "inventory/landing.html")

    else:

        library_name = request.POST["name"]
        

        # load librarie's dashboard
        return HttpResponseRedirect(reverse("load_library", args=(library_name,)))


def load_library(request, library_id):

    """returns all information needed to load a library including all classifications
    and a list w/ number of books done so far showing 10 of the latest scans
    pre: library name
    post: returns all information needed to land the library's dashboard
    """

    # TODO:

    context = {

    }

    return render(request, "inventory/index.html", context)


def logFile(request, library_id):
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

