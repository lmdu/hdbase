from django.urls import reverse, reverse_lazy
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import *
from .forms import *

# Create your views here.
def sign_in(request):
	if request.user.is_authenticated:
		return redirect('index')

	elif request.method == 'GET':
		return render(request, 'signin.html')

	elif request.method == 'POST':
		user_id = request.POST.get('userid')
		user_pwd = request.POST.get('userpass')

		user = None
		if '@' in user_id:
			user = authenticate(email=user_id, password=user_pwd)

		if not user:
			user = authenticate(username=user_id, password=user_pwd)

		if user:
			if user.profile.role == 0:
				messages.error(request, "你的帐号未激活, 请联系管理员审核")
				return render(request, 'error.html')

			login(request, user)
			return redirect('index')
		else:
			messages.error(request, "帐号或密码错误")
			return redirect('signin')

def sign_out(request):
	if request.user.is_authenticated:
		logout(request)
		return redirect('signin')

def sign_up(request):
	if request.user.is_authenticated:
		return redirect('index')

	elif request.method == 'GET':
		return render(request, 'signup.html')

	elif request.method == 'POST':
		user = User.objects.create_user(
			username = request.POST.get('username'),
			password = request.POST.get('userpass'),
			email = request.POST.get('useremail'),
			first_name = request.POST.get('userfirst'),
			last_name = request.POST.get('userlast')
		)

		return redirect('signin')

def sign_valid(request):
	if request.method == 'POST':
		if 'username' in request.POST:
			user_name = request.POST.get('username')
			query = User.objects.filter(username=user_name)

		elif 'useremail' in request.POST:
			user_email = request.POST.get('useremail')
			query = User.objects.filter(email=user_email)

		elif 'sampleid' in request.POST:
			sample_id = request.POST.get('sampleid')
			query = Sample.objects.filter(sample_code=sample_id)

		elif 'specimenid' in request.POST:
			specimen_id = request.POST.get('specimenid')
			query = Specimen.objects.filter(specimen_code=specimen_id)

		elif 'speciesid' in request.POST:
			species_id = request.POST.get('speciesid')
			query = Species.objects.filter(species_en=species_id)

		return HttpResponse(str(not query.exists()).lower())

def setpass(request, action):
	if not request.user.is_authenticated:
		return redirect('signin')

	if action == 'view':
		if request.method == 'GET':
			return render(request, 'setpass.html')

	elif action == 'edit':
		if request.method == 'POST':
			uid = int(request.POST.get('uid'))
			old = request.POST.get('old_passwd')
			new = request.POST.get('new_passwd')
			user = User.objects.get(pk=uid)

			if user.check_password(old):
				user.set_password(new)
				user.save()
				logout(request)
				return redirect('signin')
			else:
				messages.error(request, "输入的原始密码错误!")
				return render(request, 'error.html')

class CustomerListView(LoginRequiredMixin, ListView):
	model = Profile
	template_name = 'customer-list.html'
	context_object_name = 'customers'
	paginate_by = 10

class CustomerUpdateView(LoginRequiredMixin, UpdateView):
	model = Profile
	form_class = ProfileForm
	template_name = 'customer-edit.html'
	success_url = reverse_lazy('list-customer')

class CustomerDeleteView(LoginRequiredMixin, DeleteView):
	model = Profile
	template_name = 'customer-delete.html'
	success_url = reverse_lazy('list-customer')

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
	model = Profile
	form_class = ProfileForm
	template_name = 'profile-edit.html'
	success_url = reverse_lazy('profile')

	def get_object(self):
		return self.request.user.profile

class PasswordUpdateView(LoginRequiredMixin, UpdateView):
	model = Profile
	template_name = 'setpass.html'
	success_url = reverse_lazy('setpass')
