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
		exclude = ['created', 'disease', 'author']

class KawasakiDiseaseForm(TablerModelForm):
	class Meta:
		model = KawasakiDisease
		exclude = ['created', 'updated', 'author']

class KawasakiBloodForm(TablerModelForm):
	class Meta:
		model = KawasakiBlood
		exclude = ['created', 'disease', 'author']
		widgets = {
			'tested': DatePickerInput,
		}

class KawasakiBiochemistryForm(TablerModelForm):
	class Meta:
		model = KawasakiBiochemistry
		exclude = ['created', 'disease', 'author']
		widgets = {
			'tested': DatePickerInput,
		}

class KawasakiMarkerForm(TablerModelForm):
	class Meta:
		model = KawasakiMarker
		exclude = ['created', 'disease', 'author']
		widgets = {
			'tested': DatePickerInput,
		}

class KawasakiOtherExamineForm(TablerModelForm):
	class Meta:
		model = KawasakiOtherExamine
		exclude = ['created', 'disease', 'author']

class KawasakiTreatmentForm(TablerModelForm):
	class Meta:
		model = KawasakiTreatment
		exclude = ['created', 'disease', 'author']

class KawasakiCardiacPhenotypeForm(TablerModelForm):
	class Meta:
		model = KawasakiCardiacPhenotype
		exclude = ['created', 'disease', 'author']

class KawasakiUltrasoundForm(TablerModelForm):
	class Meta:
		model = KawasakiUltrasound
		exclude = ['created', 'disease', 'author']
		widgets = {
			'tested': DatePickerInput,
		}

class KawasakiMedimageForm(TablerModelForm):
	class Meta:
		model = KawasakiMedimage
		exclude = ['created', 'disease', 'author']
		widgets = {
			'tested': DatePickerInput,
		}

class KawasakiGeneReportForm(TablerModelForm):
	class Meta:
		model = KawasakiGeneReport
		exclude = ['created', 'disease', 'author']
		widgets = {
			'tested': DatePickerInput,
		}

class KawasakiGeneMutationForm(TablerModelForm):
	class Meta:
		model = KawasakiGeneMutation
		exclude = ['created', 'disease', 'author']