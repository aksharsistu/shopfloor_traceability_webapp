import json
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.utils import timezone
from barcode.models import Barcode, Permanent
from process.models import ProcessData, Quantity
from product.models import ProductData, ProductList


def log(request):
    data = json.loads(request.body)

    # Mandatory checks:
    if not check_correct_product(data):
        return HttpResponse('Product barcode mismatch')

    if check_previous_stages(data):
        return HttpResponse('Product not scanned at previous stage: ' + check_previous_stages(data))

    if check_place(data):
        return HttpResponse('Product not scanned at the start')

    if check_multiple_scans(data):
        return HttpResponse('Multiple scans detected at the same stage/place')

    # Update Quantity:
    try:
        # Stage wise quantities in the Quantity Model:
        e = ProductData.objects.all().filter(productName_id__exact=data['productName'])\
            .get(stageName_id__exact=data['stageName'])
        if data['placeName'] == e.final:
            k = Quantity.objects.get(processNo_id__exact=data['processNo'], stageName_id=data['stageName'])
            k.quantity = k.quantity + 1
            k.save()
        # Overall Quantity in the ProcessData model:
        quantities = []
        p = ProcessData.objects.get(processNo=data['processNo'])
        for r in Quantity.objects.all().filter(processNo_id__exact=data['processNo']):
            quantities.append(r.quantity)
        p.currentQuantity = min(quantities)
        p.save()
    except ProductData.DoesNotExist:
        return HttpResponseBadRequest('Error updating the quantity')
    except ProcessData.DoesNotExist:
        return HttpResponseBadRequest('Error updating the quantity')
    except Quantity.DoesNotExist:
        return HttpResponseBadRequest('Error updating the quantity')

    # Logging the barcode:
    q = Barcode(barcode=data['barcode'], description=data['description'], processNo_id=data['processNo'],
                productName_id=data['productName'], stageName_id=data['stageName'], placeName=data['placeName'],
                username_id=data['username'], timestamp=timezone.now())
    q.save()

    # Linking the permanent and temporary barcodes:
    if len(data['description']) == 13:
        q = Permanent(barcode=data['barcode'], permanent=data['description'])
        q.save()
        return HttpResponse('Successfully Linked' + data['barcode'] + ' / ' + data['description'])

    return HttpResponse('Successfully scanned: ' + data['barcode'])


def check(request):
    data = json.loads(request.body)
    try:
        if data['placeName'] == 'start':
            return JsonResponse({'disable': not ProductData.objects.get(productName_id=data['productName'],
                                                                        stageName_id=data['stageName']).start})
        if data['placeName'] == 'end':
            return JsonResponse({'disable': not ProductData.objects.get(productName_id=data['productName'],
                                                                        stageName_id=data['stageName']).end})
        if data['placeName'] == 'qa':
            return JsonResponse({'disable': not ProductData.objects.get(productName_id=data['productName'],
                                                                        stageName_id=data['stageName']).qa})
        if data['placeName'] == 'rework':
            return JsonResponse({'disable': not ProductData.objects.get(productName_id=data['productName'],
                                                                        stageName_id=data['stageName']).rework})
    except ProductData.DoesNotExist:
        return JsonResponse({'disable': True})
    return JsonResponse({'disable': True})


def check_correct_product(data):
    q = ProcessData.objects.get(processNo__exact=data['processNo'])
    if int(data['barcode']) in range(int(q.startingSNo), int(q.endingSNo)):
        return True
    return False


def check_place(data):
    if data['placeName'] != "start" and not Barcode.objects.all().filter(barcode__exact=data['barcode'])\
            .filter(stageName_id__exact=data['stageName']).filter(placeName__exact="start").exists():
        return True
    return False


def check_multiple_scans(data):
    return Barcode.objects.all().filter(barcode__exact=data['barcode']).filter(stageName_id__exact=data['stageName'])\
        .filter(placeName__exact=data['placeName']).exists() and not data['override']


def check_previous_stages(data):
    process_id = ProductList.objects.get(productName__exact=data['productName']).processId
    index_val = 0
    arr = process_id.split('-')
    for i in range(0, len(arr)):
        if arr[i] == data['stageName']:
            index_val = i
    for i in range(0, index_val):
        try:
            last_stage = ProductData.objects.get(productName_id__exact=data['productName'], stageName_id=arr[i]).final
        except ProductData.DoesNotExist:
            last_stage = ""
        if not Barcode.objects.all().filter(barcode__exact=data['barcode']).filter(stageName_id__exact=arr[i])\
                .filter(productName_id__exact=data['productName']).filter(placeName__exact=last_stage).exists():
            return arr[i] + '-' + last_stage
    return 0
