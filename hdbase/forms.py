from django import forms
from django_select2 import forms as s2forms
from bootstrap_datepicker_plus.widgets import DatePickerInput
from django_jsonform.widgets import JSONFormWidget

from .models import *

class TablerModelForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		for field in self.fields.values():
			if isinstance(field.widget, forms.Select):
				field.widget.attrs['class'] = "form-select"
			else:
				field.widget.attrs['class'] = "form-control"

class PatientSelectWidget(s2forms.ModelSelect2Widget):
	search_fields = [
		'name__icontains',
		'number__icontains'
	]

class PatientForm(TablerModelForm):
	class Meta:
		model = Patient
		exclude = ['created', 'updated', 'author']
		widgets = {
			'birthday': DatePickerInput,
		}

class CardiomyopathyDiseaseForm(TablerModelForm):
	class Meta:
		model = CardiomyopathyDisease
		exclude = ['created', 'updated', 'author']
		widgets = {
			'patient': PatientSelectWidget,
			'follow_time': DatePickerInput,
			'death_time': DatePickerInput,
		}

class CardiomyopathyBloodForm(TablerModelForm):
	class Meta:
		model = CardiomyopathyBloodRoutine
		exclude = ['created', 'disease', 'author']
		widgets = {
			'tested': DatePickerInput,
		}

class CardiomyopathyMarkerForm(TablerModelForm):
	class Meta:
		model = CardiomyopathyMarker
		exclude = ['created', 'disease', 'author']
		widgets = {
			'tested': DatePickerInput,
		}

class CardiomyopathyTreatmentForm(TablerModelForm):
	class Meta:
		model = CardiomyopathyTreatment
		exclude = ['created', 'disease', 'author']
		widgets = {
			'drugs': JSONFormWidget(schema={
				'type': 'object',
				'keys': {},
				'additionalProperties': True,
			}),
			'treated': DatePickerInput,
		}

class CardiomyopathyUltrasoundForm(TablerModelForm):
	class Meta:
		model = CardiomyopathyUltrasound
		exclude = ['created', 'disease', 'author', 'dicom_uuid']
		widgets = {
			'tested': DatePickerInput,
		}

class CardiomyopathyMRIForm(TablerModelForm):
	class Meta:
		model = CardiomyopathyMRI
		exclude = ['created', 'disease', 'author', 'dicom_uuid']
		widgets = {
			'tested': DatePickerInput,
		}

class CardiomyopathyECGForm(TablerModelForm):
	class Meta:
		model = CardiomyopathyECG
		exclude = ['created', 'disease', 'author']
		widgets = {
			'tested': DatePickerInput,
		}

class CardiomyopathyGeneReportForm(TablerModelForm):
	class Meta:
		model = CardiomyopathyGeneReport
		exclude = ['created', 'disease', 'author']
		widgets = {
			'tested': DatePickerInput,
		}

class CardiomyopathyGeneMutationForm(TablerModelForm):
	class Meta:
		model = CardiomyopathyGeneMutation
		fields = '__all__'
