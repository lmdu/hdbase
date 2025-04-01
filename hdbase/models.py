from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class TaskModel(models.Model):
	FAILURE = 0
	SUCCESS = 1
	RUNNING = 2
	WAITING = 3

	STATUS_CHOICES = {
		FAILURE: 'FAILURE',
		SUCCESS: 'SUCCESS',
		RUNNING: 'RUNNING',
		WAITING: 'WAITING'
	}

	short_id = models.CharField(max_length=10, blank=True, default='')
	long_id = models.CharField(max_length=40, blank=True, default='')
	read_one = models.CharField(max_length=100)
	read_two = models.CharField(max_length=100)
	status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=3)
	progress = models.PositiveSmallIntegerField(default=0)
	message = models.TextField(blank=True, default='')
	submit_user = models.ForeignKey(User, on_delete=models.CASCADE)
	submit_time = models.DateTimeField(auto_now_add=True)
	start_time = models.DateTimeField(blank=True, null=True)
	stop_time = models.DateTimeField(blank=True, null=True)

	class Meta:
		ordering = ['-submit_time']


