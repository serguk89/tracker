#!/usr/bin/env python3

from tracker.mqtt import Mqtt
from tracker.models import Task, UserTask


def on_message(self, mosq, obj, message):
    print(str(message.payload, 'utf-8'))


def db_sync():
    stored = [x.name for x in Task.objects.all()]
    if tuple(stored) == TASKS: return
    for task in tuple(set(tuple(stored)) ^ set(TASKS)):
        Task.objects.create(name=task)


def do_user_tasks(user, inout=True):
    for task in UserTask.objects.filter(user_id=user):
        globals()[str(task.task.name).lower().replace(' ', '_')](user, inout)


def turn_lamp_on(user, inout=True):
    if inout:
        mqtt_client.send(topic='room1', message=1)
    else:
        mqtt_client.send(topic='room1', message=0)


TASKS = ('Turn Lamp On', )
mqtt_client = Mqtt(ip='192.168.0.2', port=8883, username='pi', password='123456', subscription='server', on_message=on_message)
db_sync()