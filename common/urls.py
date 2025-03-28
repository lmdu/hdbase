from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
	path('signin', views.sign_in, name='signin'),
	path('signup', views.sign_up, name='signup'),
	path('signout', views.sign_out, name='signout'),
	path('signvalid', views.sign_valid, name='signvalid')
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
