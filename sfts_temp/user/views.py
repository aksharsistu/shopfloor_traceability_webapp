import json
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from user.models import UserData


def login(request):
    data = json.loads(request.body)
    try:
        q = UserData.objects.get(username__exact=data['username'])
        if data['password'] == q.password:
            return JsonResponse({'username': q.username, 'superuser': q.superuser, 'message': ''})
        else:
            return JsonResponse({'username': '', 'superuser': '', 'message': 'Check credentials'})
    except UserData.DoesNotExist:
        return HttpResponseBadRequest('User does not exist')


def register(request):
    data = json.loads(request.body)
    q = UserData(username=data['username'], password=data['password'], firstName=data['firstName'],
                 lastName=data['lastName'], employeeId=data['employeeId'], superuser=data['superuser'])
    q.save()
    return HttpResponse('Success')


def delete(request):
    try:
        q = UserData.objects.get(username__exact=request.body)
        q.delete()
        return HttpResponse('Success')
    except UserData.DoesNotExist:
        return HttpResponseBadRequest('User does not exist')
