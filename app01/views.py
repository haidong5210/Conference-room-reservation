from django.shortcuts import render
from app01 import models
# Create your views here.


def index(request):
    meet_time = (
        (1, '8:00'),
        (2, '9:00'),
        (3, '10:00'),
        (4, '11:00'),
        (5, '12:00'),
        (6, '14:00'),
        (7, '15:00'),
        (8, '16:00'),
        (9, '17:00'),
        (10, '18:00'),
        (11, '19:00'),
    )
    boardroom_set = models.Boardroom.objects.all()
    return render(request,"index.html",{"boardroom_set":boardroom_set,"meet_time":meet_time})