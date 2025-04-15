from pathlib import Path

from django.utils import timezone
from django.conf import settings
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from django.db import transaction
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import *
from .tasks import *
from .forms import *

# Create your views here.
@login_required
def index(request):
	#add.delay(1,2)
	return render(request, 'index.html')

@login_required
def aboutus(request):
	return render(request, 'about.html')

@login_required
def changelog(request):
	return render(request, 'changelog.html')

@login_required
def upload_process(request):
	if request.method == 'POST':
		file = request.FILES.get('file')
		now_time = timezone.now()
		upload_folder = Path(settings.MEDIA_ROOT) / str(now_time.year) / str(now_time.month)
		upload_folder.mkdir(parents=True, exist_ok=True)
		save_file = str(upload_folder / file.name)

		with open(save_file, 'wb') as fw:
			for chunk in file.chunks():
				fw.write(chunk)

		return JsonResponse({'path': save_file})

@login_required
def validate_field(request):
	pass

@login_required
def get_file_browser(request):
	current_dir = request.GET.get('id')

	if current_dir == '#':
		current_dir = settings.MEDIA_ROOT

	fpath = Path(current_dir or BASE_DIR)

	children = []

	for item in fpath.iterdir():
		children.append({
			'id': str(item),
			'text': item.name,
			'icon': '/static/img/folder.svg' if item.is_dir() else '/static/img/file.svg',
			'children': item.is_dir()
		})

	return JsonResponse(children, safe=False)

@login_required
def fetch_for_select(request):
	model = request.GET.get('model')
	term = request.GET.get('term', '')
	term = term.strip()
	items = []

	match model:
		case 'patient':
			objs = Patient.objects.all()

			if term:
				objs = objs.filter(
					Q(name__icontains=term) |
					Q(number__icontains=term)
				)

			for obj in objs[0:30]:
				items.append({
					'id': obj.pk,
					'text': "{} / {}".format(obj.name, obj.number)
				})

		case 'dataset':
			objs = Dataset.objects.all()

			if term:
				objs = objs.filter(
					Q(name__icontains=term) |
					Q(code__icontains=term) |
					Q(patient__name__icontains=term) |
					Q(patient__number__icontains=term)
				)

			for obj in objs[0:30]:
				items.append({
					'id': obj.pk,
					'text': "{} / {} / {} / {}".format(
						obj.name, obj.code,
						obj.patient.name,
						obj.patient.number
					)
				})

	return JsonResponse({
		'results': items,
		'pagination': {'more': False}
	})

class DiseaseListView(LoginRequiredMixin, ListView):
	model = Disease
	template_name = 'disease-list.html'
	context_object_name = 'diseases'
	paginate_by = 10

class DiseaseCreateView(LoginRequiredMixin, CreateView):
	model = Disease
	http_method_names = ['post']
	fields = ['name', 'comment']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class PatientListView(LoginRequiredMixin, ListView):
	model = Patient
	template_name = 'patient-list.html'
	context_object_name = 'patients'
	paginate_by = 10

class PatientCreateView(LoginRequiredMixin, CreateView):
	model = Patient
	http_method_names = ['post']
	success_url = reverse_lazy('list-patients')
	fields = ['name', 'number', 'gender', 'ethnicity', 'age', 'weight', 'height', 'phone', 'address']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class DatasetListView(LoginRequiredMixin, ListView):
	model = Dataset
	template_name = 'dataset-list.html'
	context_object_name = 'datas'
	paginate_by = 10

class DatasetCreateView(LoginRequiredMixin, CreateView):
	model = Dataset
	template_name = 'dataset-form.html'
	success_url = reverse_lazy('list-datasets')
	http_method_names = ['get', 'post']
	fields = ['code', 'tissue', 'first', 'second', 'type', 'platform', 'comment', 'patient']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

#@login_required
class TaskListView(LoginRequiredMixin, ListView):
	model = Task
	template_name = 'task-list.html'
	context_object_name = 'tasks'
	paginate_by = 10

class TaskCreateView(LoginRequiredMixin, CreateView):
	model = Task
	success_url = reverse_lazy('list-tasks')
	http_method_names = ['post']
	fields = ['name', 'command', 'dataset']

	def form_valid(self, form):
		form.instance.author = self.request.user
		response = super().form_valid(form)
		tid = self.object.id

		def on_commit():
			if self.object.command == 1:
				task = call_snp_from_ges.delay(self.object.id)
			else:
				task = test_pipeline.delay(self.object.id)

			self.object.long_id = task.id
			self.object.short_id = task.id[0:8]
			self.object.save()

		transaction.on_commit(on_commit)
		return response
