from django.http.response import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from datetime import date
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

        library_id = request.POST["library"]

        if library_id == "None":
            return HttpResponseRedirect(reverse("library_options"))
        
        library_id = int(library_id)

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
        return render(request, "inventory/index.html", {
            "message": "Library with ID does not exist"
        })

    books = library.library_books.order_by("id")

    # call help function to classify books
    classifications = classify_books(books)

    # # all classifications
    # classifications = { 
    #     "file_pass": library.library_books.filter(status=file_pass).count(), 
    #     "not_found": library.library_books.filter(status=not_found).count(), 
    #     "meta_call": library.library_books.filter(status=meta_call).count(), 
    #     "meta_ttl": library.library_books.filter(status=meta_ttl).count(), 
    #     "meta_vol": library.library_books.filter(status=meta_vol).count(), 
    #     "pull_stat": library.library_books.filter(status=pull_stat).count(), 
    #     "pull_loc": library.library_books.filter(status=pull_loc).count(), 
    #     "pull_supp": library.library_books.filter(status=pull_supp).count(), 
    #     "pull_hsup": library.library_books.filter(status=pull_hsup).count(), 
    #     "pull_due": library.library_books.filter(status=pull_due).count(), 
    #     "pull_mult": library.library_books.filter(status=pull_mult).count(),
    #     "wrong_order": library.library_books.filter(inorder=False).count() 
    # }

    context = {
        "files_num": library.files.count(),
        "books_scanned": books,
        "classifications": classifications,
        "library": library,
        "num_books": len(books)
    }

    return render(request, "inventory/index.html", context)


@login_required(redirect_field_name="account_login", login_url="/accounts/login")
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
        return render(request, "inventory/index.html", {
            "message": "Library with current id unavailable! Please go back"
        })


    if request.method == 'GET':
        form = UploadFileForm()

        return render(request, "inventory/upload.html", {
            "form": form,
            "library": library
        })

    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
        books_file = request.FILES['file']
        date = form.cleaned_data['date']

        # check if it's a csv file
        if not books_file.name.endswith(".csv"):
            return render(request, "inventory/index.html", {
                "message": "Specified file not found, please go back!"
            })
        
        process_book_file(request, books_file, library, date)
        #xls_reader(books_file)

        return HttpResponseRedirect(reverse("load_library", args=(library.id,)))
    else:

        return render(request, "inventory/upload.html", {
            "form": form,
            "library": library,
        })

@login_required(redirect_field_name="account_login", login_url="/accounts/login")
def load_files(request, library_id):


    try:
        library = Library.objects.get(pk=library_id)
    except Library.DoesNotExist:
        return render(request, "inventory/index.html", {
            "message": "Can't find specific library, please go back!"
        })

    return render(request, "inventory/files.html", {
        "files": library.files.all(),
        "library": library
    })


@login_required(redirect_field_name="account_login", login_url="/accounts/login")
def delete_file(request, file_id):

    try:
        file = File.objects.get(pk=file_id)
        library_id = file.library.id
        file.delete()
    except File.DoesNotExist:
        return render(request, "inventory/index.html", {
            "message": "Specified file not found, please go back!"
        })

    return HttpResponseRedirect(reverse("load_files", args=(library_id,)))

    
