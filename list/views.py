import json

from django.http import HttpResponse, JsonResponse

from list.models import Products, Processes
from stage.models import Quantity


# Create your views here


def set_process(request):
    data = json.loads(request.body)
    # Delete any previous processes with similar name:
    delete_process(request)

    q = Processes(process=data['processName'], pid=data['processId'])
    q.save()
    return HttpResponse('success')


def delete_process(request):
    data = json.loads(request.body)
    e = Processes.objects.get(process__exact=data['processName'])
    e.delete()
    return HttpResponse('success')


def get_process(request):
    processes = []
    for e in Processes.objects.all():
        processes.append({"processName": str(e.process), "processId": str(e.pid)})
    return JsonResponse(processes, safe=False)


def set_product(request):
    data = json.loads(request.body)
    # Delete any previous product of similar name:
    delete_product(request)

    q = Products(product_name=data['productName'], process_id=data['processName'],
                 product_code=data['productCode'], fg_code=data['fgCode'])
    q.save()
    for stage in Processes.objects.get(process=data['processName']).pid.split('-'):
        e = Quantity(product_name_id=data['productName'], line_code_id=stage, max_quantity=data['maxQuantity'], current_quantity=0, start_sno=data['startSno'], end_sno=data['endSno'])
        e.save()

    return HttpResponse('success')


def delete_product(request):
    data = json.loads(request.body)
    e = Products.objects.get(product_name__exact=data['productName'])
    e.delete()
    return HttpResponse('success')


def get_product(request):
    products = []
    for e in Products.objects.all():
        try:
            pid = Processes.objects.get(process__exact=str(e.process.process)).pid
            data = {"productName": str(e.product_name), "processName": str(e.process.process), "processId": str(pid),
                    "fgCode": str(e.fg_code), "productCode": str(e.product_code)}
        except Processes.DoesNotExist:
            data = {"productName": "Error", "processName": "Error", "processId": "Error", "fgCode": "Error", "productCode": "Error"}

        products.append(data)
    return JsonResponse(products, safe=False)
