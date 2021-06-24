from django.urls import path 
from . import views

urlpatterns = [
    path("", views.index, name="library_options"),
    path("load_library/<int:library_id>", views.load_library, name="load_library"),
    path("logFile/<int:library_id>", views.log_file, name="log_file"),
    path("files/<int:library_id>", views.load_files, name="load_files"),
    path("delete/<int:file_id>", views.delete_file, name="delete_file"),
    path("unauthorized_login", views.unauthorized_login, name="unauthorized_login"),   
]