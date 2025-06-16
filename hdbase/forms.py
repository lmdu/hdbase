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
			'remain_sample': "剩余标本",
			'patient': "患者",
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
			'remain_sample': None,
			'patient': None,
		}

class CardiomyopathyBloodForm(TablerModelForm):
	class Meta:
		model = CardiomyopathyBloodRoutine
		exclude = ['created', 'disease', 'author']
		labels = {
			'wbc': "WBC (×10^9/L)",
			'hgb': "HGB (g/L)",
			'hct': "HCT (%)",
			'mcv': "MCV (fl)",
			'mch': "MCH (pg)",
			'mchc': "MCHC (g/L)",
			'rdw': "RDW (fl)",
			'crp': "CRP/hs-CRP (mg/L)",
			'alt': "ALT (U/L)",
			'ast': "AST (U/L)",
			'alb': "ALB (g/L)",
			'cr': "Cr (umol/L)",
			'tc': "TC (mmol/L)",
			'tg': "TG (mmol/L)",
			'hdlc': "HDL-C (mmol/L)",
			'ldlc': "LDL-C (mmol/L)",
			'apoa': "APO-A1 (g/L)",
			'apob': "APO-B (g/L)",
			'glu': "GLU (mmol/L)",
			'rheumatism': "风湿筛查",
			'autoantibody': "自身抗体",
			'positive_result': "阳性结果",
		}
		help_texts = {
			'wbc': None,
			'hgb': None,
			'hct': None,
			'mcv': None,
			'mch': None,
			'mchc': None,
			'rdw': None,
			'crp': None,
			'alt': None,
			'ast': None,
			'alb': None,
			'cr': None,
			'tc': None,
			'tg': None,
			'hdlc': None,
			'ldlc': None,
			'apoa': None,
			'apob': None,
			'glu': None,
			'rheumatism': None,
			'autoantibody': None,
			'positive_result': None,
		}
