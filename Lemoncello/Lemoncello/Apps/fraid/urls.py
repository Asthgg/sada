from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from Lemoncello.Apps.fraid.views import *
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from rest_framework import routers
from django.urls import path, include

router = routers.DefaultRouter()
router.register('Events',  EventView)

urlpatterns = [
	path('api/v1/', include(router.urls)),
	url(r'^profile', profile, name='profile'),
	url(r'^login', LoginView.as_view(template_name='login.html'), name='login'),
	url(r'^logout', LogoutView.as_view(template_name='login.html'), name='logout'),
	url(r'^signup', signup, name='signup'),
	url(r'^ambient', ambient, name='ambient'),
	url(r'^dashboard', Dashboard.as_view(), name='dashboard'),
	url(r'^classifier', classifierM, name='classifier'),
	url(r'^response', response, name='response'),
    url(r'^pusher_authentication', pusher_authentication),
    url(r'^conversation$', broadcast),
    url(r'^events/$', events),
    url(r'^events/(?P<id>[-\w]+)/delivered$',alerted),
    url(r'^alerts/$', alerts),
    url(r'^alerts/(?P<id>[-\w]+)/alerted$',alerted),
]
