from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from Lemoncello.Apps.fraid.models import *
from Lemoncello.Apps.fraid.forms import *
from Lemoncello.Apps.fraid.serializers import *
from django.views.generic import View, TemplateView

from rest_framework import generics, viewsets
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

from pusher import Pusher
import json

import Sada.response_module as resmod
from Sada.Classifier.classifier_tree import *
import queue
import time
import random as rd
from datetime import datetime

rd.seed(datetime.now())


#instantiate pusher

pusher = Pusher(app_id=u'901958', key=u'd3c25f2bb99c1dada587', secret=u'3f23a3951ac08b81070b', cluster=u'us2')
pusher2 = Pusher(app_id=u'901958', key=u'd3c25f2bb99c1dada587', secret=u'3f23a3951ac08b81070b', cluster=u'us2')

def pusher_authentication(request):
    channel = request.GET.get('channel_name', None)
    socket_id = request.GET.get('socket_id', None)
    auth = pusher.authenticate(
      channel = channel,
      socket_id = socket_id
    )
 
    return JsonResponse(json.dumps(auth), safe=False)
"""TODO: Convert events from numbers to their respecive names 
Ex: 0->'HUMAN_CROWDS+CHILDREN+FOOTSTEPS', 1->'COMEDY+FANTASY+HUMOR', 3->''SCHOOLS&CROWDS', etc
After that, it classifies it as the 'more general events' (NonMechanic, Mechanic, etc)"""
def convert_events(event_keys, num_of_event):  # Can be used for dashboard
    event_name = event_keys[num_of_event]
    return event_name

# Decrements one second
def decounter(vclock, event_dict):
    time_per_event = vclock.time_per_event

    for event, time in time_per_event.items():
        if time >= 1:
            #print("Decounter: ")
            vclock.decrement_event(event, 1)
            #print(time_per_event)
    #print(time_per_event)

def validator(triggered_events, vclock, validator_clock):
    validator_dict = validator_clock.time_per_event
    print("triggered events:", triggered_events)
    
    for name_of_event, value in validator_dict.items():
        validator_clock.increment_event(name_of_event,1)
        #print("entro", name_of_event, value)
        if value == 8:
            vclock.restart_event(name_of_event)
            validator_clock.restart_event(name_of_event)
            #print("reseteo!!", name_of_event)
    #print("paso1: ",validator_dict)

    for event in triggered_events:
    	print("vclock: ",vclock.consult_event(event))
    	for name_of_event in validator_dict.keys():
    		if name_of_event == event:
    			validator_clock.restart_event(name_of_event)  # Event happened, reset    
    #print("Paso2: ",validator_dict)

            
def generate_events():
    num_of_events = rd.randrange(1,3)
    events = output_events_randomly(num_of_events)
    #print(events)
    return events
# Output a few events randomly
class EventView(viewsets.ModelViewSet):
	queryset = Event.objects.all()
	serializer_class = EventSerializer

	def get_object(self):
		queryset = self.get_queryset()
		obj = get_object_or_404(
			queryset,
			pk=self.kwargs['pk'],
			)
		return obj


#@login_required
def profile(request):
	context = {
		'usuario': request.user
	}
	return render(request, 'profile/profile.html', context)


def ambient(request):
	return render(request, "smartroom/ambient.html", {})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'login/signup.html', {'form': form})

def classifierM(request):
	return render(request, 'classifierModule.html', {})

def response(request):
	return render(request, 'responseModule.html', {})

def randomColor():
	color = ['#FA8072', '#CD5C5C', '#61BED4', '#61D498', '#F1B636', '#F17D51', '#709CF6', 
	'#B970F6', '#B1F3EB']
	return rd.choice(color)


class Dashboard(TemplateView):
	def get(self, request):
		events = Event.objects.all().delete()
		alerts = Alert.objects.all().delete()

		return render(request, "dashboard/dashboard.html", {})

@csrf_exempt
def broadcast(request):
	env_events = resmod.EnvironmentEvents()
	event_keys = env_events.eventKeys
	vclock = resmod.VirtualClock(event_keys)  # Used to track events time
	validator_clock = resmod.VirtualClock(event_keys)  # Used to reset events (of vclock) if they don't happen for some time
	time_per_event = vclock.time_per_event
	resp = resmod.ResponseClass()
	stop = 4 #Number of iterations 

	while True:
		events = generate_events()
		triggered_events = []
		color = randomColor()

		for event in events:
			name_of_event = convert_events(event_keys, event[0])  # Search name by number
			vclock.increment_event(name_of_event, event[1])  # Increment time value of that event
			triggered_events.append(name_of_event)
			#kind_of_event = env_events.event_dict[name_of_event]
			name = convert_events(event_keys, event[0])
			
			eventObj = Event.objects.create(classId=event[0], className=name, length=event[1], startDate=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), audioFile="media/audio/"+name+".wav", color=color)
			pusher.trigger(u'a_channel', u'an_event', {u'classId': eventObj.classId,
			 u'className': eventObj.className, u'length': eventObj.length,
			 u'startDate':eventObj.startDate,u'id':eventObj.id, u'audioFile':eventObj.audioFile,
			 u'accumulated': vclock.consult_event(name_of_event), u'color': color})
			print('ok')
			response = resp.calculate_response(time_per_event)
			print(response)

			if response:
				alert = Alert.objects.create(alertMessage=response, 
											 date = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
											 color = color)
				alert.setEvents(triggered_events)
				alert.save()
				pusher2.trigger(u'a_channel', u'an_alert', {u'alertMessage': alert.alertMessage, 
															u'date': alert.date,
															u'events': alert.events,
															u'color': color})
		
			time.sleep(2)# Delay between events		  

		decounter(vclock, events)
		triggerev = validator(triggered_events, vclock, validator_clock)

		time.sleep(2)

		if stop < 1:
			break
		else:
			stop -= 1
	return JsonResponse(event, safe=False)


def events(request):
    data = Event.objects.all().order_by('-id')
    data = [{ 'classId': event.classId, 'className': event.className, 'id': event.id,
     'length': event.length, 'startDate': event.startDate,
      'audioFile': event.audioFile, 'accumulated':event.accumulated,
      'color': event.color} for event in data]
    return JsonResponse(data, safe=False)

def alerts(request):
	data = Alert.objects.all().order_by('-id')
	data =  [{ 'alertMessage': alert.alertMessage, 'date': alert.date, 'events': alert.events,
				'color': alert.color} for alert in data]
	return JsonResponse(data, safe=False)

@csrf_exempt
def delivered(request, id):
	event = Event.objects.get(pk=id)
	socket_id = request.POST.get('socket_id', '')
	event.save();
	event = {'classId': event.classId,'className': event.className,
	 'length': event.length, 'id': event.id, 'startDate':event.startDate,
	  'audioFile':event.audioFile, 'accumulated':event.accumulated, 'color': event.color}
	pusher.trigger(u'a_channel', u'delivered_event', event, socket_id)
	return HttpResponse('ok')


@csrf_exempt
def alerted(request, id):
	alert = Alert.objects.get(pk=id)
	socket_id = request.POST.get('socket_id', '')
	alert.save();
	alert = { 'alertMessage': alert.alertMessage, 'date': alert.date, 'events': alert.events, 'color':alert.color}
	pusher.trigger(u'a_channel', u'alerted_event', alert, socket_id)
	return HttpResponse('ok alert')
