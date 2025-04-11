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

class ProfileForm(TablerModelForm):
	username = forms.CharField(
		required = False,
		label = "用户名",
		widget = forms.TextInput(attrs = {'disabled': 'disabled'})
	)
	last_name = forms.CharField(label="姓氏", required=False)
	first_name = forms.CharField(label="名字", required=False)
	email = forms.CharField(label="邮箱", required=True)

	class Meta:
		model = Profile
		fields = ['username', 'last_name', 'first_name',
			'email', 'phone', 'major', 'resume', 'role',
			'title', 'degree', 'position', 'state'
		]
		labels = {
			'phone': "电话",
			'major': "专业",
			'resume': "个人简介",
			'role': "权限",
			'title': "职称",
			'degree': "学历",
			'position': "职位",
			'state': "状态"
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		user = self.instance.user
		self.fields['username'].initial = user.username
		self.fields['last_name'].initial = user.last_name
		self.fields['first_name'].initial = user.first_name
		self.fields['email'].initial = user.email

	def save(self):
		profile = super().save(commit=False)
		profile.user.first_name = self.cleaned_data['first_name']
		profile.user.last_name = self.cleaned_data['last_name']
		profile.user.email = self.cleaned_data['email']
		profile.user.save()
		return profile
