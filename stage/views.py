import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from stage.models import Stages, StageData, Quantity


# Create your views here.


def set_stage(request):
    data = json.loads(request.body)
    q = Stages(ip=data['ip'], line_code=StageData.objects.get(line_code__exact=data['stage_id']), place=data['place'])
    q.save()
    return HttpResponse('success')


def get_stage(request):
    ip = request.META.get('REMOTE_ADDR')
    try:
        s = Stages.objects.get(ip__exact=ip)
    except Stages.DoesNotExist:
        return JsonResponse({"stage": "not", "place": "defined"})
    return JsonResponse({"stage": s.line_code.line_code, "place": s.place})


def delete_stage(request):
    data = json.loads(request.body)
    try:
        s = Stages.objects.get(ip__exact=data['ip'])
        s.delete()
        return HttpResponse('success')
    except Stages.DoesNotExist:
        return HttpResponse('IP Address Does not exist. Server Error')


def get_stage_data(request):
    stage_list = []
    for e in Stages.objects.all():
        stage_list.append({"stage": e.line_code.line_code, "ip": e.ip, "place": e.place})
    return JsonResponse(stage_list, safe=False)


def get_stage_list(request):
    stage_list = []
    for e in StageData.objects.all():
        stage_list.append(str(e.line_code))
    return JsonResponse(stage_list, safe=False)


def get_quantity(request):
    data = json.loads(request.body)
    try:
        e = Quantity.objects.get(product_name_id__exact=data['product'], line_code_id__exact=data['stage'])
    except Quantity.DoesNotExist:
        return HttpResponse('Product/Stage invalid')
    return HttpResponse(e.current_quantity)
