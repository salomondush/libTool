from django.shortcuts import render

# Create your views here.
def index(request):
    """returns landing page to choose library 
    """

    return render(request, "inventory/landing.html")

def logFile(request):
    # TODO: clear up the description and function and then finish code
    """Function receives a file containing books and then creates a file instance for the current library
        - this file instance is used to bulk upload books into memory
    """

    # use: pycn.callnumber('D3.A3 A534 v.9') <  pycn.callnumber('D3 .A3 A534 v.10') when confirming files sorting

    # create a file instance
    # open file
    # loop through every row
    # use the pycallnumber library to spot books out of order
    # use a dictionary to classify books into various errors
    # build book instance and save it
    # use try block to catch "django.db.IntegrityError" in case of duplicate entry
    # return sorting data and the dictionary of classifications