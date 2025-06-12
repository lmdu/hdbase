from pathlib import Path

import psutil

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
from django.views.generic import View, ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import *
from .tasks import *
from .forms import *

from venom.celery import app as celery_app

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

class FileBrowseView(LoginRequiredMixin, View):
	def get(self, request):
		current_dir = request.GET.get('id')

		if current_dir == '#':
			opt, _ = Option.objects.get_or_create(name='global')
			current_dir = opt.values.get('rawdir', '/tmp')

		children = []
		for item in Path(current_dir).iterdir():
			children.append({
				'id': str(item),
				'text': item.name,
				'icon': '/static/img/folder.svg' if item.is_dir() else '/static/img/file.svg',
				'children': item.is_dir()
			})

		return JsonResponse(children, safe=False)

class DicomUploadView(LoginRequiredMixin, View):
	def post(self, request):
		dicom_file = request.FILES.get('dicomfile')

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

class WebsiteSettingView(LoginRequiredMixin, View):
	def get(self, request):
		return render(request, 'setting-website.html')

	def post(self, request):
		pass

class GlobalSettingView(LoginRequiredMixin, View):
	def get(self, request):
		params, _ = Option.objects.get_or_create(name='global')
		return render(request, 'setting-global.html', {
			'cpu_count': psutil.cpu_count(),
			'params': params.values
		})

	def post(self, request):
		params = request.POST.dict()
		params.pop('csrfmiddlewaretoken')
		obj = Option.objects.get(name='global')
		obj.values = params
		obj.save()

		stats = celery_app.control.inspect().stats()

		inspector = celery_app.control.inspect()
		active_tasks = inspector.active() or {}
		total_tasks = sum(len(tasks) for tasks in active_tasks.values())

		set_workers =  int(params['workers'])

		if set_workers > total_tasks:
			celery_app.control.pool_grow(set_workers - total_tasks)
		elif set_workers < total_tasks:
			celery_app.control.pool_shrink(total_tasks - set_workers)

		return redirect('setting-global')

class ParameterSettingView(LoginRequiredMixin, View):
	def get(self, request):
		params, _ = Option.objects.get_or_create(name='parameter')
		return render(request, 'setting-parameter.html', {
			'params': params.values
		})

	def post(self, request):
		params = request.POST.dict()
		params.pop('csrfmiddlewaretoken')
		obj = Option.objects.get(name='parameter')
		obj.values = params
		obj.save()
		return redirect('setting-parameter')

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
	fields = ['name', 'code', 'tissue', 'first', 'second', 'type', 'platform', 'comment', 'patient']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		opt, _ = Option.objects.get_or_create(name='global')
		context["rawdir"] = opt.values.get('rawdir', '/tmp')
		return context

#@login_required
class TaskListView(LoginRequiredMixin, ListView):
	model = Job
	template_name = 'task-list.html'
	context_object_name = 'tasks'
	paginate_by = 10

class TaskCreateView(LoginRequiredMixin, CreateView):
	model = Job
	success_url = reverse_lazy('list-tasks')
	http_method_names = ['post']
	fields = ['name', 'command', 'dataset']

	def form_valid(self, form):
		form.instance.author = self.request.user
		response = super().form_valid(form)

		opt = Option.objects.get(name='global')
		params = opt.values
		opt = Option.objects.get(name='parameter')
		params.update(opt.values)
		params['read1'] = self.object.dataset.first
		params['read2'] = self.object.dataset.second

		def on_commit():
			if self.object.command == 1:
				task = call_snp_from_ges.delay(self.object.id, self.object.short_id, params)
			else:
				task = test_pipeline.delay(self.object.id, self.object.short_id, params)

			self.object.long_id = task.id
			self.object.short_id = task.id[0:8]
			self.object.save()

		transaction.on_commit(on_commit)
		return response

class CardiomyopathyListView(LoginRequiredMixin, ListView):
	model = CardiomyopathyDisease
	template_name = 'cardiomyopathy-list.html'
	context_object_name = 'cds'
	paginate_by = 10
