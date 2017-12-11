import json
from django.shortcuts import render,HttpResponse
from app01 import models
from django.http import JsonResponse
# Create your views here.


def login(request):
    if request.is_ajax():
        user = request.POST.get("user")
        pwd = request.POST.get("password")
        user_obj = models.User.objects.filter(name=user,password=pwd).first()
        login = {"log":False}
        if user_obj:
            login['log'] = True
            request.session['user'] = {"password":user_obj.password,"name":user_obj.name,"id":user_obj.id}
        return HttpResponse(json.dumps(login))
    else:
        return render(request,"login.html")


def index(request):
    meet_time = models.Boardroom2Time2user.meetTime
    room_set = models.Boardroom.objects.all()

    return render(request,"index.html",{"meet_time":meet_time,"room_set":room_set})


def book(request):
    date = request.GET.get("choice_data")
    book_set = models.Boardroom2Time2user.objects.filter(time=date)
    book_dict = {}
    for bk in book_set:
        if bk.boardroom_id not in book_dict:
            book_dict[bk.boardroom_id]={bk.meet_time:bk.user.name}
        else:
            book_dict[bk.boardroom_id][bk.meet_time]=bk.user.name
    """
    dict = {
        会议室id:{
            时间段id：user_id,
            时间段id：user_id,
           }     
        
    }
    """
    response = {"status":True,"error":None,"data":None}
    #处理预定信息
    # {}
    try:
        data = []
        room_set = models.Boardroom.objects.all()
        for room in room_set:
            data_list = []
            data_list.append({"text":room.title})
            for time in models.Boardroom2Time2user.meetTime:
                if room.id in book_dict and time[0] in book_dict[room.id]:
                    data_list.append({"text":book_dict[room.id][time[0]],"attrs":{"room_id":room.id,"time_id":time[0]},"class":"bg"})
                else:
                    data_list.append({"text": "", "attrs": {"room_id": room.id, "time_id": time[0]},"class":"cli"})
            data.append(data_list)
        # data = [
        #     [{"name":"天使"},{"name":"","attrs":{}},{"name":""},{"name":""},{"name":""},{"name":""}],
        # ]
        response["data"] = data
    except Exception as e:
        response["status"] = False
        response["error"] = str(e)
    return JsonResponse(response)