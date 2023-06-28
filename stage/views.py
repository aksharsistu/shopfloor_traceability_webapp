import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from stage.models import Stages, StageData


# Create your views here.


def set_stage(request):
    data = json.loads(request.body)
    q = Stages(ip=data['ip'], line_code=StageData.objects.get(line_code__exact=data['stage_id']))
    q.save()
    return HttpResponse('success')


def get_stage(request):
    ip = request.META.get('REMOTE_ADDR')
    try:
        s = Stages.objects.get(ip__exact=ip)
    except Stages.DoesNotExist:
        return HttpResponse('not defined')
    return HttpResponse(s.line_code.line_code)


def delete_stage(request):
    data = json.loads(request.body)
    s = Stages.objects.get(ip__exact=data['ip'])
    s.delete()
    return HttpResponse('success')


def get_stage_data(request):
    stage_list = []
    for e in Stages.objects.all():
        stage_list.append({"stage": e.line_code.line_code, "ip": e.ip})
    return JsonResponse(stage_list, safe=False)
