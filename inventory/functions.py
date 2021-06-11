from django.http import Http404
from django.db import IntegrityError
from io import StringIO
from pycallnumber import callnumber
from models import *
import csv

file_pass ="PASS", fail="FAIL", meta_call="META-CALL", meta_ttl="META-TTL"
meta_vol = "META-VOL", pull_stat='PULL-STAT', pull_loc='PULL-LOC', pull_supp="PULL-SUPP"
pull_hsup='PULL-HSUPP', pull_due='PULL-DUE', pull_mult='PULL-MULT'


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

    # check for other issues
    status = current_book.status
    
    if status == file_pass: file.file_pass += 1
    if status == fail: file.fail += 1
    if status == meta_call: file.meta_call += 1
    if status == meta_ttl: file.meta_ttl += 1
    if status == meta_vol: file.meta_vol += 1
    if status == pull_stat: file.pull_stat += 1
    if status == pull_loc: file.pull_loc += 1
    if status == pull_supp: file.pull_supp += 1
    if status == pull_hsup: file.pull_hsup += 1
    if status == pull_due: file.pull_due += 1
    if status == pull_mult: file.pull_mult += 1
    


def process_book_file(books_file, library: Library, date):
    # check if it's a csv file
    if not books_file.endswith(".csv"):
        return Http404("This is not a csv file")

    # creating a file instance
    file = File.objects.create(
        library=library,
        date = date
    )


    books = books_file.read().decode('UTF-8')
    io_string = StringIO(books)
    next(io_string) # skip first line
    
    for row in csv.reader(StringIO(books), delimeter=',', quotechar='|'):
        # if nothing in the database, we write in the first line
        if (len(file.file_books.all()) == 0):
            Book.objects.create(
                file=file,
                library=library,
                barCode=row[1].strip(),
                location=row[2].strip(),
                call_number= (f"{row[3]} {row[4]}").strip(),
                title=row[5],
                status=row[11].strip()
            )

        else:
            # we get the last entry in database
            prev_book = Book.objects.last()

            # compare it to the current entry in csv
            try:
                book = Book.objects.create(
                    file=file,
                    library=library,
                    barCode=row[1].strip(),
                    location=row[2].strip(),
                    call_number= (f"{row[3]} {row[4]}").strip(),
                    title=row[5],
                    status=row[11].strip()
                )

                # call function to compare books
                compareBooks(prev_book, book, file)

            except IntegrityError:
                pass