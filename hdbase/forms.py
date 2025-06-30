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
		exclude = ['code', 'created', 'updated', 'author']
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
		exclude = ['code', 'created', 'updated', 'author']
		widgets = {
			'patient': PatientSelectWidget,
		}

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

class ArrhythmiaDiseaseForm(TablerModelForm):
	class Meta:
		model = ArrhythmiaDisease
		exclude = ['code', 'created', 'updated', 'author']
		widgets = {
			'sssj': DatePickerInput,
			'sfsj': DatePickerInput,
			'patient': PatientSelectWidget,
		}

class ArrhythmiaBloodForm(TablerModelForm):
	class Meta:
		model = ArrhythmiaBlood
		exclude = ['created', 'disease', 'author']
		widgets = {
			'tested': DatePickerInput,
		}

class ArrhythmiaBiochemistryForm(TablerModelForm):
	class Meta:
		model = ArrhythmiaBiochemistry
		exclude = ['created', 'disease', 'author']
		widgets = {
			'tested': DatePickerInput,
		}

class ArrhythmiaMarkerForm(TablerModelForm):
	class Meta:
		model = ArrhythmiaMarker
		exclude = ['created', 'disease', 'author']
		widgets = {
			'tested': DatePickerInput,
		}

class ArrhythmiaOtherExamineForm(TablerModelForm):
	class Meta:
		model = ArrhythmiaOtherExamine
		exclude = ['created', 'disease', 'author']

class ArrhythmiaCardiogramForm(TablerModelForm):
	class Meta:
		model = ArrhythmiaCardiogram
		exclude = ['created', 'disease', 'author']

class ArrhythmiaSurgeryForm(TablerModelForm):
	class Meta:
		model = ArrhythmiaSurgery
		exclude = ['created', 'disease', 'author']
		widgets = {
			'operated': DatePickerInput,
		}

class ArrhythmiaUltrasoundForm(TablerModelForm):
	class Meta:
		model = ArrhythmiaUltrasound
		exclude = ['created', 'disease', 'author', 'dicom_uuid']
		widgets = {
			'tested': DatePickerInput,
		}

class ArrhythmiaMRIForm(TablerModelForm):
	class Meta:
		model = ArrhythmiaMRI
		exclude = ['created', 'disease', 'author', 'dicom_uuid']
		widgets = {
			'tested': DatePickerInput,
		}

class ArrhythmiaGeneReportForm(TablerModelForm):
	class Meta:
		model = ArrhythmiaGeneReport
		exclude = ['created', 'disease', 'author']
		widgets = {
			'tested': DatePickerInput,
		}

class ArrhythmiaGeneMutationForm(TablerModelForm):
	class Meta:
		model = ArrhythmiaGeneMutation
		exclude = ['created', 'disease', 'author']

class CongenitalSurgeryDiseaseForm(TablerModelForm):
	class Meta:
		model = CongenitalSurgeryDisease
		exclude = ['code', 'created', 'updated', 'author']
		widgets = {
			'patient': PatientSelectWidget,
			'sssj': DatePickerInput,
			'sfsj': DatePickerInput,
		}

class CongenitalSurgeryPreBloodForm(TablerModelForm):
	class Meta:
		model = CongenitalSurgeryPreBlood
		exclude = ['created', 'disease', 'author']
		widgets = {
			'tested': DatePickerInput,
		}

class CongenitalSurgeryPreBiochemistryForm(TablerModelForm):
	class Meta:
		model = CongenitalSurgeryPreBiochemistry
		exclude = ['created', 'disease', 'author']
		widgets = {
			'tested': DatePickerInput,
		}

class CongenitalSurgeryPreCruorForm(TablerModelForm):
	class Meta:
		model = CongenitalSurgeryPreCruor
		exclude = ['created', 'disease', 'author']
		widgets = {
			'tested': DatePickerInput,
		}

class CongenitalSurgeryPreExamineForm(TablerModelForm):
	class Meta:
		model = CongenitalSurgeryPreExamine
		exclude = ['created', 'disease', 'author']

class CongenitalSurgeryPreLungForm(TablerModelForm):
	class Meta:
		model = CongenitalSurgeryPreLung
		exclude = ['created', 'disease', 'author']

class CongenitalSurgeryPreCardiogramForm(TablerModelForm):
	class Meta:
		model = CongenitalSurgeryPreCardiogram
		exclude = ['created', 'disease', 'author']
		widgets = {
			'tested': DatePickerInput,
		}

class CongenitalSurgeryPostPHForm(TablerModelForm):
	class Meta:
		model = CongenitalSurgeryPostPH
		exclude = ['created', 'disease', 'author']

class CongenitalSurgeryPostBloodForm(TablerModelForm):
	class Meta:
		model = CongenitalSurgeryPostBlood
		exclude = ['created', 'disease', 'author']

class CongenitalSurgeryPostLiverForm(TablerModelForm):
	class Meta:
		model = CongenitalSurgeryPostLiver
		exclude = ['created', 'disease', 'author']

class CongenitalSurgeryPostCruorForm(TablerModelForm):
	class Meta:
		model = CongenitalSurgeryPostCruor
		exclude = ['created', 'disease', 'author']

class CongenitalSurgeryPostLungForm(TablerModelForm):
	class Meta:
		model = CongenitalSurgeryPostLung
		exclude = ['created', 'disease', 'author']

class CongenitalSurgeryPostCardiogramForm(TablerModelForm):
	class Meta:
		model = CongenitalSurgeryPostCardiogram
		exclude = ['created', 'disease', 'author']
		widgets = {
			'tested': DatePickerInput,
		}

class CongenitalSurgeryOperationForm(TablerModelForm):
	class Meta:
		model = CongenitalSurgeryOperation
		exclude = ['created', 'disease', 'author']
		widgets = {
			'sssj': DatePickerInput,
		}

class CongenitalSurgeryVentilatorForm(TablerModelForm):
	class Meta:
		model = CongenitalSurgeryVentilator
		exclude = ['created', 'disease', 'author']

class CongenitalSurgeryTreatmentForm(TablerModelForm):
	class Meta:
		model = CongenitalSurgeryTreatment
		exclude = ['created', 'disease', 'author']

class CongenitalSurgeryUltrasoundForm(TablerModelForm):
	class Meta:
		model = CongenitalSurgeryUltrasound
		exclude = ['created', 'disease', 'author', 'dicom_uuid']
		widgets = {
			'tested': DatePickerInput,
		}

class CongenitalSurgeryMedimageForm(TablerModelForm):
	class Meta:
		model = CongenitalSurgeryMedimage
		exclude = ['created', 'disease', 'author', 'dicom_uuid']
		widgets = {
			'tested': DatePickerInput,
		}

class CongenitalSurgeryGeneReportForm(TablerModelForm):
	class Meta:
		model = CongenitalSurgeryGeneReport
		exclude = ['created', 'disease', 'author']
		widgets = {
			'tested': DatePickerInput,
		}

class CongenitalSurgeryGeneMutationForm(TablerModelForm):
	class Meta:
		model = CongenitalSurgeryGeneMutation
		exclude = ['created', 'disease', 'author']

class CongenitalInterveneDiseaseForm(TablerModelForm):
	class Meta:
		model = CongenitalInterveneDisease
		exclude = ['code', 'created', 'updated', 'author']
		widgets = {
			'patient': PatientSelectWidget,
			'sfsj': DatePickerInput,
		}

class CongenitalIntervenePreUltrasoundForm(TablerModelForm):
	class Meta:
		model = CongenitalIntervenePreUltrasound
		exclude = ['created', 'disease', 'author']

class CongenitalInterveneCardiogramForm(TablerModelForm):
	class Meta:
		model = CongenitalInterveneCardiogram
		exclude = ['created', 'disease', 'author']
		widgets = {
			'tested': DatePickerInput,
		}

class CongenitalInterveneOperateForm(TablerModelForm):
	class Meta:
		model = CongenitalInterveneOperate
		exclude = ['created', 'disease', 'author']
		widgets = {
			'tested': DatePickerInput,
		}

class CongenitalInterveneUltrasoundForm(TablerModelForm):
	class Meta:
		model = CongenitalInterveneUltrasound
		exclude = ['created', 'disease', 'author', 'dicom_uuid']
		widgets = {
			'tested': DatePickerInput,
		}

class CongenitalInterveneMedimageForm(TablerModelForm):
	class Meta:
		model = CongenitalInterveneMedimage
		exclude = ['created', 'disease', 'author', 'dicom_uuid']
		widgets = {
			'tested': DatePickerInput,
		}

class CongenitalInterveneGeneReportForm(TablerModelForm):
	class Meta:
		model = CongenitalInterveneGeneReport
		exclude = ['created', 'disease', 'author']
		widgets = {
			'tested': DatePickerInput,
		}

class CongenitalInterveneGeneMutationForm(TablerModelForm):
	class Meta:
		model = CongenitalInterveneGeneMutation
		exclude = ['created', 'disease', 'author']