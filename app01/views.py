import json
from django.shortcuts import render,HttpResponse,redirect
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
    if request.is_ajax():
        dict = {"status":True,"error":None}
        try:
            data_dict = json.loads(request.POST.get("data"))
            if not data_dict["add"] and not data_dict["edit"]:
                dict["status"] = False
                dict["error"] = "请选择之后提交"
            if data_dict["add"]:
                for data in data_dict["add"]:
                    models.Boardroom2Time2user.objects.create(**data)
            if data_dict["edit"]:
                for edit_data in data_dict["edit"]:
                    models.Boardroom2Time2user.objects.filter(**edit_data,user_id=request.session["user"]["id"]).delete()
        except Exception as e:
            dict["status"] = False
            dict["error"] = str(e)
        return JsonResponse(dict)
    else:
        if request.session.get("user"):
            meet_time = models.Boardroom2Time2user.meetTime
            return render(request,"index.html",{"meet_time":meet_time,})
        else:
            return redirect('/login/')


def book(request):
    """
    处理如何在前端显示以选择的会议室
    :param request:
    :return:
    """
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
            时间段id：user_name,
            时间段id：user_name,
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
                    if request.session["user"]["name"] == book_dict[room.id][time[0]]:
                        data_list.append(
                        {"text":book_dict[room.id][time[0]],"attrs":{"room_id":room.id,"time_id":time[0]},"class":"mySlfe"})
                    else:
                        data_list.append(
                            {"text": book_dict[room.id][time[0]], "attrs": {"room_id": room.id, "time_id": time[0]},
                             "class": "bg"})
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
