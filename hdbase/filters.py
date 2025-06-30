from django import forms
from django_filters import *

from .models import *

class CardiomyopathyDiseaseFilter(FilterSet):
	patient__name = CharFilter(
		label = "患者姓名",
		lookup_expr='icontains',
		widget = forms.TextInput(attrs={'class': 'form-control form-control-sm'})
	)
	patient__number = CharFilter(
		label = "患者登记号",
		lookup_expr='icontains',
		widget = forms.TextInput(attrs={'class': 'form-control form-control-sm'})
	)
	disease_type = CharFilter(
		label = "心肌病分型",
		lookup_expr='icontains',
		widget = forms.TextInput(attrs={'class': 'form-control form-control-sm'})
	)

	mutate_gene = CharFilter(
		label = "突变基因",
		lookup_expr='icontains',
		widget = forms.TextInput(attrs={'class': 'form-control form-control-sm'})
	)

	arrhythmia_type = CharFilter(
		label = "心律失常类型",
		lookup_expr='icontains',
		widget = forms.TextInput(attrs={'class': 'form-control form-control-sm'})
	)

	class Meta:
		model = CardiomyopathyDisease
		fields = ['patient__name', 'patient__number', 'disease_type', 'mutate_gene', 'arrhythmia_type']
