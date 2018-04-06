import json
import pdb
from django.shortcuts import render
from django.http import JsonResponse
from _project.models import User, UserConfig, Label, List, Promo
# Create your views here.
# 注册接口
def register(request):
    ''' register '''
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
    ''' login '''
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

# 退出登陆
def logout(request):
    ''' logout '''
    try:
        del request.session['user_id']
    except:
        pass
    response = {
        'status': True,
        'err_code': 1
    }
    return JsonResponse(response)

# 增加配置
'''
configInfo: {
    // 专注时间
    focus_mins: 25,
    // 休息时间
    relax_mins: 5,
    // 长时间休息
    relax_long_mins: 20,
    // 长时间间隔
    relax_long_count: 4,
    // 允许系统通知
    use_notification: true,
    // 自动专注
    auto_focus: false,
    // 自动休息
    auto_relax: false
}
'''
def addconfig(request):
    ''' addconfig '''
    if request.method == 'POST':
        data = json.loads(request.body.decode())
        try:
            # config = UserConfig.objects.create(focus_mins=data['focus_mins'], relax_mins=data['relax_mins'], relax_long_mins=data['relax_long_mins'], relax_long_count=data['relax_long_count'], use_notification=data['use_notification'], auto_focus=data['auto_focus'], auto_relax=data['auto_relax'])
            pdb.set_trace()
            config = UserConfig(focus_mins=data['focus_mins'])
            config.relax_mins = data['relax_mins']
            config.relax_long_mins = data['relax_long_mins']
            config.relax_long_count = data['relax_long_count']
            config.use_notification = data['use_notification']
            config.auto_focus = data['auto_focus']
            config.relax_mins = data['relax_mins']
            config.auto_relax = data['auto_relax']
            config.save()
            status = True
            err_code = 1
        except:
            status = False
            err_code = 100
        response = {
            'status': status,
            'err_code': err_code
        }
        return JsonResponse(response)


def config(request):
    ''' config '''
    if request.method == 'POST':
        user_id = request.session['user_id']
        pdb.set_trace()
        try:
            pdb.set_trace()
            config = UserConfig.objects.get(user_id=user_id)
        except:
            pdb.set_trace()
            config  = UserConfig.objects.create(user_id=user_id)
        status = True
        err_code = 1
        data = {
            'focus_mins': config.focus_mins,
            'relax_mins': config.relax_mins,
            'relax_long_mins': config.relax_long_mins,
            'relax_long_count': config.relax_long_count,
            'use_notification': config.use_notification,
            'auto_focus': config.auto_focus,
            'auto_relax': config.auto_relax
        }
        response = {
            "status": status,
            "data": data,
            "err_code": err_code
        }
        return JsonResponse(response)