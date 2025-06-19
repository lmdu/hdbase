from django import forms
from django_select2 import forms as s2forms
from bootstrap_datepicker_plus.widgets import DatePickerInput

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
			'tested': DatePickerInput,
		}
