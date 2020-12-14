from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import RedirectView # <== This allows for redirecting one route to another
from django.conf import settings # <== Import Global Settings
from django.conf.urls.static import static
from catalog.views import signup, user_profile


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    re_path(r'^accounts/signup/$', signup, name="signup"),
    path('profile', user_profile, name="user-profile"),
    path('catalog/', include('catalog.urls')),
    path('', RedirectView.as_view(url='catalog/', permanent=True))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
