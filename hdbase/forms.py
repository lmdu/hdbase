from django import forms

from .models import *

class TablerModelForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		for field in self.fields.values():
			if isinstance(field.widget, forms.Select):
				field.widget.attrs['class'] = "form-select"
			else:
				field.widget.attrs['class'] = "form-control"

class ChoiceFieldNoValidation(forms.ChoiceField):
	def validate(self, value):
		pass

class CardiomyopathyDiseaseForm(TablerModelForm):
	patient = ChoiceFieldNoValidation(choices=(), label="患者")

	class Meta:
		model = CardiomyopathyDisease
		exclude = ['created', 'updated', 'author']
		labels = {
			'disease_code': "编号或测序编号",
			'body_surface': "体表面积",
			'disease_type': "心肌病分型",
			'mutate_gene': "突变基因",
			'diagnose_age': "初诊年龄",
			'has_history': "有无家族史",
			'family_history': "家族史情况",
			'complication': "合并症",
			'heart_failure': "心衰评分",
			'is_survival': "是否存活",
			'death_time': "死亡时间",
			'arrhythmia_type': "心律失常类型",
			'special_treatment': "特殊治疗",
			'hospital_visits': "心衰再入院次数",
			'follow_time': "随访时间",
			'sample_collect': "是否采集标本",
			'test_sample': "已送检标本",
			'remain_sample': "剩余标本"
		}
		help_texts = {
			'disease_code': None,
			'body_surface': None,
			'disease_type': None,
			'mutate_gene': None,
			'diagnose_age': None,
			'has_history': None,
			'family_history': None,
			'complication': None,
			'heart_failure': None,
			'is_survival': None,
			'death_time': None,
			'arrhythmia_type': None,
			'special_treatment': None,
			'hospital_visits': None,
			'follow_time': None,
			'sample_collect': None,
			'test_sample': None,
			'remain_sample': None
		}


