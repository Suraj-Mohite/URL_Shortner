from django.contrib import admin
from django.urls import path, include
from Services.views import redirect_to_target_page
from .views import HomePage

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomePage, name='home_page'),
    path("auth/", include('Accounts.urls')),
    path("dashboard/", include('Services.urls')),
    path("<str:alias>/", redirect_to_target_page, name='redirect to target page'),
]
