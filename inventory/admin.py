from django.contrib import admin
from .models import User, File, Book, Library

# Register your models here.
admin.site.register(User)
admin.site.register(Book)
admin.site.register(File)
admin.site.register(Library)
