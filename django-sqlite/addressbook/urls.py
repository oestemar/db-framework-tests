from django.urls import path

from . import views

urlpatterns = [
    path("", views.display, name="display"),
    path("detail/<int:id>/", views.detail, name="detail"),
    path("register/", views.register, name="register"),
    path("register_csv/", views.register_csv, name="register_csv"),
    path("edit/<int:id>/", views.edit, name="edit"),
    path("delete/<int:id>/", views.delete, name="delete"),
]