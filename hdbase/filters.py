from django import forms
from django_filters import *

from .models import *

class CardiomyopathyDiseaseFilter(FilterSet):
	code = CharFilter(
		label = "编号",
		lookup_expr='icontains',
		widget = forms.TextInput(
			attrs={'class': 'form-control form-control-sm'}
		)
	)
	disease_code = CharFilter(
		label = "测序编号",
		lookup_expr='icontains',
		widget = forms.TextInput(
			attrs={'class': 'form-control form-control-sm'}
		)
	)
	patient__name = CharFilter(
		label = "患者姓名",
		lookup_expr='icontains',
		widget = forms.TextInput(
			attrs={'class': 'form-control form-control-sm'}
		)
	)
	patient__number = CharFilter(
		label = "患者登记号",
		lookup_expr='icontains',
		widget = forms.TextInput(
			attrs={'class': 'form-control form-control-sm'}
		)
	)
	disease_type = CharFilter(
		label = "心肌病分型",
		lookup_expr='icontains',
		widget = forms.TextInput(
			attrs={'class': 'form-control form-control-sm'}
		)
	)

	mutate_gene = CharFilter(
		label = "突变基因",
		lookup_expr='icontains',
		widget = forms.TextInput(
			attrs={'class': 'form-control form-control-sm'}
		)
	)

	arrhythmia_type = CharFilter(
		label = "心律失常类型",
		lookup_expr='icontains',
		widget = forms.TextInput(
			attrs={'class': 'form-control form-control-sm'}
		)
	)

	special_treatment = ChoiceFilter(
		label = "特殊治疗",
		widget = forms.Select(
			attrs = {'class': 'form-select form-select-sm'}
		),
		choices = CardiomyopathyDisease.SPECIAL_TREATMENTS
	)

	hospital_visits__gte = NumberFilter(
		label = "心衰再入院次数>=",
		widget = forms.NumberInput(
			attrs = {'class': 'form-control form-control-sm'}
		)
	)

	class Meta:
		model = CardiomyopathyDisease
		fields = [
			'code', 'disease_code', 'patient__name',
			'patient__number', 'disease_type', 'mutate_gene',
			'arrhythmia_type'
		]

class KawasakiDiseaseFilter(FilterSet):
	code = CharFilter(
		label = "编号",
		lookup_expr='icontains',
		widget = forms.TextInput(
			attrs={'class': 'form-control form-control-sm'}
		)
	)
	disease_code = CharFilter(
		label = "测序编号",
		lookup_expr='icontains',
		widget = forms.TextInput(
			attrs={'class': 'form-control form-control-sm'}
		)
	)
	patient__name = CharFilter(
		label = "患者姓名",
		lookup_expr='icontains',
		widget = forms.TextInput(
			attrs={'class': 'form-control form-control-sm'}
		)
	)
	patient__number = CharFilter(
		label = "患者登记号",
		lookup_expr='icontains',
		widget = forms.TextInput(
			attrs={'class': 'form-control form-control-sm'}
		)
	)

	class Meta:
		model = KawasakiDisease
		fields = [
			'code', 'disease_code', 'patient__name',
			'patient__number'
		]

class ArrhythmiaDiseaseFilter(FilterSet):
	code = CharFilter(
		label = "编号",
		lookup_expr='icontains',
		widget = forms.TextInput(
			attrs={'class': 'form-control form-control-sm'}
		)
	)
	disease_code = CharFilter(
		label = "测序编号",
		lookup_expr='icontains',
		widget = forms.TextInput(
			attrs={'class': 'form-control form-control-sm'}
		)
	)
	patient__name = CharFilter(
		label = "患者姓名",
		lookup_expr='icontains',
		widget = forms.TextInput(
			attrs={'class': 'form-control form-control-sm'}
		)
	)
	patient__number = CharFilter(
		label = "患者登记号",
		lookup_expr='icontains',
		widget = forms.TextInput(
			attrs={'class': 'form-control form-control-sm'}
		)
	)

	class Meta:
		model = ArrhythmiaDisease
		fields = [
			'code', 'disease_code', 'patient__name',
			'patient__number'
		]

class CongenitalSurgeryDiseaseFilter(FilterSet):
	code = CharFilter(
		label = "编号",
		lookup_expr='icontains',
		widget = forms.TextInput(
			attrs={'class': 'form-control form-control-sm'}
		)
	)
	disease_code = CharFilter(
		label = "测序编号",
		lookup_expr='icontains',
		widget = forms.TextInput(
			attrs={'class': 'form-control form-control-sm'}
		)
	)
	patient__name = CharFilter(
		label = "患者姓名",
		lookup_expr='icontains',
		widget = forms.TextInput(
			attrs={'class': 'form-control form-control-sm'}
		)
	)
	patient__number = CharFilter(
		label = "患者登记号",
		lookup_expr='icontains',
		widget = forms.TextInput(
			attrs={'class': 'form-control form-control-sm'}
		)
	)

	class Meta:
		model = CongenitalSurgeryDisease
		fields = [
			'code', 'disease_code', 'patient__name',
			'patient__number'
		]

class CongenitalInterveneDiseaseFilter(FilterSet):
	code = CharFilter(
		label = "编号",
		lookup_expr='icontains',
		widget = forms.TextInput(
			attrs={'class': 'form-control form-control-sm'}
		)
	)
	disease_code = CharFilter(
		label = "测序编号",
		lookup_expr='icontains',
		widget = forms.TextInput(
			attrs={'class': 'form-control form-control-sm'}
		)
	)
	patient__name = CharFilter(
		label = "患者姓名",
		lookup_expr='icontains',
		widget = forms.TextInput(
			attrs={'class': 'form-control form-control-sm'}
		)
	)
	patient__number = CharFilter(
		label = "患者登记号",
		lookup_expr='icontains',
		widget = forms.TextInput(
			attrs={'class': 'form-control form-control-sm'}
		)
	)

	class Meta:
		model = CongenitalInterveneDisease
		fields = [
			'code', 'disease_code', 'patient__name',
			'patient__number'
		]