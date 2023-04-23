from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/',auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("", include("tuyensinh.urls")),
    path("admin/", admin.site.urls),
    path('logout/',auth_views.LogoutView.as_view(next_page='/'),name='logout'),
]