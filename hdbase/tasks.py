import time
import random
import tempfile
import traceback

from django.db import transaction
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.timesince import timeuntil

from celery import shared_task, Task

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync, sync_to_async

from .models import *
from .pipeline import *
from .utils import *
from .loads import *

class SocketTask(Task):
	task_pk = None
	task_type = 'task'
	channel_layer = get_channel_layer()

	def send_message(self, message):
		message['task_id'] = self.task_pk
		message['task_type'] = self.task_type

		async_to_sync(self.channel_layer.group_send)('tasks',
			{
				'type': 'send.message',
				'message': message
			}
		)

	def update_running(self, **kwargs):
		#self.update_state(state='PROGRESS', meta=kwargs)
		Job.objects.filter(pk=self.task_pk).update(**kwargs)

		if 'started' in kwargs:
			kwargs['started'] = kwargs['started'].strftime("%Y-%m-%d %H:%M:%S")

		if 'stopped' in kwargs:
			kwargs['elapsed'] = timeuntil(kwargs['stopped'], self.start_time)
			kwargs['stopped'] = kwargs['stopped'].strftime("%Y-%m-%d %H:%M:%S")

		self.send_message(kwargs)

	def do_step(self, step, progress, func):
		self.update_running(step=step)
		func()
		self.update_running(progress=progress)

class ImportTask(SocketTask):
	task_type = 'import'

	def update_running(self, **kwargs):
		DiseaseImport.objects.filter(pk=self.task_pk).update(**kwargs)
		self.send_message(kwargs)


@shared_task(base=SocketTask, bind=True)
def call_snp_from_ges(self, task_pk, task_id, params):
	"""
	@param task_pk int, the task primary key in database
	@param task_id str, the short hash id of the task
	@param params dict, the parameter for this pipeline
	"""
	time.sleep(2)
	self.start_time = timezone.now()
	self.task_pk = task_pk
	self.task_id = task_id

	self.update_running(
		status = 2,
		started = self.start_time
	)

	try:
		pipeline = WESPipeline(task_id, params)

		for step in pipeline.steps:
			self.do_step(**step)

	except:
		status = 0
		message = traceback.format_exc()
		print(message)

	else:
		status = 1
		message = '任务已成功完成'

	finally:
		self.update_running(
			status = status,
			message = message,
			progress = 100,
			stopped = timezone.now()
		)
		#self.temp_dir.cleanup()


@shared_task(base=ImportTask, bind=True)
def import_cardiomyopathy(self, task_pk, excel_file, author_id):
	self.task_pk = task_pk

	self.update_running(status=2, message="运行中...")

	try:
		author = User.objects.get(id=author_id)

		with transaction.atomic():
			load_data_into_cardiomyopathy(excel_file, author)

		self.update_running(status=1, message="导入成功")

	except Exception as e:
		print(traceback.format_exc())
		self.update_running(status=0, message=str(e))

	finally:
		pass

@shared_task(base=SocketTask, bind=True)
def test_pipeline(self, task_pk, task_id, params):
	"""
	@param pk int, the task primary key in database
	"""
	time.sleep(2)
	self.start_time = timezone.now()
	self.task_pk = task_pk

	self.update_running(
		status = 2,
		started = self.start_time
	)

	try:
		print(params)

		num = random.randint(5, 20)
		for i in range(num):
			time.sleep(i)
			p = int(i/num*100)

			self.update_running(
				progress = p,
				message="sleep {} seconds".format(i)
			)

	except:
		status = 0
		message = traceback.format_exc()

	else:
		status = 1
		message = '任务已成功完成'

	finally:
		self.update_running(
			status = status,
			message = message,
			progress = 100,
			stopped = timezone.now()
		)