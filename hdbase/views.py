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
from django.views.generic import View, ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import *
from .tasks import *
from .forms import *
from .utils import *

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
	form_class = PatientForm
	template_name = 'disease-common-form.html'
	success_url = reverse_lazy('list-patients')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = "添加患者"
		context['subtitle'] = "添加患者信息"
		return context

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class PatientUpdateView(LoginRequiredMixin, UpdateView):
	model = Patient
	form_class = PatientForm
	template_name = 'disease-common-form.html'
	success_url = reverse_lazy('list-patients')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = "修改患者 {}-{}".format(self.object.name, self.object.number)
		context['subtitle'] = "修改患者信息"
		return context

class PatientDeleteView(LoginRequiredMixin, DeleteView):
	model = Patient
	template_name = 'disease-common-delete.html'
	success_url = reverse_lazy('list-patients')

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

#disease classes
class DiseaseListView(LoginRequiredMixin, ListView):
	paginate_by = 15

class DiseaseCreateView(LoginRequiredMixin, CreateView):
	disease_type = ''
	template_name = 'disease-common-form.html'

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = "添加{}病例".format(self.disease_type)
		context['subtitle'] = "添加病例"
		return context

class DiseaseUpdateView(LoginRequiredMixin, UpdateView):
	disease_type = ''
	template_name = 'disease-common-form.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = "修改{}病例 {}".format(self.disease_type, self.object.disease_code)
		context['subtitle'] = "修改病例信息"
		return context

class DiseaseDeleteView(LoginRequiredMixin, DeleteView):
	template_name = 'disease-common-delete.html'

class DiseaseDetailView(LoginRequiredMixin, DetailView):
	pass

#cardiomyopathy disease
class CardiomyopathyListView(DiseaseListView):
	model = CardiomyopathyDisease
	template_name = 'cardiomyopathy-list.html'
	context_object_name = 'cds'

class CardiomyopathyCreateView(DiseaseCreateView):
	disease_type = '心肌病'
	model = CardiomyopathyDisease
	form_class = CardiomyopathyDiseaseForm
	success_url = reverse_lazy('list-cardiomyopathy')

class CardiomyopathyUpdateView(DiseaseUpdateView):
	disease_type = '心肌病'
	model = CardiomyopathyDisease
	form_class = CardiomyopathyDiseaseForm
	success_url = reverse_lazy('list-cardiomyopathy')

class CardiomyopathyDeleteView(DiseaseDeleteView):
	model = CardiomyopathyDisease
	success_url = reverse_lazy('list-cardiomyopathy')

class CardiomyopathyDetailView(DiseaseDetailView):
	model = CardiomyopathyDisease
	template_name = 'cardiomyopathy-detail.html'

class CardiomyopathyExtraCreateView(LoginRequiredMixin, CreateView):
	sub_title = ""
	template_name = 'disease-common-form.html'

	def get_success_url(self):
		return reverse('view-cardiomyopathy', kwargs={'pk': self.object.disease.pk})

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		d = CardiomyopathyDisease.objects.get(pk=self.kwargs['did'])
		context['title'] = "病例 {}".format(d.disease_code)
		context['subtitle'] = sub_title
		return context

	def form_valid(self, form):
		form.instance.author = self.request.user
		disease = CardiomyopathyDisease.objects.get(pk=self.kwargs['did'])
		form.instance.disease = disease
		response = super().form_valid(form)

		if 'dicom_file' in form.cleaned_data and self.object.dicom_file:
			study_id = upload_dicoms(self.object.dicom_file.path)
			self.object.dicom_uuid = study_id
			self.object.save()

		return response

class CardiomyopathyExtraUpdateView(LoginRequiredMixin, UpdateView):
	sub_title = ''
	template_name = 'disease-common-form.html'

	def get_success_url(self):
		return reverse('view-cardiomyopathy', kwargs={'pk': self.object.disease.pk})

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = "病例 {}".format(self.object.disease.disease_code)
		context['subtitle'] = sub_title
		return context

	def form_valid(self, form):
		response = super().form_valid(form)

		if form.has_changed() and 'dicom_file' in form.changed_data:
			study_id = upload_dicoms(self.object.dicom_file.path)
			self.object.dicom_uuid = study_id
			self.object.save()

		return response

class CardiomyopathyExtraDeleteView(LoginRequiredMixin, DeleteView):
	template_name = 'disease-common-delete.html'

	def get_success_url(self):
		return reverse('view-cardiomyopathy', kwargs={'pk': self.object.disease.pk})

class CardiomyopathyBloodCreateView(CardiomyopathyExtraCreateView):
	sub_title = "添加检验信息"
	model = CardiomyopathyBloodRoutine
	form_class = CardiomyopathyBloodForm

class CardiomyopathyBloodUpdateView(CardiomyopathyExtraUpdateView):
	sub_title = "修改检验信息"
	model = CardiomyopathyBloodRoutine
	form_class = CardiomyopathyBloodForm

class CardiomyopathyBloodDeleteView(CardiomyopathyExtraDeleteView):
	model = CardiomyopathyBloodRoutine

class CardiomyopathyMarkerCreateView(CardiomyopathyExtraCreateView):
	sub_title = "添加心肌(心衰)标志物"
	model = CardiomyopathyMarker
	form_class = CardiomyopathyMarkerForm

class CardiomyopathyMarkerUpdateView(CardiomyopathyExtraUpdateView):
	sub_title = "修改心肌(心衰)标志物"
	model = CardiomyopathyMarker
	form_class = CardiomyopathyMarkerForm

class CardiomyopathyMarkerDeleteView(CardiomyopathyExtraDeleteView):
	model = CardiomyopathyMarker

class CardiomyopathyTreatmentCreateView(CardiomyopathyExtraCreateView):
	sub_title = "添加治疗情况"
	model = CardiomyopathyTreatment
	form_class = CardiomyopathyTreatmentForm

class CardiomyopathyTreatmentUpdateView(CardiomyopathyExtraUpdateView):
	sub_title = "修改治疗情况"
	model = CardiomyopathyTreatment
	form_class = CardiomyopathyTreatmentForm

class CardiomyopathyTreatmentDeleteView(CardiomyopathyExtraDeleteView):
	model = CardiomyopathyTreatment

class CardiomyopathyUltrasoundCreateView(CardiomyopathyExtraCreateView):
	sub_title = "添加心脏超声"
	model = CardiomyopathyUltrasound
	form_class = CardiomyopathyUltrasoundForm

class CardiomyopathyUltrasoundUpdateView(CardiomyopathyExtraUpdateView):
	sub_title = "修改心脏超声"
	model = CardiomyopathyUltrasound
	form_class = CardiomyopathyUltrasoundForm
	template_name = 'disease-common-form.html'

class CardiomyopathyUltrasoundDeleteView(CardiomyopathyExtraDeleteView):
	model = CardiomyopathyUltrasound

class CardiomyopathyMRICreateView(CardiomyopathyExtraCreateView):
	sub_title = "添加MRI"
	model = CardiomyopathyMRI
	form_class = CardiomyopathyMRIForm

class CardiomyopathyMRIUpdateView(CardiomyopathyExtraUpdateView):
	sub_title = "修改MRI"
	model = CardiomyopathyMRI
	form_class = CardiomyopathyMRIForm

class CardiomyopathyMRIDeleteView(CardiomyopathyExtraDeleteView):
	model = CardiomyopathyMRI

class CardiomyopathyECGCreateView(CardiomyopathyExtraCreateView):
	sub_title = "添加心电图"
	model = CardiomyopathyECG
	form_class = CardiomyopathyECGForm

class CardiomyopathyECGUpdateView(CardiomyopathyExtraUpdateView):
	sub_title = "修改心电图"
	model = CardiomyopathyECG
	form_class = CardiomyopathyECGForm

class CardiomyopathyECGDeleteView(CardiomyopathyExtraDeleteView):
	model = CardiomyopathyECG

class CardiomyopathyGeneReportCreateView(CardiomyopathyExtraCreateView):
	sub_title = "添加基因检测报告"
	model = CardiomyopathyGeneReport
	form_class = CardiomyopathyGeneReportForm

class CardiomyopathyGeneReportUpdateView(CardiomyopathyExtraUpdateView):
	sub_title = "修改基因检测报告"
	model = CardiomyopathyGeneReport
	form_class = CardiomyopathyGeneReportForm

class CardiomyopathyGeneReportDeleteView(CardiomyopathyExtraDeleteView):
	model = CardiomyopathyGeneReport

class CardiomyopathyGeneMutationCreateView(CardiomyopathyExtraCreateView):
	sub_title = "添加基因检测报告内容"
	model = CardiomyopathyGeneMutation
	form_class = CardiomyopathyGeneMutationForm

class CardiomyopathyGeneMutationUpdateView(CardiomyopathyExtraUpdateView):
	sub_title = "修改基因检测报告内容"
	model = CardiomyopathyGeneMutation
	form_class = CardiomyopathyGeneMutationForm

class CardiomyopathyGeneMutationDeleteView(CardiomyopathyExtraDeleteView):
	model = CardiomyopathyGeneMutation

#kawasaki disease
class KawasakiListView(LoginRequiredMixin, ListView):
	model = KawasakiDisease
	template_name = 'kawasaki-list.html'
	paginate_by = 10

class KawasakiCreateView(LoginRequiredMixin, CreateView):
	model = KawasakiDisease
	form_class = KawasakiDiseaseForm
	template_name = 'disease-common-form.html'
	success_url = reverse_lazy('list-kawasaki')

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = "添加心肌病病例"
		context['subtitle'] = "添加病例"
		return context

class CardiomyopathyUpdateView(LoginRequiredMixin, UpdateView):
	model = CardiomyopathyDisease
	form_class = CardiomyopathyDiseaseForm
	template_name = 'disease-common-form.html'
	success_url = reverse_lazy('list-cardiomyopathy')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = "修改心肌病病例 {}".format(self.object.disease_code)
		context['subtitle'] = "修改病例信息"
		return context

class CardiomyopathyDeleteView(LoginRequiredMixin, DeleteView):
	model = CardiomyopathyDisease
	template_name = 'disease-common-delete.html'
	success_url = reverse_lazy('list-cardiomyopathy')

class CardiomyopathyDetailView(LoginRequiredMixin, DetailView):
	model = CardiomyopathyDisease
	template_name = 'cardiomyopathy-detail.html'

class CardiomyopathyBloodCreateView(LoginRequiredMixin, CreateView):
	model = CardiomyopathyBloodRoutine
	form_class = CardiomyopathyBloodForm
	template_name = 'disease-common-form.html'

	def get_success_url(self):
		return reverse('view-cardiomyopathy', kwargs={'pk': self.object.disease.pk})

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		d = CardiomyopathyDisease.objects.get(pk=self.kwargs['did'])
		context['title'] = "病例 {}".format(d.disease_code)
		context['subtitle'] = "添加检验信息"
		return context

	def form_valid(self, form):
		form.instance.author = self.request.user
		form.instance.disease =  CardiomyopathyDisease.objects.get(pk=self.kwargs['did'])
		return super().form_valid(form)

class CardiomyopathyBloodUpdateView(LoginRequiredMixin, UpdateView):
	model = CardiomyopathyBloodRoutine
	form_class = CardiomyopathyBloodForm
	template_name = 'disease-common-form.html'

	def get_success_url(self):
		return reverse('view-cardiomyopathy', kwargs={'pk': self.object.disease.pk})

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		d = CardiomyopathyDisease.objects.get(pk=self.kwargs['did'])
		context['title'] = "病例 {}".format(d.disease_code)
		context['subtitle'] = "修改检验信息"
		return context

class CardiomyopathyBloodDeleteView(LoginRequiredMixin, DeleteView):
	model = CardiomyopathyBloodRoutine
	template_name = 'disease-common-delete.html'

	def get_success_url(self):
		return reverse('view-cardiomyopathy', kwargs={'pk': self.object.disease.pk})

class CardiomyopathyMarkerCreateView(LoginRequiredMixin, CreateView):
	model = CardiomyopathyMarker
	form_class = CardiomyopathyMarkerForm
	template_name = 'disease-common-form.html'

	def get_success_url(self):
		return reverse('view-cardiomyopathy', kwargs={'pk': self.object.disease.pk})

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		d = CardiomyopathyDisease.objects.get(pk=self.kwargs['did'])
		context['title'] = "病例 {}".format(d.disease_code)
		context['subtitle'] = "添加心肌(心衰)标志物"
		return context

	def form_valid(self, form):
		form.instance.author = self.request.user
		form.instance.disease =  CardiomyopathyDisease.objects.get(pk=self.kwargs['did'])
		return super().form_valid(form)

class CardiomyopathyMarkerUpdateView(LoginRequiredMixin, UpdateView):
	model = CardiomyopathyMarker
	form_class = CardiomyopathyMarkerForm
	template_name = 'disease-common-form.html'

	def get_success_url(self):
		return reverse('view-cardiomyopathy', kwargs={'pk': self.object.disease.pk})

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		d = CardiomyopathyDisease.objects.get(pk=self.kwargs['did'])
		context['title'] = "病例 {}".format(d.disease_code)
		context['subtitle'] = "修改心肌(心衰)标志物"
		return context

class CardiomyopathyMarkerDeleteView(LoginRequiredMixin, DeleteView):
	model = CardiomyopathyMarker
	template_name = 'disease-common-delete.html'

	def get_success_url(self):
		return reverse('view-cardiomyopathy', kwargs={'pk': self.object.disease.pk})

class CardiomyopathyTreatmentCreateView(LoginRequiredMixin, CreateView):
	model = CardiomyopathyTreatment
	form_class = CardiomyopathyTreatmentForm
	template_name = 'disease-common-form.html'

	def get_success_url(self):
		return reverse('view-cardiomyopathy', kwargs={'pk': self.object.disease.pk})

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		d = CardiomyopathyDisease.objects.get(pk=self.kwargs['did'])
		context['title'] = "病例 {}".format(d.disease_code)
		context['subtitle'] = "添加治疗情况"
		return context

	def form_valid(self, form):
		form.instance.author = self.request.user
		form.instance.disease =  CardiomyopathyDisease.objects.get(pk=self.kwargs['did'])
		return super().form_valid(form)

class CardiomyopathyTreatmentUpdateView(LoginRequiredMixin, UpdateView):
	model = CardiomyopathyTreatment
	form_class = CardiomyopathyTreatmentForm
	template_name = 'disease-common-form.html'

	def get_success_url(self):
		return reverse('view-cardiomyopathy', kwargs={'pk': self.object.disease.pk})

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		d = CardiomyopathyDisease.objects.get(pk=self.kwargs['did'])
		context['title'] = "病例 {}".format(d.disease_code)
		context['subtitle'] = "修改治疗情况"
		return context

class CardiomyopathyTreatmentDeleteView(LoginRequiredMixin, DeleteView):
	model = CardiomyopathyTreatment
	template_name = 'disease-common-delete.html'

	def get_success_url(self):
		return reverse('view-cardiomyopathy', kwargs={'pk': self.object.disease.pk})

class CardiomyopathyUltrasoundCreateView(LoginRequiredMixin, CreateView):
	model = CardiomyopathyUltrasound
	form_class = CardiomyopathyUltrasoundForm
	template_name = 'disease-common-form.html'

	def get_success_url(self):
		return reverse('view-cardiomyopathy', kwargs={'pk': self.object.disease.pk})

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		d = CardiomyopathyDisease.objects.get(pk=self.kwargs['did'])
		context['title'] = "病例 {}".format(d.disease_code)
		context['subtitle'] = "添加心脏超声"
		return context

	def form_valid(self, form):
		form.instance.author = self.request.user
		form.instance.disease =  CardiomyopathyDisease.objects.get(pk=self.kwargs['did'])
		response = super().form_valid(form)

		if self.object.dicom_file:
			study_id = upload_dicoms(self.object.dicom_file.path)
			self.object.dicom_uuid = study_id
			self.object.save()

		return response

class CardiomyopathyUltrasoundUpdateView(LoginRequiredMixin, UpdateView):
	model = CardiomyopathyUltrasound
	form_class = CardiomyopathyUltrasoundForm
	template_name = 'disease-common-form.html'

	def get_success_url(self):
		return reverse('view-cardiomyopathy', kwargs={'pk': self.object.disease.pk})

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		d = CardiomyopathyDisease.objects.get(pk=self.kwargs['did'])
		context['title'] = "病例 {}".format(d.disease_code)
		context['subtitle'] = "修改心脏超声"
		return context

	def form_valid(self, form):
		response = super().form_valid(form)

		if 'dicom_file' in form.changed_data:
			study_id = upload_dicoms(self.object.dicom_file.path)
			self.object.dicom_uuid = study_id
			self.object.save()

		return response

class CardiomyopathyUltrasoundDeleteView(LoginRequiredMixin, DeleteView):
	model = CardiomyopathyUltrasound
	template_name = 'disease-common-delete.html'

	def get_success_url(self):
		return reverse('view-cardiomyopathy', kwargs={'pk': self.kwargs['did']})

class CardiomyopathyMRICreateView(LoginRequiredMixin, CreateView):
	model = CardiomyopathyMRI
	form_class = CardiomyopathyMRIForm
	template_name = 'disease-common-form.html'

	def get_success_url(self):
		return reverse('view-cardiomyopathy', kwargs={'pk': self.object.disease.pk})

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		d = CardiomyopathyDisease.objects.get(pk=self.kwargs['did'])
		context['title'] = "病例 {}".format(d.disease_code)
		context['subtitle'] = "添加MRI"
		return context

	def form_valid(self, form):
		form.instance.author = self.request.user
		form.instance.disease =  CardiomyopathyDisease.objects.get(pk=self.kwargs['did'])
		response = super().form_valid(form)

		if self.object.dicom_file:
			study_id = upload_dicoms(self.object.dicom_file.path)
			self.object.dicom_uuid = study_id
			self.object.save()

		return response

class CardiomyopathyMRIUpdateView(LoginRequiredMixin, UpdateView):
	model = CardiomyopathyMRI
	form_class = CardiomyopathyMRIForm
	template_name = 'disease-common-form.html'

	def get_success_url(self):
		return reverse('view-cardiomyopathy', kwargs={'pk': self.object.disease.pk})

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		d = CardiomyopathyDisease.objects.get(pk=self.kwargs['did'])
		context['title'] = "病例 {}".format(d.disease_code)
		context['subtitle'] = "修改MRI"
		return context

	def form_valid(self, form):
		response = super().form_valid(form)

		if 'dicom_file' in form.changed_data:
			study_id = upload_dicoms(self.object.dicom_file.path)
			self.object.dicom_uuid = study_id
			self.object.save()

		return response

class CardiomyopathyMRIDeleteView(LoginRequiredMixin, DeleteView):
	model = CardiomyopathyMRI
	template_name = 'disease-common-delete.html'

	def get_success_url(self):
		return reverse('view-cardiomyopathy', kwargs={'pk': self.kwargs['did']})

class CardiomyopathyECGCreateView(LoginRequiredMixin, CreateView):
	model = CardiomyopathyECG
	form_class = CardiomyopathyECGForm
	template_name = 'disease-common-form.html'

	def get_success_url(self):
		return reverse('view-cardiomyopathy', kwargs={'pk': self.object.disease.pk})

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		d = CardiomyopathyDisease.objects.get(pk=self.kwargs['did'])
		context['title'] = "病例 {}".format(d.disease_code)
		context['subtitle'] = "添加心电图"
		return context

	def form_valid(self, form):
		form.instance.author = self.request.user
		form.instance.disease =  CardiomyopathyDisease.objects.get(pk=self.kwargs['did'])
		return super().form_valid(form)

class CardiomyopathyECGUpdateView(LoginRequiredMixin, UpdateView):
	model = CardiomyopathyECG
	form_class = CardiomyopathyECGForm
	template_name = 'disease-common-form.html'

	def get_success_url(self):
		return reverse('view-cardiomyopathy', kwargs={'pk': self.object.disease.pk})

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		d = CardiomyopathyDisease.objects.get(pk=self.kwargs['did'])
		context['title'] = "病例 {}".format(d.disease_code)
		context['subtitle'] = "修改心电图"
		return context

class CardiomyopathyECGDeleteView(LoginRequiredMixin, DeleteView):
	model = CardiomyopathyECG
	template_name = 'disease-common-delete.html'

	def get_success_url(self):
		return reverse('view-cardiomyopathy', kwargs={'pk': self.kwargs['did']})

class CardiomyopathyGeneReportCreateView(LoginRequiredMixin, CreateView):
	model = CardiomyopathyGeneReport
	form_class = CardiomyopathyGeneReportForm
	template_name = 'disease-common-form.html'

	def get_success_url(self):
		return reverse('view-cardiomyopathy', kwargs={'pk': self.object.disease.pk})

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		d = CardiomyopathyDisease.objects.get(pk=self.kwargs['did'])
		context['title'] = "病例 {}".format(d.disease_code)
		context['subtitle'] = "添加基因检测报告"
		return context

	def form_valid(self, form):
		form.instance.author = self.request.user
		form.instance.disease =  CardiomyopathyDisease.objects.get(pk=self.kwargs['did'])
		return super().form_valid(form)

class CardiomyopathyGeneReportUpdateView(LoginRequiredMixin, UpdateView):
	model = CardiomyopathyGeneReport
	form_class = CardiomyopathyGeneReportForm
	template_name = 'disease-common-form.html'

	def get_success_url(self):
		return reverse('view-cardiomyopathy', kwargs={'pk': self.object.report.disease.pk})

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		d = CardiomyopathyDisease.objects.get(pk=self.kwargs['did'])
		context['title'] = "病例 {}".format(d.disease_code)
		context['subtitle'] = "修改基因检测报告"
		return context

class CardiomyopathyGeneReportDeleteView(LoginRequiredMixin, DeleteView):
	model = CardiomyopathyGeneReport
	template_name = 'disease-common-delete.html'

	def get_success_url(self):
		return reverse('view-cardiomyopathy', kwargs={'pk': self.kwargs['did']})

class CardiomyopathyGeneMutationCreateView(LoginRequiredMixin, CreateView):
	model = CardiomyopathyGeneMutation
	form_class = CardiomyopathyGeneMutationForm
	template_name = 'disease-common-form.html'

	def get_success_url(self):
		return reverse('view-cardiomyopathy', kwargs={'pk': self.object.report.disease.pk})

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		d = CardiomyopathyDisease.objects.get(pk=self.kwargs['did'])
		context['title'] = "病例 {}".format(d.disease_code)
		context['subtitle'] = "添加基因检测报告内容"
		return context

class CardiomyopathyGeneMutationUpdateView(LoginRequiredMixin, UpdateView):
	model = CardiomyopathyGeneMutation
	form_class = CardiomyopathyGeneMutationForm
	template_name = 'disease-common-form.html'

	def get_success_url(self):
		return reverse('view-cardiomyopathy', kwargs={'pk': self.object.report.disease.pk})

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		d = CardiomyopathyDisease.objects.get(pk=self.kwargs['did'])
		context['title'] = "病例 {}".format(d.disease_code)
		context['subtitle'] = "修改基因检测报告内容"
		return context

class CardiomyopathyGeneMutationDeleteView(LoginRequiredMixin, DeleteView):
	model = CardiomyopathyGeneMutation
	template_name = 'disease-common-delete.html'

	def get_success_url(self):
		return reverse('view-cardiomyopathy', kwargs={'pk': self.kwargs['did']})


