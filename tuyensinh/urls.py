from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name ="index"),
    path("manage", views.manage_application, name="manage"),
    path("edit", views.ApplicationView.as_view(), name = "edit"),
    path("application/<int:id>", views.view_application, name="view"),
    path("application/<int:id>/edit", views.ApplicationView.as_view(), name="edit_admin"),
    path("upload/", views.UploadUserView.as_view(), name="upload")
]