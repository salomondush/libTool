from django.db import models
from django.contrib.auth.models import AbstractUser

from datetime import date
# Create your models here.

##Add more information on these models
# class User(AbstractUser):
#     phone = models.CharField(max_length=20)
#     date_of_birth = models.DateField()
#     city = models.CharField(max_length=100)
#     country = models.CharField(max_length=100, blank=True)
#     is_doctor = models.BooleanField()
#     gender = models.CharField(max_length=1, blank=True)

#     def is_valid_user(self):
#         return ((len(self.username) > 0) and (len(self.gender) > 0)
#                 and (len(self.email) > 0) and (self.date_of_birth 
#                 > date(1818, 1, 1)))

#     def __str__(self):
#         return f"{self.first_name} {self.last_name}"

#         #You can also use hasattr to avoid the need for exception catching:
#         #hasattr.(u, "doctor"), which returns "True" or "False"

class Library(models.Model):
    name = models.CharField(max_length=100) 
    
    def __str__(self):
        return f"{self.name}"

class File(models.Model):
    library = models.ForeignKey(Library, on_delete=models.CASCADE, related_name="files")
    date = models.DateField()
    # TODO: also list all fields and classifications, including sorting.
    wrong_order = models.IntegerField(default=0)
    file_pass = models.IntegerField(default=0)
    fail = models.IntegerField(default=0)
    meta_call = models.IntegerField(default=0)
    meta_ttl = models.IntegerField(default=0)
    meta_vol = models.IntegerField(default=0)
    pull_stat = models.IntegerField(default=0)
    pull_loc = models.IntegerField(default=0)
    pull_supp = models.IntegerField(default=0)
    pull_hsup = models.IntegerField(default=0)
    pull_due = models.IntegerField(default=0)
    pull_mult = models.IntegerField(default=0)


    
    def upload(books):
        # TODO: Finish this function
        """reads file with books and bulk uploads them
        pre: a file with books
        post: returns boolean indicating if the books were installed
        """

    def __str__(self):
        return f'{self.name} - {self.date.strftime("%m/%d/%y")}' 


class Book(models.Model):
    file = models.ForeignKey(File, delete=models.CASCADE, related_name="file_books")
    library = models.ForeignKey(Library, on_delete=models.CASCADE, related_name="library_books")
    barCode = models.CharField(max_length=100, unique=True) # to avoid duplicates
    location = models.CharField(max_length=50)
    call_number = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    inorder = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.barcode} : {self.title}"

"""Adding migrations to apps Now, run python manage.py migrate --fake-initial , 
   and Django will detect that you have an initial migration and that the tables 
   it wants to create already exist, and will mark the migration as already applied.
"""