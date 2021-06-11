from django.urls import path 
from . import views

urlpatterns = [
    path("", views.index, name="library_options"),
    path("load_library/<int:library_id>", views.load_library, name="load_library"),
    path("logFile/<int:library_id>", views.log_file, name="log_file")
]