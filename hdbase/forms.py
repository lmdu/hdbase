from django import forms

from .models import *

class TaskForm(forms.ModelForm):
	class Meta:
		model = TaskModel
		fields = ['read_one', 'read_two']