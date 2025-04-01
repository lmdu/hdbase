from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static

from .views import *

urlpatterns = [
	path('', index, name='index'),
	path('task/list', TaskListView.as_view(), name='task'),
	path('task/add', TaskCreateView.as_view(), name='addtask'),
]
