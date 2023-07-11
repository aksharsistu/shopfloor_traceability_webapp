import json
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from product.models import ProductList, ProductData


def setProduct(request):
    # Delete any previous such entry:
    deleteProduct(request)

    data = json.loads(request.body)
    q = ProductList(productName=data['productName'], processId='-'.join(data['processId']))
    q.save()
    for i in range(0, len(data['processId'])):
        q = ProductData(productName_id=data['productName'], stageName_id=data['processId'][i], start=data['start'][i],
                        end=data['end'][i], qa=data['qa'][i], rework=data['rework'][i], final=data['final'][i])
        q.save()
    return HttpResponse('Success')


def getProducts(request):
    try:
        productList = []
        for e in ProductList.objects.all():
            productList.append({'productName': e.productName, 'processId': e.processId})
        return JsonResponse(productList, safe=False)
    except ProductList.DoesNotExist:
        return HttpResponseBadRequest('No products found')


def deleteProduct(request):
    try:
        q = ProductList.objects.get(productName__exact=request.body.decode('unicode-escape'))
        q.delete()
        return HttpResponse('Success')
    except ProductList.DoesNotExist:
        return HttpResponseBadRequest('Server error occurred')
