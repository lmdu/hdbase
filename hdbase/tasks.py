import time
import random
import traceback

from django.db import transaction
from django.utils import timezone
from django.utils.timesince import timeuntil

from celery import shared_task, Task

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync, sync_to_async

from .models import Task as Job

class SocketTask(Task):
	task_pk = None
	channel_layer = get_channel_layer()

	def send_message(self, message):
		message['task_id'] = self.task_pk

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

@shared_task(base=SocketTask, bind=True)
def call_snp_from_ges(self, pk):
	pass

@shared_task(base=SocketTask, bind=True)
def test_pipeline(self, pk):
	"""
	@param pk int, the task primary key in database
	"""
	time.sleep(2)
	self.start_time = timezone.now()
	self.task_pk = pk

	self.update_running(
		status = 2,
		started = self.start_time
	)

	try:
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