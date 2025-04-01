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
#@login_required
def index(request):
	#add.delay(1,2)
	return render(request, 'index.html')

#@login_required
class TaskListView(LoginRequiredMixin, ListView):
	model = TaskModel
	template_name = 'task-list.html'
	context_object_name = 'tasks'
	paginate_by = 10

class TaskCreateView(LoginRequiredMixin, CreateView):
	model = TaskModel
	#form_class = TaskForm
	success_url = reverse_lazy('task')
	http_method_names = ['post']

	fields = ['read_one', 'read_two']

	def form_valid(self, form):
		form.instance.submit_user = self.request.user
		response = super().form_valid(form)
		tid = self.object.id
		r1 = form.cleaned_data['read_one']
		r2 = form.cleaned_data['read_two']

		def on_commit():
			obj = TaskModel.objects.get(id=tid)
			task = human_snp_pipeline.delay(tid, r1, r2)
			obj.long_id = task.id
			obj.short_id = task.id[0:8]
			obj.save()

		transaction.on_commit(on_commit)
		return response
