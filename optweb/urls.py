from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from acftdata.views import planes_page
from main.views import about_page, index_page


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_page, name='home'),
    path('planes', planes_page, name='planes'),
    path('about', about_page, name='about')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
