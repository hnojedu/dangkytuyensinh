from django.urls import path

from . import views

urlpatterns = [
    path("", views.StudentIDView.as_view(), name ="index"),
    path("manage", views.manage_application, name="manage"),
    path("edit/<str:id>", views.ApplicationView.as_view(), name = "edit"),
    path("application/<str:id>", views.view_application, name="view"),
    path("application/<str:id>/<int:status>", views.view_application, name="view"),
    path("application/<str:id>/edit", views.ApplicationView.as_view(), name="edit_admin"),
    path("search", views.SearchApplicationView.as_view(), name="search"),
    path("print", views.PrintView.as_view(), name="print"),
    path("get_status/<str:ma_ho_so>", views.get_status, name="get_status"),
    path('export/', views.export_to_excel, name='export_to_excel'),
    path('toggle/', views.toggle_portal_status, name='toggle'),
    path('toggle_search/', views.toggle_search_portal_status, name='toggle_search'),
    path('upload_excel/', views.upload_excel, name = 'upload_excel'),
]

handler404 = 'tuyensinh.views.handler404'
handler500 = 'tuyensinh.views.handler500'
