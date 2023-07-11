import json
import random
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from process.models import ProcessData, Quantity
from product.models import ProductList


def setProcess(request):
    data = json.loads(request.body)
    q = ProcessData(processNo=data['processNo'], productName_id=data['productName'], startingSNo=str(data['startingSNo']),
                    endingSNo=str(data['endingSNo']), maxQuantity=data['maxQuantity'], currentQuantity=0)
    q.save()
    for r in ProductList.objects.get(productName=data['productName']).processId.split('-'):
        e = Quantity(processNo_id=data['processNo'], productName_id=data['productName'],
                     stageName_id=r, quantity=0)
        e.save()
    return HttpResponse('Success')


def getProcess(request):
    try:
        processList = []
        for e in ProcessData.objects.all():
            processList.append({'processNo': e.processNo, 'productName': e.productName.productName,
                                'startingSNo': e.startingSNo, 'maxQuantity': e.maxQuantity,
                                'currentQuantity': e.currentQuantity})
        return JsonResponse(processList, safe=False)
    except ProcessData.DoesNotExist:
        return HttpResponseBadRequest('No processes found')


def deleteProcess(request):
    try:
        q = ProcessData.objects.get(processNo__exact=request.body.decode('unicode-escape'))
        q.delete()
        return HttpResponse('Success')
    except ProcessData.DoesNotExist:
        return HttpResponseBadRequest('Server error occurred')


def generateNumbers(request):
    startingSNo = (10**6)*random.randint(10**5, 10**6-1)
    if ProcessData.objects.all().filter(startingSNo__exact=startingSNo).exists():
        return generateNumbers(request)
    try:
        currentProcessNos = []
        for e in ProcessData.objects.all():
            currentProcessNos.append(e.processNo)
        processNo = max(currentProcessNos) + 1
    except ProcessData.DoesNotExist:
        processNo = 10000
    except ValueError:
        processNo = 10000
    return JsonResponse({'startingSNo': (10**6)*random.randint(10**6, 10**7-1), 'processNo': processNo})


def getStageQuantity(request):
    data = json.loads(request.body)
    try:
        q = Quantity.objects.get(processNo_id__exact=data['processNo'], productName_id__exact=data['productName'],
                                 stageName_id__exact=data['stageName'])
        return HttpResponse(q.quantity)
    except Quantity.DoesNotExist:
        return HttpResponseBadRequest('No product found')
