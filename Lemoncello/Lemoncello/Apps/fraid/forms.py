from django import forms
from Lemoncello.Apps.fraid.models import *


class EventForm(forms.ModelForm):
	class Meta:
		model = Event
		fields = '__all__'