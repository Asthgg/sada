
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls import url, include
from rest_framework.authtoken import views
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    url(r'', include(('Lemoncello.Apps.fraid.urls'))),
    url(r'^api/v1/auth', include('rest_framework.urls', namespace='rest_framework')),
]

#urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


