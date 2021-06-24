from django.http import Http404
from django.db import IntegrityError
from io import StringIO
from pycallnumber import callnumber
import datetime
from .models import *
import csv



file_pass ="PASS"
fail="FAIL"
not_found="NOT-FOUND"
meta_call="META-CALL"
meta_ttl="META-TTL"
meta_vol = "META-VOL"
pull_stat='PULL-STAT'
pull_loc='PULL-LOC'
pull_supp="PULL-SUPP"
pull_hsup='PULL-HSUPP'
pull_due='PULL-DUE'
pull_mult='PULL-MULT'
BAR_CODE_LENGTH = 14


def compareBooks(prev_book: Book, current_book: Book, file: File):

    # use the pycallnumber library to spot books out of order
    # use a dictionary to classify books into various errors
    # build book instance and save it
    # use try block to catch "django.db.IntegrityError" in case of duplicate entry
    # return sorting data and the dictionary of classifications

    if (current_book.call_number != "" and prev_book.call_number != "") and \
            callnumber(current_book.call_number) >  callnumber(prev_book.call_number):
        file.wrong_order += 1
        current_book.inorder = False
        current_book.save()

    # check for other issues
    status = current_book.status
    
    if status == file_pass: file.file_pass += 1
    if status == not_found: file.not_found += 1
    if status == meta_call: file.meta_call += 1
    if status == meta_ttl: file.meta_ttl += 1
    if status == meta_vol: file.meta_vol += 1
    if status == pull_stat: file.pull_stat += 1
    if status == pull_loc: file.pull_loc += 1
    if status == pull_supp: file.pull_supp += 1
    if status == pull_hsup: file.pull_hsup += 1
    if status == pull_due: file.pull_due += 1
    if status == pull_mult: file.pull_mult += 1

    file.save()
    


def process_book_file(books_file, library: Library, date):

    # creating a file instance
    file = File.objects.create(
        name=books_file.name,
        library=library,
        date = date
    )


    books = books_file.read().decode('UTF-8')
    book_rows = csv.reader(StringIO(books), delimiter=',')

    # skip first line 
    next(book_rows)

    for row in book_rows:

        # if nothing in the database, we write in the first line
        if (len(file.file_books.all()) == 0 and len(Book.objects.all()) == 0) \
        and len(row[1].strip()) == BAR_CODE_LENGTH:
            Book.objects.create( # TODO: if the starting book has a status
                file=file,
                library=library,
                barCode=row[1].strip(),
                location=row[2].strip(),
                call_number= (f"{row[3]} {row[4]}").strip(),
                title=row[5],
                status=row[11].strip(),
                date= date
            )

        else:
            # we get the last book entry of the library
            prev_book = library.library_books.all().last()

            # compare it to the current entry in csv
            try:
                if (len(row[1].strip()) == BAR_CODE_LENGTH):
                    book = Book.objects.create(
                        file=file,
                        library=library,
                        barCode=row[1].strip(),
                        location=row[2].strip(),
                        call_number= (f"{row[3]} {row[4]}").strip(),
                        title=row[5],
                        status=row[11].strip(),
                        date=date
                    )

                    # call function to compare books
                    compareBooks(prev_book, book, file)

            except IntegrityError:
                pass



def get_user_emails(users):
    """Extracts email addresses from user objects
    pre: a list of user object -- users
    post: a list of email addressess 
    """
    emails = []

    for user in users:
        emails.append(user.email)

    return emails


def classify_books(books):
    """Puts books into classifications
    pre: Array of books objects
    post: count Dictionary of status codes
    """

    # all classifications
    classifications = { 
        "file_pass": 0,
        "fail": 0,
        "not_found": 0,
        "meta_call": 0,
        "meta_ttl": 0,
        "meta_vol": 0,
        "pull_stat": 0,
        "pull_loc": 0,
        "pull_supp": 0,
        "pull_hsup": 0,
        "pull_due": 0,
        "pull_mult": 0,
        "wrong_order": 0
    }

    for book in books:
        status = book.status

        if status == fail: classifications["fail"] += 1
        if status == file_pass: classifications["file_pass"] += 1
        if status == not_found: classifications["not_found"] += 1
        if status == meta_call: classifications["meta_call"] += 1
        if status == meta_ttl: classifications["meta_ttl"] += 1
        if status == meta_vol: classifications["meta_vol"] += 1
        if status == pull_stat: classifications["pull_stat"] += 1
        if status == pull_loc: classifications["pull_loc"] += 1
        if status == pull_supp: classifications["pull_supp"] += 1
        if status == pull_hsup: classifications["pull_hsup"] += 1
        if status == pull_due: classifications["pull_due"] += 1
        if status == pull_mult: classifications["pull_mult"] += 1
        if not book.inorder: classifications["wrong_order"] += 1

    return classifications

"""def xls_reader(books_file):

    if (str(books_file).endswith("xls")):
        data = xls_get(books_file, column_limit=4)
    elif (str(books_file).endswith("xls")):
        data = xlsx_get(books_file, column_limit=4)
    else:
        raise Http404("Please upload an excel file")

    print(data)"""
        



    