import json
import random

from django.http import HttpResponse
from django.utils import timezone
from barcode.models import Trace, PermanentTrace
from list.models import Products
from place.models import PlaceData
from session.models import UserData
from stage.models import StageData, Quantity


# Create your views here.


def generate(request):
    data = json.loads(request.body)
    length = 12 - len(str(data['maxQuantity']))
    sno = random.randrange(10**(length-2), 10**(length-1)-1)
    sno_final = sno*(10**(13-length))+1
    for e in Quantity.objects.all():
        if not e.start_sno.find(str(sno)) == -1:
            generate(request)
    return HttpResponse(sno_final)


def index(request):
    data = json.loads(request.body)

    # Mandatory checks
    if not check_correct_product(data):
        return HttpResponse('Product barcode mismatch')

    if check_previous_stages(data):
        return HttpResponse('Product not scanned at previous stage:' + check_previous_stages(data))

    if check_place(data):
        return HttpResponse('Product not scanned at the start')

    if check_multiple_scans(data):
        return HttpResponse('Multiple scans detected at the same stage')

    # Creating permanent trace
    r = PermanentTrace(sno=data['barcode'])
    r.save()

    # Logging the scan with details
    q = Trace(username=UserData.objects.get(username__exact=data['username']), sno_id=data['barcode'],
              stage=StageData.objects.get(line_code__exact=data['stage']), time=timezone.now(), place=data['place'],
              description=data['description'], product_name=Products.objects.get(product_name__exact=data['product']))
    q.save()

    # Updating quantity
    if data['place'] == 'start':
        e = Quantity.objects.get(product_name_id__exact=data['product'], line_code_id__exact=data['stage'])
        p = Quantity(id=e.id, current_quantity=e.current_quantity+1, product_name_id=e.product_name_id, line_code_id=e.line_code_id, max_quantity=e.max_quantity, start_sno=e.start_sno, end_sno=e.end_sno)
        p.save()

    # Check for final stage
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


def check_correct_product(data):
    q = Quantity.objects.get(product_name_id__exact=data['product'], line_code_id__exact=data['stage'])
    if int(data['barcode']) in range(int(q.start_sno), int(q.end_sno)):
        return True
    return False



