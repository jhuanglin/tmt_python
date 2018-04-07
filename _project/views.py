import json
import pdb
import time
import datetime
from django.shortcuts import render
from django.http import JsonResponse
from _project.models import User, UserConfig, Label, List, Promo

# Create your views here.
# 注册接口
def register(request):
    ''' register '''
    if request.method == 'POST':
        # 需要对body解码之后通过json解析成dict
        data = json.loads(request.body.decode())
        username = data['username']
        password = data['password']
        if User.objects.filter(username=username):
            # 已存在该用户名
            err_code = '100'
            status = False
        else:
            # 创建新的用户
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
        # print(username)
        # print(password)
        # print(User.objects.filter(username=username))
        try:
            # 查询是否该用户名
            user = User.objects.get(username=username)
        except:
            pass
        if not user:
            # 用户不存在
            status = False
            err_code = '100'
        else:
            # 密码不一样
            if user.password != password:
                status = False
                err_code = '101'
            else:
                # 存取session
                request.session['user_id'] = user.id
                # pdb.set_trace()
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
        # 删除用户session
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
'''
def addConfig(request):
    ''' addConfig '''
    if request.method == 'POST':
        data = json.loads(request.body.decode())
        user_id = request.session['user_id']
        try:
            # config = UserConfig.objects.create(focus_mins=data['focus_mins'], relax_mins=data['relax_mins'], relax_long_mins=data['relax_long_mins'], relax_long_count=data['relax_long_count'], use_notification=data['use_notification'], auto_focus=data['auto_focus'], auto_relax=data['auto_relax'])
            # pdb.set_trace()
            config = UserConfig.objects.get(user_id=user_id)
            # config.focus_mins = data['focus_mins']
            # config.relax_mins = data['relax_mins']
            # config.relax_long_mins = data['relax_long_mins']
            # config.relax_long_count = data['relax_long_count']
            # config.use_notification = data['use_notification']
            # config.auto_focus = data['auto_focus']
            # config.auto_relax = data['auto_relax']
            for key in data:
                setattr(config, key, data[key])
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


# 查询个人配置
def config(request):
    ''' config '''
    if request.method == 'POST':
        user_id = request.session['user_id']
        # pdb.set_trace()
        try:
            # pdb.set_trace()
            config = UserConfig.objects.get(user_id=user_id)
        except:
            # pdb.set_trace()
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

# 获取所有标签的值
def getLabel(request):
    ''' label '''
    label = []
    try:
        # pdb.set_trace()
        labels = Label.objects.all().values()
        for item in labels:
            obj = {
                'value': item['id'],
                'label': item['name']
            }
            label.append(obj)
        status = True
        err_code = 1
    except:
        status = False
        err_code = 100
    response = {
        'status': status,
        'label': label,
        'err_code': err_code
    }
    return JsonResponse(response)

def getList(request):
    ''' getList '''
    if request.method == 'POST':
        user_id =request.session['user_id']
        today = datetime.date.today().strftime('%Y-%m-%d')
        lists = []
        try:
            # all_lists
            all_lists = List.objects.filter(user_id=user_id, complete=False)
            # today_lists
            order_lists = list(all_lists.filter(start_time=today))
            other_lists = list(all_lists.exclude(start_time=today).order_by('-start_time'))
            order_lists.extend(other_lists)
            labels = Label.objects.all()
            for item in order_lists:
                label_index_id = item.label_id - 1
                obj = {
                    'list_id': item.list_id,
                    'title': item.title,
                    'label': labels[label_index_id].name,
                    'start_time': item.start_time,
                    'summary': item.summary,
                    'complete': item.complete,
                    'tmt_counts': item.tmt_counts,
                    'complete_counts': item.complete_counts
                }
                lists.append(obj)
            status = True
            err_code = 1
        except Exception as e:
            print(e)
            status = False
            err_code = 100
        response = {
            "status": status,
            "list": lists,
            "err_code": err_code
        }
        return JsonResponse(response)

# 增加个人清单
def addList(request):
    ''' addlist '''
    if request.method == 'POST':
        list_info = json.loads(request.body.decode())
        user_id = request.session['user_id']
        try:
            new_list = List(user_id=user_id)
            for key in list_info:
                if key == 'label':
                    new_list.label_id = list_info[key]
                else :
                    setattr(new_list, key, list_info[key])
            new_list.save()
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

# 删除个人清单
'''
:param list_id
'''
def delList(request):
    ''' delList '''
    if request.method == 'POST':
        data = json.loads(request.body.decode())
        list_id = data['list_id']
        try:
            List.objects.filter(list_id=list_id).delete()
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

# 完成任务
def doneList(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode())
        summary = data['summary']
        list_id = data['list_id']
        # pdb.set_trace()
        try:
            done_list = List.objects.get(list_id=list_id)
            # 保存总结
            done_list.summary = summary
            # 修改完成标志
            done_list.complete = True
            # 记录完成时间
            done_list.done_time = datetime.datetime.now()
            done_list.save()
            status = True
            err_code = 1
        except Exception as e:
            print(e)
            status = False
            err_code = 100
        response = {
            'status': status,
            'err_code': err_code
        }
        return JsonResponse(response)


# 查询个人清单
def listSearchDate(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode())
        start_time = datetime.datetime.strptime(data['start_time'], '%Y-%m-%d')
        end_time = datetime.datetime.strptime(data['end_time'], '%Y-%m-%d')
        labels = Label.objects.all()
        lists = []
        try:
            filter_lists = List.objects.filter(start_time__range=(start_time, end_time)).order_by('-start_time')
            for item in filter_lists:
                label_index_id = item.label_id - 1
                obj = {
                    'list_id': item.list_id,
                    'title': item.title,
                    'label': labels[label_index_id].name,
                    'start_time': item.start_time,
                    'summary': item.summary,
                    'complete': item.complete,
                    'tmt_counts': item.tmt_counts,
                    'complete_counts': item.complete_counts
                }
                lists.append(obj)
            status = True
            err_code = 1
        except Exception as e:
            print(e)
            status = False
            err_code = 100
        response = {
            "status": status,
            'list': lists,
            "err_code": err_code
        }
        return JsonResponse(response)
