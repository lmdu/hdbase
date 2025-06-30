from django_filters import FilterSet

from .models import *

class CardiomyopathyDiseaseFilter(FilterSet):
	class Meta:
		model = CardiomyopathyDisease
		fields = ['disease_type', 'mutate_gene', 'arrhythmia_type']
