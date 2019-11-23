from django.db import models
from django.conf import settings
import json

class Event(models.Model):
	classId = models.PositiveIntegerField()
	className = models.CharField(max_length=200)
	length = models.PositiveIntegerField(default=1)
	audioFile = models.CharField(max_length=500)
	startDate = models.CharField(max_length=200)
	accumulated = models.PositiveIntegerField(default=0)
	color = models.CharField(max_length=200, default='')

	def __str__(self):
		return self.className

class Alert(models.Model):
	alertMessage = models.CharField(max_length=1000, null=True)
	date = models.CharField(max_length=200)
	events = models.CharField(max_length=3000, default='')
	color = models.CharField(max_length=200, default='')

	def setEvents(self, e):
		e = json.dumps(e)
		print('dumped: ', e)

		self.events = e.replace("[", "").replace("]", "").replace('"', '').replace(",", " ")

	def __str__(self):
		return self.alertMessage