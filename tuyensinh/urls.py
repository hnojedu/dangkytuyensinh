from django.urls import path

from . import views

urlpatterns = [
    path("", views.StudentIDView.as_view(), name ="index"),
    path("manage", views.manage_application, name="manage"),
    path("edit/<str:id>", views.ApplicationView.as_view(), name = "edit"),
    path("application/<str:id>", views.view_application, name="view"),
    path("application/<str:id>/<int:status>", views.view_application, name="view"),
    path("application/<str:id>/edit", views.ApplicationView.as_view(), name="edit_admin"),
    path("search", views.SearchApplicationView.as_view(), name="search")
]

handler404 = 'tuyensinh.views.handler404'
handler500 = 'tuyensinh.views.handler500'
