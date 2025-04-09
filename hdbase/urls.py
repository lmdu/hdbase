from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static

from .views import *

urlpatterns = [
	path('', index, name='index'),
	path('validate', validate_field, name='valid-field'),
	path('upload', upload_process, name='upload-file'),
	path('browser', get_file_browser, name='file-browser'),
	path('select', fetch_for_select, name='fetch-select'),
	path('tasks', TaskListView.as_view(), name='list-tasks'),
	path('task/add', TaskCreateView.as_view(), name='add-task'),
	path('patients', PatientListView.as_view(), name='list-patients'),
	path('patient/add', PatientCreateView.as_view(), name='add-patient'),
	path('datasets', DatasetListView.as_view(), name='list-datasets'),
	path('dataset/add', DatasetCreateView.as_view(), name='add-dataset'),
]
