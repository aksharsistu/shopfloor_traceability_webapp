import json
from django.http import HttpResponse
from django.utils import timezone
from barcode.models import Trace, PermanentTrace
from list.models import Products
from place.models import PlaceData
from session.models import UserData
from stage.models import StageData


# Create your views here.


def index(request):
    data = json.loads(request.body)

    if check_previous_stages(data):
        return HttpResponse('Product not scanned at previous stage:' + check_previous_stages(data))

    if check_place(data):
        return HttpResponse('Product not scanned at the start')

    if check_multiple_scans(data):
        return HttpResponse('Multiple scans detected at the same stage')

    r = PermanentTrace(sno=data['barcode'])
    r.save()
    q = Trace(username=UserData.objects.get(username__exact=data['username']), sno_id=data['barcode'],
              stage=StageData.objects.get(line_code__exact=data['stage']), time=timezone.now(), place=data['place'],
              description=data['description'], product_name=Products.objects.get(product_name__exact=data['product']))
    q.save()
    if len(data['description']) == 13:
        r = PermanentTrace(sno=data['barcode'], permanent_sno=data['description'])
        r.save()
        return HttpResponse('Barcodes Linked Successfully: ' + data['barcode'] + '/' + data['description'])

    return HttpResponse('Successfully scanned: ' + data['barcode'])


def check_multiple_scans(data):
    return Trace.objects.all().filter(sno__exact=data['barcode']).filter(stage_id__exact=data['stage']).filter(place__exact=data['place']).exists() and not \
            data['override']


def check_previous_stages(data):
    process_id = Products.objects.get(product_name__exact=data['product']).process.pid
    index_val = 0
    arr = process_id.split('-')
    for i in range(0, len(arr)):
        if arr[i] == data['stage']:
            index_val = i
    for i in range(0, index_val):
        try:
            last_stage = PlaceData.objects.get(stage_id__exact=arr[i]).final
        except PlaceData.DoesNotExist:
            last_stage = ""
        if not Trace.objects.all().filter(sno__exact=data['barcode']).filter(stage_id__exact=arr[i]).filter(product_name_id__exact=data['product']).filter(place__exact=last_stage).exists():
            return arr[i] + last_stage
    return 0


def check_place(data):
    if data['place'] != "start" and not Trace.objects.all().filter(sno__exact=data['barcode']).filter(stage_id__exact=data['stage']).filter(place__exact="start").exists():
        return True
    return False
