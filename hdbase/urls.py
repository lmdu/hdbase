from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static

from .views import *

urlpatterns = [
	path('', index, name='index'),
	path('aboutus', aboutus, name='aboutus'),
	path('changelog', changelog, name='changelog'),
	path('validate', validate_field, name='valid-field'),
	path('upload', upload_process, name='upload-file'),
	path('browser', FileBrowseView.as_view(), name='file-browser'),
	path('select', fetch_for_select, name='fetch-select'),
	path('tasks', TaskListView.as_view(), name='list-tasks'),
	path('task/add', TaskCreateView.as_view(), name='add-task'),
	path('patients', PatientListView.as_view(), name='list-patients'),
	path('patient/add', PatientCreateView.as_view(), name='add-patient'),
	path('datasets', DatasetListView.as_view(), name='list-datasets'),
	path('dataset/add', DatasetCreateView.as_view(), name='add-dataset'),
	path('setting/website', WebsiteSettingView.as_view(), name='setting-website'),
	path('setting/global', GlobalSettingView.as_view(), name='setting-global'),
	path('setting/parameter', ParameterSettingView.as_view(), name='setting-parameter'),
	path('cardiomyopathy', CardiomyopathyListView.as_view(), name='list-cardiomyopathy'),
	path('cardiomyopathy/<int:pk>/', CardiomyopathyDetailView.as_view(), name='view-cardiomyopathy'),
	path('cardiomyopathy/add', CardiomyopathyCreateView.as_view(), name='add-cardiomyopathy'),
	path('cardiomyopathy/<int:did>/examine/add', CardiomyopathyBloodCreateView.as_view(), name='add-cardiomyopathy-examine'),
	path('cardiomyopathy/<int:did>/examine/edit/<int:pk>', CardiomyopathyBloodUpdateView.as_view(), name='edit-cardiomyopathy-examine'),
	path('cardiomyopathy/<int:did>/examine/delete/<int:pk>', CardiomyopathyBloodDeleteView.as_view(), name='delete-cardiomyopathy-examine'),
	path('cardiomyopathy/<int:did>/marker/add', CardiomyopathyMarkerCreateView.as_view(), name='add-cardiomyopathy-marker'),
	path('cardiomyopathy/<int:did>/marker/edit/<int:pk>', CardiomyopathyMarkerUpdateView.as_view(), name='edit-cardiomyopathy-marker'),
	path('cardiomyopathy/<int:did>/marker/delete/<int:pk>', CardiomyopathyMarkerDeleteView.as_view(), name='delete-cardiomyopathy-marker'),
	path('cardiomyopathy/<int:did>/treatment/add', CardiomyopathyTreatmentCreateView.as_view(), name='add-cardiomyopathy-treatment'),
	path('cardiomyopathy/<int:did>/treatment/edit/<int:pk>', CardiomyopathyTreatmentUpdateView.as_view(), name='edit-cardiomyopathy-treatment'),
	path('cardiomyopathy/<int:did>/treatment/delete/<int:pk>', CardiomyopathyTreatmentDeleteView.as_view(), name='delete-cardiomyopathy-treatment'),
	path('cardiomyopathy/<int:did>/ultrasound/add', CardiomyopathyUltrasoundCreateView.as_view(), name='add-cardiomyopathy-ultrasound'),
	path('cardiomyopathy/<int:did>/ultrasound/edit/<int:pk>', CardiomyopathyUltrasoundUpdateView.as_view(), name='edit-cardiomyopathy-ultrasound'),
	path('cardiomyopathy/<int:did>/ultrasound/delete/<int:pk>', CardiomyopathyUltrasoundDeleteView.as_view(), name='delete-cardiomyopathy-ultrasound')

]
