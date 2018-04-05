import json
import pdb
from django.shortcuts import render
from django.http import JsonResponse
from _project.models import User
# Create your views here.
# 注册接口
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode())
        username = data['username']
        password = data['password']
        if User.objects.filter(username=username):
            err_code = '100'
            status = False
        else:
            User.objects.create(username=username, password=password)
            status = True
            err_code = 1
        response = {
            "status": status,
            "err_code": err_code
        }
        return JsonResponse(response)

# 登录接口
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode())
        username = data['username']
        password = data['password']
        user = {}
        print(username)
        print(password)
        print(User.objects.filter(username=username))
        try:
            user = User.objects.get(username=username)
        except:
            pass
        if not user:
            status = False
            err_code = '100'
        else:
            if user.password != password:
                status = False
                err_code = '101'
            else:
                request.session['user_id'] = user.id
                pdb.set_trace()
                status = True
                err_code = 1
        response = {
            "status": status,
            "err_code": err_code
        }
        return JsonResponse(response)

def logout(request):
    try:
        del request.session['user_id']
    except:
        pass
    response = {
        'status': True,
        'err_code': 1
    }
    return JsonResponse(response)