import json

from django.http import HttpResponse, JsonResponse
from django.utils import timezone

from session.models import UserData, UserLog


# Create your views here.


def check_user(username, password):
    for e in UserData.objects.all().filter(username__exact=username):
        if e.username == username and e.password == password:
            return True
    return False


def login(request):
    data = json.loads(request.body)
    if check_user(data['username'], data['password']):
        q = UserLog(username=UserData.objects.get(username__exact=data['username']), login_time=timezone.now())
        q.save()
        return JsonResponse(
            {"message": "success", "access": UserData.objects.get(username__exact=data['username']).superuser})
    else:
        return HttpResponse("login failed")


def logout(request):
    data = json.loads(request.body)
    q = UserLog(username=UserData.objects.get(username__exact=data['username']), logout_time=timezone.now())
    q.save()
    return HttpResponse('success')


def register(request):
    data = json.loads(request.body)
    q = UserData(username=data['username'], password=data['password'], firstname=data['firstname'],
                 lastname=data['lastname'], superuser=data['superuser'], employee_id=data['employeeId'])
    q.save()
    return HttpResponse('success')


def delete(request):
    data = json.loads(request.body)
    q = UserData.objects.get(username__exact=data['username'])
    q.delete()
    return HttpResponse('success')
