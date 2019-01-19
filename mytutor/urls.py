from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from mytutor import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^account/', include('accounts.urls', namespace='accounts')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
