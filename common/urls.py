from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
	path('signin', views.sign_in, name='signin'),
	path('signup', views.sign_up, name='signup'),
	path('signout', views.sign_out, name='signout'),
	path('signvalid', views.sign_valid, name='signvalid'),
	path('profile', views.ProfileUpdateView.as_view(), name='profile'),
	path('setpass', views.PasswordUpdateView.as_view(), name='setpass'),
	path('customers', views.CustomerListView.as_view(), name='list-customer'),
	path('customer/edit/<int:pk>', views.CustomerUpdateView.as_view(), name='edit-customer'),
	path('customer/delete/<int:pk>', views.CustomerDeleteView.as_view(), name='delete-customer'),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
