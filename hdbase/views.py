import datetime
from pathlib import Path

import psutil

from django.utils import timezone
from django.utils.timesince import timesince
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

from django_filters.views import FilterView

from .models import *
from .tasks import *
from .forms import *
from .utils import *
from .filters import *

from venom.celery import app as celery_app

# Create your views here.
class IndexView(LoginRequiredMixin, View):
	def get(self, request):
		mem = psutil.virtual_memory()
		ttt = datetime.datetime.fromtimestamp(psutil.boot_time())
		active_cpus = len([p for p in psutil.cpu_percent(percpu=True) if p > 0])
		disk = psutil.disk_usage('/')

		dbdir = Path(__file__).parent.parent.resolve()
		print(dbdir)

		return render(request, 'index.html', {
			'memory': {
				'total': int(mem.total/1024/1024/1024),
				'avail': round(mem.available/1024/1024/1024, 2),
				'percent': round(mem.percent, 2),
			},
			'cpu': {
				'count': psutil.cpu_count(),
				'percent': round(psutil.cpu_percent(), 2),
				'running': timesince(ttt),
				'active': active_cpus,
				'activep': round(active_cpus/psutil.cpu_count()*100, 2),
			},
			'disk': {
				'total': int(disk.total/1024/1024/1024),
				'used': int(disk.used/1024/1024/1024),
				'free': int(disk.free/1024/1024/1024),
				'percent': disk.percent,
			},
			'stats': {
				'patient': Patient.objects.count(),
				'cm': CardiomyopathyDisease.objects.count(),
				'kd': KawasakiDisease.objects.count(),
				'ad': ArrhythmiaDisease.objects.count(),
				'csd': CongenitalSurgeryDisease.objects.count(),
				'cid': CongenitalInterveneDisease.objects.count(),
			}
		})

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

class Disease1ListView(LoginRequiredMixin, ListView):
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
class DiseaseListView(LoginRequiredMixin, FilterView):
	paginate_by = 15

class DiseaseCreateView(LoginRequiredMixin, CreateView):
	disease_abbr = ''
	disease_type = ''
	template_name = 'disease-common-form.html'

	def form_valid(self, form):
		form.instance.author = self.request.user
		response = super().form_valid(form)
		self.object.code = "{}{:0>7d}".format(self.disease_abbr, self.object.id)
		self.object.save()
		return response

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
	filterset_class = CardiomyopathyDiseaseFilter

class CardiomyopathyCreateView(DiseaseCreateView):
	disease_abbr = 'CM'
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
		context['subtitle'] = self.sub_title
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
		context['subtitle'] = self.sub_title
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
class KawasakiListView(DiseaseListView):
	model = KawasakiDisease
	template_name = 'kawasaki-list.html'
	filterset_class = KawasakiDiseaseFilter

class KawasakiCreateView(DiseaseCreateView):
	disease_abbr = 'KD'
	disease_type = '川崎病'
	model = KawasakiDisease
	form_class = KawasakiDiseaseForm
	success_url = reverse_lazy('list-kawasaki')

class KawasakiUpdateView(DiseaseUpdateView):
	disease_type = '川崎病'
	model = KawasakiDisease
	form_class = KawasakiDiseaseForm
	success_url = reverse_lazy('list-kawasaki')

class KawasakiDeleteView(DiseaseDeleteView):
	model = CardiomyopathyDisease
	success_url = reverse_lazy('list-kawasaki')

class KawasakiDetailView(DiseaseDetailView):
	model = KawasakiDisease
	template_name = 'kawasaki-detail.html'

class KawasakiExtraCreateView(LoginRequiredMixin, CreateView):
	sub_title = ""
	template_name = 'disease-common-form.html'

	def get_success_url(self):
		return reverse('view-kawasaki', kwargs={'pk': self.object.disease.pk})

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		d = KawasakiDisease.objects.get(pk=self.kwargs['did'])
		context['title'] = "病例 {}".format(d.disease_code)
		context['subtitle'] = self.sub_title
		return context

	def form_valid(self, form):
		form.instance.author = self.request.user
		disease = KawasakiDisease.objects.get(pk=self.kwargs['did'])
		form.instance.disease = disease
		response = super().form_valid(form)

		if 'dicom_file' in form.cleaned_data and self.object.dicom_file:
			study_id = upload_dicoms(self.object.dicom_file.path)
			self.object.dicom_uuid = study_id
			self.object.save()

		return response

class KawasakiExtraUpdateView(LoginRequiredMixin, UpdateView):
	sub_title = ''
	template_name = 'disease-common-form.html'

	def get_success_url(self):
		return reverse('view-kawasaki', kwargs={'pk': self.object.disease.pk})

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = "病例 {}".format(self.object.disease.disease_code)
		context['subtitle'] = self.sub_title
		return context

	def form_valid(self, form):
		response = super().form_valid(form)

		if form.has_changed() and 'dicom_file' in form.changed_data:
			study_id = upload_dicoms(self.object.dicom_file.path)
			self.object.dicom_uuid = study_id
			self.object.save()

		return response

class KawasakiExtraDeleteView(LoginRequiredMixin, DeleteView):
	template_name = 'disease-common-delete.html'

	def get_success_url(self):
		return reverse('view-kawasaki', kwargs={'pk': self.object.disease.pk})

class KawasakiBloodCreateView(KawasakiExtraCreateView):
	sub_title = "添加血常规信息"
	model = KawasakiBlood
	form_class = KawasakiBloodForm

class KawasakiBloodUpdateView(KawasakiExtraUpdateView):
	sub_title = "修改血常规信息"
	model = KawasakiBlood
	form_class = KawasakiBloodForm

class KawasakiBloodDeleteView(KawasakiExtraDeleteView):
	model = KawasakiBlood

class KawasakiBiochemistryCreateView(KawasakiExtraCreateView):
	sub_title = "添加生化检验"
	model = KawasakiBiochemistry
	form_class = KawasakiBiochemistryForm

class KawasakiBiochemistryUpdateView(KawasakiExtraUpdateView):
	sub_title = "修改生化检验"
	model = KawasakiBiochemistry
	form_class = KawasakiBiochemistryForm

class KawasakiBiochemistryDeleteView(KawasakiExtraDeleteView):
	model = KawasakiBiochemistry

class KawasakiMarkerCreateView(KawasakiExtraCreateView):
	sub_title = "添加凝血/心肌标志物"
	model = KawasakiMarker
	form_class = KawasakiMarkerForm

class KawasakiMarkerUpdateView(KawasakiExtraUpdateView):
	sub_title = "修改凝血/心肌标志物"
	model = KawasakiMarker
	form_class = KawasakiMarkerForm

class KawasakiMarkerDeleteView(KawasakiExtraDeleteView):
	model = KawasakiMarker

class KawasakiOtherExamineCreateView(KawasakiExtraCreateView):
	sub_title = "添加其他检验/检查"
	model = KawasakiOtherExamine
	form_class = KawasakiOtherExamineForm

class KawasakiOtherExamineUpdateView(KawasakiExtraUpdateView):
	sub_title = "修改其他检验/检查"
	model = KawasakiOtherExamine
	form_class = KawasakiOtherExamineForm

class KawasakiOtherExamineDeleteView(KawasakiExtraDeleteView):
	model = KawasakiOtherExamine

class KawasakiTreatmentCreateView(KawasakiExtraCreateView):
	sub_title = "添加治疗及效果"
	model = KawasakiTreatment
	form_class = KawasakiTreatmentForm

class KawasakiTreatmentUpdateView(KawasakiExtraUpdateView):
	sub_title = "修改治疗及效果"
	model = KawasakiTreatment
	form_class = KawasakiTreatmentForm

class KawasakiTreatmentDeleteView(KawasakiExtraDeleteView):
	model = KawasakiTreatment

class KawasakiCardiacPhenotypeCreateView(KawasakiExtraCreateView):
	sub_title = "添加心外表型"
	model = KawasakiCardiacPhenotype
	form_class = KawasakiCardiacPhenotypeForm

class KawasakiCardiacPhenotypeUpdateView(KawasakiExtraUpdateView):
	sub_title = "修改心外表型"
	model = KawasakiCardiacPhenotype
	form_class = KawasakiCardiacPhenotypeForm

class KawasakiCardiacPhenotypeDeleteView(KawasakiExtraDeleteView):
	model = KawasakiCardiacPhenotype

class KawasakiUltrasoundCreateView(KawasakiExtraCreateView):
	sub_title = "添加超声影像"
	model = KawasakiUltrasound
	form_class = KawasakiUltrasoundForm

class KawasakiUltrasoundUpdateView(KawasakiExtraUpdateView):
	sub_title = "修改超声影像"
	model = KawasakiUltrasound
	form_class = KawasakiUltrasoundForm

class KawasakiUltrasoundDeleteView(KawasakiExtraDeleteView):
	model = KawasakiUltrasound

class KawasakiMedimageCreateView(KawasakiExtraCreateView):
	sub_title = "添加特殊影像"
	model = KawasakiMedimage
	form_class = KawasakiMedimageForm

class KawasakiMedimageUpdateView(KawasakiExtraUpdateView):
	sub_title = "修改特殊影像"
	model = KawasakiMedimage
	form_class = KawasakiMedimageForm

class KawasakiMedimageDeleteView(KawasakiExtraDeleteView):
	model = KawasakiMedimage

class KawasakiGeneReportCreateView(KawasakiExtraCreateView):
	sub_title = "添加基因检测报告"
	model = KawasakiGeneReport
	form_class = KawasakiGeneReportForm

class KawasakiGeneReportUpdateView(KawasakiExtraUpdateView):
	sub_title = "修改基因检测报告"
	model = KawasakiGeneReport
	form_class = KawasakiGeneReportForm

class KawasakiGeneReportDeleteView(KawasakiExtraDeleteView):
	model = KawasakiGeneReport

class KawasakiGeneMutationCreateView(KawasakiExtraCreateView):
	sub_title = "添加基因检测报告内容"
	model = KawasakiGeneMutation
	form_class = KawasakiGeneMutationForm

class KawasakiGeneMutationUpdateView(KawasakiExtraUpdateView):
	sub_title = "修改基因检测报告内容"
	model = KawasakiGeneMutation
	form_class = KawasakiGeneMutationForm

class KawasakiGeneMutationDeleteView(KawasakiExtraDeleteView):
	model = KawasakiGeneMutation

#arrhythmia disease
class ArrhythmiaListView(DiseaseListView):
	model = ArrhythmiaDisease
	template_name = 'arrhythmia-list.html'
	filterset_class = ArrhythmiaDiseaseFilter

class ArrhythmiaCreateView(DiseaseCreateView):
	disease_abbr = 'CA'
	disease_type = '心律失常'
	model = ArrhythmiaDisease
	form_class = ArrhythmiaDiseaseForm
	success_url = reverse_lazy('list-arrhythmia')

class ArrhythmiaUpdateView(DiseaseUpdateView):
	disease_type = '心律失常'
	model = ArrhythmiaDisease
	form_class = ArrhythmiaDiseaseForm
	success_url = reverse_lazy('list-arrhythmia')

class ArrhythmiaDeleteView(DiseaseDeleteView):
	model = ArrhythmiaDisease
	success_url = reverse_lazy('list-arrhythmia')

class ArrhythmiaDetailView(DiseaseDetailView):
	model = ArrhythmiaDisease
	template_name = 'arrhythmia-detail.html'

class ArrhythmiaExtraCreateView(LoginRequiredMixin, CreateView):
	sub_title = ""
	template_name = 'disease-common-form.html'

	def get_success_url(self):
		return reverse('view-arrhythmia', kwargs={'pk': self.object.disease.pk})

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		d = ArrhythmiaDisease.objects.get(pk=self.kwargs['did'])
		context['title'] = "病例 {}".format(d.disease_code)
		context['subtitle'] = self.sub_title
		return context

	def form_valid(self, form):
		form.instance.author = self.request.user
		disease = ArrhythmiaDisease.objects.get(pk=self.kwargs['did'])
		form.instance.disease = disease
		response = super().form_valid(form)

		if 'dicom_file' in form.cleaned_data and self.object.dicom_file:
			study_id = upload_dicoms(self.object.dicom_file.path)
			self.object.dicom_uuid = study_id
			self.object.save()

		return response

class ArrhythmiaExtraUpdateView(LoginRequiredMixin, UpdateView):
	sub_title = ''
	template_name = 'disease-common-form.html'

	def get_success_url(self):
		return reverse('view-arrhythmia', kwargs={'pk': self.object.disease.pk})

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = "病例 {}".format(self.object.disease.disease_code)
		context['subtitle'] = self.sub_title
		return context

	def form_valid(self, form):
		response = super().form_valid(form)

		if form.has_changed() and 'dicom_file' in form.changed_data:
			study_id = upload_dicoms(self.object.dicom_file.path)
			self.object.dicom_uuid = study_id
			self.object.save()

		return response

class ArrhythmiaExtraDeleteView(LoginRequiredMixin, DeleteView):
	template_name = 'disease-common-delete.html'

	def get_success_url(self):
		return reverse('view-arrhythmia', kwargs={'pk': self.object.disease.pk})

class ArrhythmiaBloodCreateView(ArrhythmiaExtraCreateView):
	sub_title = "添加血常规信息"
	model = ArrhythmiaBlood
	form_class = ArrhythmiaBloodForm

class ArrhythmiaBloodUpdateView(ArrhythmiaExtraUpdateView):
	sub_title = "修改血常规信息"
	model = ArrhythmiaBlood
	form_class = ArrhythmiaBloodForm

class ArrhythmiaBloodDeleteView(ArrhythmiaExtraDeleteView):
	model = ArrhythmiaBlood

class ArrhythmiaBiochemistryCreateView(ArrhythmiaExtraCreateView):
	sub_title = "添加生化检验"
	model = ArrhythmiaBiochemistry
	form_class = ArrhythmiaBiochemistryForm

class ArrhythmiaBiochemistryUpdateView(ArrhythmiaExtraUpdateView):
	sub_title = "修改生化检验"
	model = ArrhythmiaBiochemistry
	form_class = ArrhythmiaBiochemistryForm

class ArrhythmiaBiochemistryDeleteView(ArrhythmiaExtraDeleteView):
	model = ArrhythmiaBiochemistry

class ArrhythmiaMarkerCreateView(ArrhythmiaExtraCreateView):
	sub_title = "添加凝血/心肌标志物"
	model = ArrhythmiaMarker
	form_class = ArrhythmiaMarkerForm

class ArrhythmiaMarkerUpdateView(ArrhythmiaExtraUpdateView):
	sub_title = "修改凝血/心肌标志物"
	model = ArrhythmiaMarker
	form_class = ArrhythmiaMarkerForm

class ArrhythmiaMarkerDeleteView(ArrhythmiaExtraDeleteView):
	model = ArrhythmiaMarker

class ArrhythmiaOtherExamineCreateView(ArrhythmiaExtraCreateView):
	sub_title = "添加其他检验/检查"
	model = ArrhythmiaOtherExamine
	form_class = ArrhythmiaOtherExamineForm

class ArrhythmiaOtherExamineUpdateView(ArrhythmiaExtraUpdateView):
	sub_title = "修改其他检验/检查"
	model = ArrhythmiaOtherExamine
	form_class = ArrhythmiaOtherExamineForm

class ArrhythmiaOtherExamineDeleteView(ArrhythmiaExtraDeleteView):
	model = ArrhythmiaOtherExamine

class ArrhythmiaCardiogramCreateView(ArrhythmiaExtraCreateView):
	sub_title = "添加动态心电图"
	model = ArrhythmiaCardiogram
	form_class = ArrhythmiaCardiogramForm

class ArrhythmiaCardiogramUpdateView(ArrhythmiaExtraUpdateView):
	sub_title = "修改动态心电图"
	model = ArrhythmiaCardiogram
	form_class = ArrhythmiaCardiogramForm

class ArrhythmiaCardiogramDeleteView(ArrhythmiaExtraDeleteView):
	model = ArrhythmiaCardiogram

class ArrhythmiaSurgeryCreateView(ArrhythmiaExtraCreateView):
	sub_title = "添加手术情况"
	model = ArrhythmiaSurgery
	form_class = ArrhythmiaSurgeryForm

class ArrhythmiaSurgeryUpdateView(ArrhythmiaExtraUpdateView):
	sub_title = "修改手术情况"
	model = ArrhythmiaSurgery
	form_class = ArrhythmiaSurgeryForm

class ArrhythmiaSurgeryDeleteView(ArrhythmiaExtraDeleteView):
	model = ArrhythmiaSurgery

class ArrhythmiaUltrasoundCreateView(ArrhythmiaExtraCreateView):
	sub_title = "添加超声影像"
	model = ArrhythmiaUltrasound
	form_class = ArrhythmiaUltrasoundForm

class ArrhythmiaUltrasoundUpdateView(ArrhythmiaExtraUpdateView):
	sub_title = "修改超声影像"
	model = ArrhythmiaUltrasound
	form_class = ArrhythmiaUltrasoundForm

class ArrhythmiaUltrasoundDeleteView(ArrhythmiaExtraDeleteView):
	model = ArrhythmiaUltrasound

class ArrhythmiaMRICreateView(ArrhythmiaExtraCreateView):
	sub_title = "添加MRI"
	model = ArrhythmiaMRI
	form_class = ArrhythmiaMRIForm

class ArrhythmiaMRIUpdateView(ArrhythmiaExtraUpdateView):
	sub_title = "修改MRI"
	model = ArrhythmiaMRI
	form_class = ArrhythmiaMRIForm

class ArrhythmiaMRIDeleteView(ArrhythmiaExtraDeleteView):
	model = ArrhythmiaMRI

class ArrhythmiaGeneReportCreateView(ArrhythmiaExtraCreateView):
	sub_title = "添加基因检测报告"
	model = ArrhythmiaGeneReport
	form_class = ArrhythmiaGeneReportForm

class ArrhythmiaGeneReportUpdateView(ArrhythmiaExtraUpdateView):
	sub_title = "修改基因检测报告"
	model = ArrhythmiaGeneReport
	form_class = ArrhythmiaGeneReportForm

class ArrhythmiaGeneReportDeleteView(ArrhythmiaExtraDeleteView):
	model = ArrhythmiaGeneReport

class ArrhythmiaGeneMutationCreateView(ArrhythmiaExtraCreateView):
	sub_title = "添加基因检测报告内容"
	model = ArrhythmiaGeneMutation
	form_class = ArrhythmiaGeneMutationForm

class ArrhythmiaGeneMutationUpdateView(ArrhythmiaExtraUpdateView):
	sub_title = "修改基因检测报告内容"
	model = ArrhythmiaGeneMutation
	form_class = ArrhythmiaGeneMutationForm

class ArrhythmiaGeneMutationDeleteView(ArrhythmiaExtraDeleteView):
	model = ArrhythmiaGeneMutation

#congenital surgery disease
class CongenitalSurgeryDiseaseListView(DiseaseListView):
	model =CongenitalSurgeryDisease
	template_name = 'surgery-list.html'
	filterset_class = CongenitalSurgeryDiseaseFilter

class CongenitalSurgeryDiseaseCreateView(DiseaseCreateView):
	disease_abbr = 'CHS'
	disease_type = '先心病-外科'
	model =CongenitalSurgeryDisease
	form_class =CongenitalSurgeryDiseaseForm
	success_url = reverse_lazy('list-surgery')

class CongenitalSurgeryDiseaseUpdateView(DiseaseUpdateView):
	disease_type = '先心病-外科'
	model =CongenitalSurgeryDisease
	form_class =CongenitalSurgeryDiseaseForm
	success_url = reverse_lazy('list-surgery')

class CongenitalSurgeryDiseaseDeleteView(DiseaseDeleteView):
	model = CongenitalSurgeryDisease
	success_url = reverse_lazy('list-surgery')

class CongenitalSurgeryDiseaseDetailView(DiseaseDetailView):
	model =CongenitalSurgeryDisease
	template_name = 'surgery-detail.html'

class CongenitalSurgeryExtraCreateView(LoginRequiredMixin, CreateView):
	sub_title = ""
	template_name = 'disease-common-form.html'

	def get_success_url(self):
		return reverse('view-surgery', kwargs={'pk': self.object.disease.pk})

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		d = CongenitalSurgeryDisease.objects.get(pk=self.kwargs['did'])
		context['title'] = "病例 {}".format(d.disease_code)
		context['subtitle'] = self.sub_title
		return context

	def form_valid(self, form):
		form.instance.author = self.request.user
		disease = CongenitalSurgeryDisease.objects.get(pk=self.kwargs['did'])
		form.instance.disease = disease
		response = super().form_valid(form)

		if 'dicom_file' in form.cleaned_data and self.object.dicom_file:
			study_id = upload_dicoms(self.object.dicom_file.path)
			self.object.dicom_uuid = study_id
			self.object.save()

		return response

class CongenitalSurgeryExtraUpdateView(LoginRequiredMixin, UpdateView):
	sub_title = ''
	template_name = 'disease-common-form.html'

	def get_success_url(self):
		return reverse('view-arrhythmia', kwargs={'pk': self.object.disease.pk})

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = "病例 {}".format(self.object.disease.disease_code)
		context['subtitle'] = self.sub_title
		return context

	def form_valid(self, form):
		response = super().form_valid(form)

		if form.has_changed() and 'dicom_file' in form.changed_data:
			study_id = upload_dicoms(self.object.dicom_file.path)
			self.object.dicom_uuid = study_id
			self.object.save()

		return response

class CongenitalSurgeryExtraDeleteView(LoginRequiredMixin, DeleteView):
	template_name = 'disease-common-delete.html'

	def get_success_url(self):
		return reverse('view-arrhythmia', kwargs={'pk': self.object.disease.pk})

class CongenitalSurgeryPreBloodCreateView(CongenitalSurgeryExtraCreateView):
	sub_title = "添加术前血常规信息"
	model = CongenitalSurgeryPreBlood
	form_class = CongenitalSurgeryPreBloodForm

class CongenitalSurgeryPreBloodUpdateView(CongenitalSurgeryExtraUpdateView):
	sub_title = "修改术前血常规信息"
	model = CongenitalSurgeryPreBlood
	form_class = CongenitalSurgeryPreBloodForm

class CongenitalSurgeryPreBloodDeleteView(CongenitalSurgeryExtraDeleteView):
	model = CongenitalSurgeryPreBlood

class CongenitalSurgeryPreBiochemistryCreateView(CongenitalSurgeryExtraCreateView):
	sub_title = "添加术前生化检验"
	model = CongenitalSurgeryPreBiochemistry
	form_class = CongenitalSurgeryPreBiochemistryForm

class CongenitalSurgeryPreBiochemistryUpdateView(CongenitalSurgeryExtraUpdateView):
	sub_title = "修改术前生化检验"
	model = CongenitalSurgeryPreBiochemistry
	form_class = CongenitalSurgeryPreBiochemistryForm

class CongenitalSurgeryPreBiochemistryDeleteView(CongenitalSurgeryExtraDeleteView):
	model = CongenitalSurgeryPreBiochemistry

class CongenitalSurgeryPreCruorCreateView(CongenitalSurgeryExtraCreateView):
	sub_title = "添加凝血标志物"
	model = CongenitalSurgeryPreCruor
	form_class = CongenitalSurgeryPreCruorForm

class CongenitalSurgeryPreCruorUpdateView(CongenitalSurgeryExtraUpdateView):
	sub_title = "修改凝血标志物"
	model = CongenitalSurgeryPreCruor
	form_class = CongenitalSurgeryPreCruorForm

class CongenitalSurgeryPreCruorDeleteView(CongenitalSurgeryExtraDeleteView):
	model = CongenitalSurgeryPreCruor

class CongenitalSurgeryPreExamineCreateView(CongenitalSurgeryExtraCreateView):
	sub_title = "添加大小便检"
	model = CongenitalSurgeryPreExamine
	form_class = CongenitalSurgeryPreExamineForm

class CongenitalSurgeryPreExamineUpdateView(CongenitalSurgeryExtraUpdateView):
	sub_title = "修改大小便检"
	model = CongenitalSurgeryPreExamine
	form_class = CongenitalSurgeryPreExamineForm

class CongenitalSurgeryPreExamineDeleteView(CongenitalSurgeryExtraDeleteView):
	model = CongenitalSurgeryPreExamine

class CongenitalSurgeryPreLungCreateView(CongenitalSurgeryExtraCreateView):
	sub_title = "添加术前肺脏情况"
	model = CongenitalSurgeryPreLung
	form_class = CongenitalSurgeryPreLungForm

class CongenitalSurgeryPreLungUpdateView(CongenitalSurgeryExtraUpdateView):
	sub_title = "修改术前肺脏情况"
	model = CongenitalSurgeryPreLung
	form_class = CongenitalSurgeryPreLungForm

class CongenitalSurgeryPreLungDeleteView(CongenitalSurgeryExtraDeleteView):
	model = CongenitalSurgeryPreLung

class CongenitalSurgeryPreCardiogramCreateView(CongenitalSurgeryExtraCreateView):
	sub_title = "添加术前心电图"
	model = CongenitalSurgeryPreCardiogram
	form_class = CongenitalSurgeryPreCardiogramForm

class CongenitalSurgeryPreCardiogramUpdateView(CongenitalSurgeryExtraUpdateView):
	sub_title = "修改术前心电图"
	model = CongenitalSurgeryPreCardiogram
	form_class = CongenitalSurgeryPreCardiogramForm

class CongenitalSurgeryPreCardiogramDeleteView(CongenitalSurgeryExtraDeleteView):
	model = CongenitalSurgeryPreCardiogram

class CongenitalSurgeryPostPHCreateView(CongenitalSurgeryExtraCreateView):
	sub_title = "添加术后PH(酸碱度)"
	model = CongenitalSurgeryPostPH
	form_class = CongenitalSurgeryPostPHForm

class CongenitalSurgeryPostPHUpdateView(CongenitalSurgeryExtraUpdateView):
	sub_title = "修改术后PH(酸碱度)"
	model = CongenitalSurgeryPostPH
	form_class = CongenitalSurgeryPostPHForm

class CongenitalSurgeryPostPHDeleteView(CongenitalSurgeryExtraDeleteView):
	model = CongenitalSurgeryPostPH

class CongenitalSurgeryPostBloodCreateView(CongenitalSurgeryExtraCreateView):
	sub_title = "术后血液系统情况"
	model = CongenitalSurgeryPostBlood
	form_class = CongenitalSurgeryPostBloodForm

class CongenitalSurgeryPostBloodUpdateView(CongenitalSurgeryExtraUpdateView):
	sub_title = "修改血液系统情况"
	model = CongenitalSurgeryPostBlood
	form_class = CongenitalSurgeryPostBloodForm

class CongenitalSurgeryPostBloodDeleteView(CongenitalSurgeryExtraDeleteView):
	model = CongenitalSurgeryPostBlood

class CongenitalSurgeryPostLiverCreateView(CongenitalSurgeryExtraCreateView):
	sub_title = "添加术后肝脏情况"
	model = CongenitalSurgeryPostLiver
	form_class = CongenitalSurgeryPostLiverForm

class CongenitalSurgeryPostLiverUpdateView(CongenitalSurgeryExtraUpdateView):
	sub_title = "修改术后肝脏情况"
	model = CongenitalSurgeryPostLiver
	form_class = CongenitalSurgeryPostLiverForm

class CongenitalSurgeryPostLiverDeleteView(CongenitalSurgeryExtraDeleteView):
	model = CongenitalSurgeryPostLiver

class CongenitalSurgeryPostCruorCreateView(CongenitalSurgeryExtraCreateView):
	sub_title = "添加术后凝血情况"
	model = CongenitalSurgeryPostCruor
	form_class = CongenitalSurgeryPostCruorForm

class CongenitalSurgeryPostCruorUpdateView(CongenitalSurgeryExtraUpdateView):
	sub_title = "修改术后凝血情况"
	model = CongenitalSurgeryPostCruor
	form_class = CongenitalSurgeryPostCruorForm

class CongenitalSurgeryPostCruorDeleteView(CongenitalSurgeryExtraDeleteView):
	model = CongenitalSurgeryPostCruor

class CongenitalSurgeryPostLungCreateView(CongenitalSurgeryExtraCreateView):
	sub_title = "添加术后肺脏情况"
	model = CongenitalSurgeryPostLung
	form_class = CongenitalSurgeryPostLungForm

class CongenitalSurgeryPostLungUpdateView(CongenitalSurgeryExtraUpdateView):
	sub_title = "修改术后肺脏情况"
	model = CongenitalSurgeryPostLung
	form_class = CongenitalSurgeryPostLungForm

class CongenitalSurgeryPostLungDeleteView(CongenitalSurgeryExtraDeleteView):
	model = CongenitalSurgeryPostLung

class CongenitalSurgeryPostCardiogramCreateView(CongenitalSurgeryExtraCreateView):
	sub_title = "添加术后心电图改变"
	model = CongenitalSurgeryPostCardiogram
	form_class = CongenitalSurgeryPostCardiogramForm

class CongenitalSurgeryPostCardiogramUpdateView(CongenitalSurgeryExtraUpdateView):
	sub_title = "修改术后心电图改变"
	model = CongenitalSurgeryPostCardiogram
	form_class = CongenitalSurgeryPostCardiogramForm

class CongenitalSurgeryPostCardiogramDeleteView(CongenitalSurgeryExtraDeleteView):
	model = CongenitalSurgeryPostCardiogram

class CongenitalSurgeryOperationCreateView(CongenitalSurgeryExtraCreateView):
	sub_title = "添加手术情况"
	model = CongenitalSurgeryOperation
	form_class = CongenitalSurgeryOperationForm

class CongenitalSurgeryOperationUpdateView(CongenitalSurgeryExtraUpdateView):
	sub_title = "修改手术情况"
	model = CongenitalSurgeryOperation
	form_class = CongenitalSurgeryOperationForm

class CongenitalSurgeryOperationDeleteView(CongenitalSurgeryExtraDeleteView):
	model = CongenitalSurgeryOperation

class CongenitalSurgeryVentilatorCreateView(CongenitalSurgeryExtraCreateView):
	sub_title = "添加呼吸机使用情况"
	model = CongenitalSurgeryVentilator
	form_class = CongenitalSurgeryVentilatorForm

class CongenitalSurgeryVentilatorUpdateView(CongenitalSurgeryExtraUpdateView):
	sub_title = "修改呼吸机使用情况"
	model = CongenitalSurgeryVentilator
	form_class = CongenitalSurgeryVentilatorForm

class CongenitalSurgeryVentilatorDeleteView(CongenitalSurgeryExtraDeleteView):
	model = CongenitalSurgeryVentilator

class CongenitalSurgeryTreatmentCreateView(CongenitalSurgeryExtraCreateView):
	sub_title = "添加治疗情况"
	model = CongenitalSurgeryTreatment
	form_class = CongenitalSurgeryTreatmentForm

class CongenitalSurgeryTreatmentUpdateView(CongenitalSurgeryExtraUpdateView):
	sub_title = "修改治疗情况"
	model = CongenitalSurgeryTreatment
	form_class = CongenitalSurgeryTreatmentForm

class CongenitalSurgeryTreatmentDeleteView(CongenitalSurgeryExtraDeleteView):
	model = CongenitalSurgeryTreatment

class CongenitalSurgeryUltrasoundCreateView(CongenitalSurgeryExtraCreateView):
	sub_title = "添加超声影像"
	model = CongenitalSurgeryUltrasound
	form_class = CongenitalSurgeryUltrasoundForm

class CongenitalSurgeryUltrasoundUpdateView(CongenitalSurgeryExtraUpdateView):
	sub_title = "修改超声影像"
	model = CongenitalSurgeryUltrasound
	form_class = CongenitalSurgeryUltrasoundForm

class CongenitalSurgeryUltrasoundDeleteView(CongenitalSurgeryExtraDeleteView):
	model = CongenitalSurgeryUltrasound

class CongenitalSurgeryMedimageCreateView(CongenitalSurgeryExtraCreateView):
	sub_title = "添加其他影像"
	model = CongenitalSurgeryMedimage
	form_class = CongenitalSurgeryMedimageForm

class CongenitalSurgeryMedimageUpdateView(CongenitalSurgeryExtraUpdateView):
	sub_title = "修改其他影像"
	model = CongenitalSurgeryMedimage
	form_class = CongenitalSurgeryMedimageForm

class CongenitalSurgeryMedimageDeleteView(CongenitalSurgeryExtraDeleteView):
	model = CongenitalSurgeryMedimage

class CongenitalSurgeryGeneReportCreateView(CongenitalSurgeryExtraCreateView):
	sub_title = "添加基因检测报告"
	model = CongenitalSurgeryGeneReport
	form_class = CongenitalSurgeryGeneReportForm

class CongenitalSurgeryGeneReportUpdateView(CongenitalSurgeryExtraUpdateView):
	sub_title = "修改基因检测报告"
	model = CongenitalSurgeryGeneReport
	form_class = CongenitalSurgeryGeneReportForm

class CongenitalSurgeryGeneReportDeleteView(CongenitalSurgeryExtraDeleteView):
	model = CongenitalSurgeryGeneReport

class CongenitalSurgeryGeneMutationCreateView(CongenitalSurgeryExtraCreateView):
	sub_title = "添加基因检测报告内容"
	model = CongenitalSurgeryGeneMutation
	form_class = CongenitalSurgeryGeneMutationForm

class CongenitalSurgeryGeneMutationUpdateView(CongenitalSurgeryExtraUpdateView):
	sub_title = "修改基因检测报告内容"
	model = CongenitalSurgeryGeneMutation
	form_class = CongenitalSurgeryGeneMutationForm

class CongenitalSurgeryGeneMutationDeleteView(CongenitalSurgeryExtraDeleteView):
	model = CongenitalSurgeryGeneMutation

#congenital VSD disease
class CongenitalInterveneDiseaseListView(DiseaseListView):
	model =CongenitalInterveneDisease
	template_name = 'intervene-list.html'
	filterset_class = CongenitalInterveneDiseaseFilter

class CongenitalInterveneDiseaseCreateView(DiseaseCreateView):
	disease_abbr = 'VSD'
	disease_type = '先心病-VSD介入'
	model =CongenitalInterveneDisease
	form_class =CongenitalInterveneDiseaseForm
	success_url = reverse_lazy('list-intervene')

class CongenitalInterveneDiseaseUpdateView(DiseaseUpdateView):
	disease_type = '先心病-VSD介入'
	model =CongenitalInterveneDisease
	form_class =CongenitalInterveneDiseaseForm
	success_url = reverse_lazy('list-intervene')

class CongenitalInterveneDiseaseDeleteView(DiseaseDeleteView):
	model = CongenitalInterveneDisease
	success_url = reverse_lazy('list-intervene')

class CongenitalInterveneDiseaseDetailView(DiseaseDetailView):
	model =CongenitalInterveneDisease
	template_name = 'intervene-detail.html'

class CongenitalInterveneExtraCreateView(LoginRequiredMixin, CreateView):
	sub_title = ""
	template_name = 'disease-common-form.html'

	def get_success_url(self):
		return reverse('view-intervene', kwargs={'pk': self.object.disease.pk})

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		d = CongenitalInterveneDisease.objects.get(pk=self.kwargs['did'])
		context['title'] = "病例 {}".format(d.disease_code)
		context['subtitle'] = self.sub_title
		return context

	def form_valid(self, form):
		form.instance.author = self.request.user
		disease = CongenitalInterveneDisease.objects.get(pk=self.kwargs['did'])
		form.instance.disease = disease
		response = super().form_valid(form)

		if 'dicom_file' in form.cleaned_data and self.object.dicom_file:
			study_id = upload_dicoms(self.object.dicom_file.path)
			self.object.dicom_uuid = study_id
			self.object.save()

		return response

class CongenitalInterveneExtraUpdateView(LoginRequiredMixin, UpdateView):
	sub_title = ''
	template_name = 'disease-common-form.html'

	def get_success_url(self):
		return reverse('view-intervene', kwargs={'pk': self.object.disease.pk})

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = "病例 {}".format(self.object.disease.disease_code)
		context['subtitle'] = self.sub_title
		return context

	def form_valid(self, form):
		response = super().form_valid(form)

		if form.has_changed() and 'dicom_file' in form.changed_data:
			study_id = upload_dicoms(self.object.dicom_file.path)
			self.object.dicom_uuid = study_id
			self.object.save()

		return response

class CongenitalInterveneExtraDeleteView(LoginRequiredMixin, DeleteView):
	template_name = 'disease-common-delete.html'

	def get_success_url(self):
		return reverse('view-intervene', kwargs={'pk': self.object.disease.pk})

class CongenitalIntervenePreUltrasoundCreateView(CongenitalInterveneExtraCreateView):
	sub_title = "添加术前超声信息"
	model = CongenitalIntervenePreUltrasound
	form_class = CongenitalIntervenePreUltrasoundForm

class CongenitalIntervenePreUltrasoundUpdateView(CongenitalInterveneExtraUpdateView):
	sub_title = "修改术前超声信息"
	model = CongenitalIntervenePreUltrasound
	form_class = CongenitalIntervenePreUltrasoundForm

class CongenitalIntervenePreUltrasoundDeleteView(CongenitalInterveneExtraDeleteView):
	model = CongenitalIntervenePreUltrasound

class CongenitalInterveneCardiogramCreateView(CongenitalInterveneExtraCreateView):
	sub_title = "添加心电图变化情况"
	model = CongenitalInterveneCardiogram
	form_class = CongenitalInterveneCardiogramForm

class CongenitalInterveneCardiogramUpdateView(CongenitalInterveneExtraUpdateView):
	sub_title = "修改心电图变化情况"
	model = CongenitalInterveneCardiogram
	form_class = CongenitalInterveneCardiogramForm

class CongenitalInterveneCardiogramDeleteView(CongenitalInterveneExtraDeleteView):
	model = CongenitalInterveneCardiogram

class CongenitalInterveneOperateCreateView(CongenitalInterveneExtraCreateView):
	sub_title = "添加手术情况"
	model = CongenitalInterveneOperate
	form_class = CongenitalInterveneOperateForm

class CongenitalInterveneOperateUpdateView(CongenitalInterveneExtraUpdateView):
	sub_title = "修改手术情况"
	model = CongenitalInterveneOperate
	form_class = CongenitalInterveneOperateForm

class CongenitalInterveneOperateDeleteView(CongenitalInterveneExtraDeleteView):
	model = CongenitalInterveneOperate

class CongenitalInterveneUltrasoundCreateView(CongenitalInterveneExtraCreateView):
	sub_title = "添加超声影像"
	model = CongenitalInterveneUltrasound
	form_class = CongenitalInterveneUltrasoundForm

class CongenitalInterveneUltrasoundUpdateView(CongenitalInterveneExtraUpdateView):
	sub_title = "修改超声影像"
	model = CongenitalInterveneUltrasound
	form_class = CongenitalInterveneUltrasoundForm

class CongenitalInterveneUltrasoundDeleteView(CongenitalInterveneExtraDeleteView):
	model = CongenitalInterveneUltrasound

class CongenitalInterveneMedimageCreateView(CongenitalInterveneExtraCreateView):
	sub_title = "添加其他影像"
	model = CongenitalInterveneMedimage
	form_class = CongenitalInterveneMedimageForm

class CongenitalInterveneMedimageUpdateView(CongenitalInterveneExtraUpdateView):
	sub_title = "修改其他影像"
	model = CongenitalInterveneMedimage
	form_class = CongenitalInterveneMedimageForm

class CongenitalInterveneMedimageDeleteView(CongenitalInterveneExtraDeleteView):
	model = CongenitalInterveneMedimage

class CongenitalInterveneGeneReportCreateView(CongenitalInterveneExtraCreateView):
	sub_title = "添加基因检测报告"
	model = CongenitalInterveneGeneReport
	form_class = CongenitalInterveneGeneReportForm

class CongenitalInterveneGeneReportUpdateView(CongenitalInterveneExtraUpdateView):
	sub_title = "修改基因检测报告"
	model = CongenitalInterveneGeneReport
	form_class = CongenitalInterveneGeneReportForm

class CongenitalInterveneGeneReportDeleteView(CongenitalInterveneExtraDeleteView):
	model = CongenitalInterveneGeneReport

class CongenitalInterveneGeneMutationCreateView(CongenitalInterveneExtraCreateView):
	sub_title = "添加基因检测报告内容"
	model = CongenitalInterveneGeneMutation
	form_class = CongenitalInterveneGeneMutationForm

class CongenitalInterveneGeneMutationUpdateView(CongenitalInterveneExtraUpdateView):
	sub_title = "修改基因检测报告内容"
	model = CongenitalInterveneGeneMutation
	form_class = CongenitalInterveneGeneMutationForm

class CongenitalInterveneGeneMutationDeleteView(CongenitalInterveneExtraDeleteView):
	model = CongenitalInterveneGeneMutation
