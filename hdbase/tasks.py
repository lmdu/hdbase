import time
import traceback

from django.db import transaction
from django.utils import timezone
from django.utils.timesince import timeuntil

from celery import shared_task, Task

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync, sync_to_async

from .models import TaskModel

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
		TaskModel.objects.filter(pk=self.task_pk).update(**kwargs)

		if 'start_time' in kwargs:
			kwargs['start_time'] = kwargs['start_time'].strftime("%Y-%m-%d %H:%M:%S")

		if 'stop_time' in kwargs:
			kwargs['elapse_time'] = timeuntil(kwargs['stop_time'], self.start_time)
			kwargs['stop_time'] = kwargs['stop_time'].strftime("%Y-%m-%d %H:%M:%S")

		self.send_message(kwargs)

@shared_task(base=SocketTask, bind=True)
def human_snp_pipeline(self, pk, r1, r2):
	"""
	@param pk int, the task primary key in database
	@param r1 str, the first fastq file
	@param r2 str, the second fastq file
	"""
	time.sleep(2)
	self.start_time = timezone.now()
	self.task_pk = pk

	self.update_running(
		status = TaskModel.RUNNING,
		start_time = self.start_time
	)

	try:
		for i in range(int(r1)):
			time.sleep(i)
			p = int(i/int(r1)*100)

			self.update_running(
				progress = p,
				message="sleep {} seconds".format(i)
			)

	except:
		status = TaskModel.FAILURE
		message = traceback.format_exc()

	else:
		status = TaskModel.SUCCESS
		message = '任务已成功完成'

	finally:
		self.update_running(
			status = status,
			message = message,
			progress = 100,
			stop_time = timezone.now()
		)