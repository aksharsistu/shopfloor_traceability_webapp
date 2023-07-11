import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from place.models import PlaceData


# Create your views here.


def set_place(request):
    # Clearing previous data:
    delete_place(request)

    data = json.loads(request.body)
    q = PlaceData(process_id=data['process'], stage_id=data['stage'], start=data['start'], end=data['end'], qa=data['qa'], rework=data['rework'], final=data['final'])
    q.save()
    return HttpResponse('Success')


def get_place(request):
    data = json.loads(request.body)
    try:
        e = PlaceData.objects.get(stage_id__exact=data['stage'])
        places = {"start": e.start, "end": e.end, "qa": e.qa, "rework": e.rework}
        return JsonResponse(places)
    except PlaceData.DoesNotExist:
        return JsonResponse({"start": False, "end": False, "qa": False, "rework": False})


def delete_place(request):
    data = json.loads(request.body)
    try:
        e = PlaceData.objects.get(process_id=data['process'], stage_id=data['stage'])
        e.delete()
    except PlaceData.DoesNotExist:
        print('no data to delete')
    return HttpResponse('success')
