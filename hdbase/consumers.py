import json
import psutil
import asyncio

from channels.generic.websocket import AsyncWebsocketConsumer

class CelerySocketioConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.group_name = 'tasks'
		await self.channel_layer.group_add(self.group_name, self.channel_name)
		await self.accept()
		self.connected = True
		asyncio.create_task(self.send_usage())

	async def disconnect(self, close_code):
		await self.channel_layer.group_discard(self.group_name, self.channel_name)
		self.connected = False

	async def receive(self, text_data):
		text_data_json = json.loads(text_data)
		message = text_data_json["message"]

	async def send_message(self, event):
		message = event['message']
		await self.send(text_data=json.dumps(message))

	async def send_usage(self):
		while self.connected:
			mem = psutil.virtual_memory()
			cpus = len([p for p in psutil.cpu_percent(percpu=True) if p > 0])

			await self.send(text_data=json.dumps({
				'memory': {
					'avail': round(mem.available/1024/1024/1024, 2),
					'percent': round(mem.percent, 2),
				},
				'cpu': {
					'percent': round(psutil.cpu_percent(), 2),
					'activep': round(cpus/psutil.cpu_count()*100, 2),
					'activec': cpus,
				}
			}))
			await asyncio.sleep(1)
