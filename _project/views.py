import json
import pdb
import time
import datetime
from django.shortcuts import render
from django.http import JsonResponse
from _project.models import User, UserConfig, Label, List, Promo, Count



def getDate(obj):
    return datetime.datetime.strftime(obj['create_time'], '%Y-%m-%d')
# Create your views here.
# 注册接口
'''
register
@param username 用户名
@param password 用户密码
'''
def register(request):
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
'''
login
@param username 用户名
@param password 用户密码
'''
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode())
        username = data['username']
        password = data['password']
        user = {}
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
'''
logout
@param user_id 用户id
'''
def logout(request):
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

# 密码查询
'''
confirmPass
@param password 加密后密码
'''
def confirmPass(request):
    old_password = json.loads(request.body.decode())['password']
    user_id = request.session['user_id']
    try:
        user = User.objects.get(user_id=user_id)
        if user.password == old_password:
            status = True
            err_code = 1
        else:
            status = False
            err_code = 1
    except Exception as e:
        print(e)
        status = False
        err_code = 100
    response = {
        "status": status,
        "err_code": err_code
    }
    return JsonResponse(response)

# 修改密码
'''
updatePass
@param password 加密后密码
'''
def updatePass(request):
    new_password = json.loads(request.body.decode())['newpass']
    user_id = request.session['user_id']
    try:
        user = User.objects.get(user_id=user_id)
        user.password = new_password
        user.save()
        status = True
        err_code = 1
    except Exception as e:
        status = False
        err_code = 100
    response = {
        "status": status,
        "err_code": err_code
    }

# 增加配置
'''
addConfig
@param focus_mins 专注时间
@param relax_mins 休息时间
@param relax_long_mins 长时间休息
@param relax_long_count 长时间间隔
@param use_notification 允许系统通知
@param auto_focus 自动专注
@param auto_relax 自动休息
'''
def addConfig(request):
    ''' addConfig '''
    if request.method == 'POST':
        data = json.loads(request.body.decode())
        user_id = request.session['user_id']
        try:
            # 更新用户配置
            config = UserConfig.objects.get(user_id=user_id)
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
'''
config
@param focus_mins 专注时间
@param relax_mins 休息时间
@param relax_long_mins 长时间休息
@param relax_long_count 长时间间隔
@param use_notification 允许系统通知
@param auto_focus 自动专注
@param auto_relax 自动休息
'''
def config(request):
    ''' config '''
    if request.method == 'POST':
        user_id = request.session['user_id']
        # pdb.set_trace()
        # 如果查不到用户的配置数据，则新建一个
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
'''
getlabel
@param id label_id
@param name label_name
'''
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

'''
getList
@param user_id 用户id
@param lists 用户的任务清单
    @param list_id list_id
    @param title 名称
    @param label label_id
    @param start_time 预计开始时间
    @param summary 总结
    @param complete 完成标志
    @param tmt_counts 预计完成番茄数
    @param complete_counts 实际完成番茄数
'''
def getList(request):
    ''' getList '''
    if request.method == 'POST':
        user_id =request.session['user_id']
        today = datetime.date.today().strftime('%Y-%m-%d')
        lists = []
        haveTodayList = False
        try:
            # all_lists
            all_lists = List.objects.filter(user_id=user_id, complete=False)
            # today_lists 获取今天的数据
            order_lists = list(all_lists.filter(start_time=today))
            if len(order_lists) != 0:
                haveTodayList = True
            # 获取其他的数据
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
            "have_todaylists": haveTodayList,
            "err_code": err_code
        }
        return JsonResponse(response)

# 增加个人清单
'''
addlist
@param user_id 用户id
'''
def addList(request):
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
'''
doneList
@param summary 总结
@param list_id list_id
@param complete 完成标志
@param done_time 完成时间 
'''
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
'''
listSearchDate
@param start_time 查询开始时间
@param end_time 查询结束时间
@prama label_id label_id
'''
def listSearchDate(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode())
        start_time = datetime.datetime.strptime(data['start_time'], '%Y-%m-%d')
        end_time = datetime.datetime.strptime(data['end_time'], '%Y-%m-%d')
        user_id = request.session['user_id']
        labels = Label.objects.all()
        lists = []
        try:
            filter_lists = List.objects.filter(user_id=user_id, start_time__range=(start_time, end_time)).order_by('-start_time')
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

'''
@param start_date 开始时间
@param end_date 结束时间 --建立的时候自动创建
@param promo promo_id
@param label label_id
@param user_id user_id
'''
# 增加番茄
def addPromo(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode())
        promo_id = data['list_id']
        user_id =request.session['user_id']
        start_date = data['start_date']
        label = data['label']
        today_date = datetime.datetime.now().date()
        try:
            # 获取label_id
            label_id = Label.objects.get(name=label).id
            # 创建新的番茄
            new_promo = Promo(user_id=user_id, promo_id=promo_id)
            # 存取开始时间
            new_promo.start_date = datetime.datetime.fromtimestamp(start_date / 1000)
            new_promo.label_id = label_id
            new_promo.save()
            up_list = List.objects.get(user_id=user_id, list_id=list_id)
            up_list.complete_counts = up_list.complete_counts + 1
            up_list.save()
            status = True
            err_code = 1
        except Exception as e:
            print(e)
            status = False
            err_code = 100
        # 添加统计
        try:
            new_count = Count.objects.filter(today_date=today_date, user_id=user_id)
            if len(new_count) == 0:
                new_count = Count(user_id=user_id)
            else:
                new_count = new_count[0]
            new_count.count_promos = new_count.count_promos + 1
            new_count.save()
        except Exception as e:
            print(e)
        response = {
            "status": status,
            "err_code": err_code 
        }
        return JsonResponse(response)

# 获取统计分钟数
'''
getCountMins
@param count_mins 完成分钟
'''
def getCountMins(request):
    if request.method == 'GET':
        user_id = request.session['user_id']
        today_date = datetime.datetime.now().date()
        count_mins = 0
        try:
            new_count = Count.objects.filter(today_date=today_date, user_id=user_id)
            if len(new_count) == 0:
                new_count = Count.objects.create(user_id=user_id)
            else:
                new_count = new_count[0]
            count_mins = new_count.count_mins
            status = True
            err_code = 1
        except Exception as e:
            status = False
            err_code = 100
        response = {
            "status": status,
            "count_mins": count_mins,
            "err_code": err_code
        }


# 添加统计分钟数
'''
addCountMins
'''
def addCountMins(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode())
        count_mins = data['countMins']
        user_id = request.session['user_id']
        today_date = datetime.datetime.now().today()
        try:
            up_count = Count.objects.get(user_id=user_id, today_date=today_date)
            up_count.count_mins = count_mins
            status = True
            err_code = 1
        except Exception as e:
            print(e)
            status = False
            err_code = 100
        response = {
            "status": status,
            "err_code": err_code
        }
        return JsonResponse(response)

# 查询番茄数据
'''
getPromo
@param user_id user_id
@param start_date 开始时间 '%Y-%m-%d'
@param end_date 结束时间 '%Y-%m-%d'
'''
def getPromo(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode())
        user_id = request.session['user_id']
        start_date = data['start_date']
        end_date = data['end_date']
        labels = Label.objects.all()
        dataList = []
        try:
            if start_date != '':
                start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
                end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
                search_promo = Promo.objects.filter(user_id=user_id, start_date__range(start_date, end_date).order_by('-start_date')
            else:
                search_promo = Promo.objects.filter(user_id=user_id).order_by('-start_date')
            dates = list(set(map(getDate, search_promo.values('start_date'))))
            for date in dates:
                obj = {}
                promoList = []
                obj['date'] = date
                fdate = datetime.datetime.strptime(date, '%Y-%m-%d')
                insert_promo = search_promo.filter(start_date=fdate)
                for item in insert_promo:
                    promo_id = item.promo_id
                    s_date = item.start_date.strftime('%H:%M:%S')
                    e_date = item.end_date.strftime('%H:%M:%S')
                    insert_list = List.objects.get(list_id=promo_id)
                    title = insert_list.title
                    label = labels[promo_id-1].name
                    summary = insert_list.summary
                    pobj = {
                        "list_id": promo_id,
                        "title": title,
                        "label": label,
                        "start_date": s_date,
                        "end_date": e_date,
                        "summary": summary
                    }
                    promoList.append(pobj)
                obj['promoList'] = promoList
                dataList.append(obj)
            status = True
            err_code = 1
        except Exception as e:
            print(e)
            status = False
            err_code = 100
        response = {
            "status": status,
            "data": dataList,
            "err_code": err_code
        }


# 删除番茄数据
'''
delPromo
@param user_id user_id
@param list_id list_id
@param day 今天日期
@param start_date 开始时间 %H:%M:%S
@param end_date 结束时间 %H:%M:%S
'''
def delPromo(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode())
        user_id = request.session['user_id']
        list_id = data['list_id']
        day = data['day']
        start_date = datetime.datetime.strptime(day + ' ' + data['start_date'], '%Y-%m-%d %H:%M:%S')
        end_date = datetime.datetime.strptime(day + ' ' + data['end_date'], '%Y-%m-%d %H:%M:%S')
        day_date = datetime.datetime.strptime(day, '%Y-%m-%d')
        try:
            Promo.objects.filter(user_id=user_id, promo_id=list_id, start_date=start_date, end_date=end_date).delete()
            old_count = Count.objects.get(user_id=user_id, today_date=day_date)
            old_count.count_promos = old_count.count_promos - 1
            old_count.count_mins = old_count.count_mins - round((end_date - start_date).total_seconds() / 60)
            old_count.save()
            status = True
            err_code = 1
        except Exception as e:
            print(e)
            status = False
            err_code = 100
        response = {
            "status": status,
            "err_code": err_code
        }
        return JsonResponse(response)

# 查询完成清单数据
'''
getCompleteList
@param user_id user_id
'''
def getCompleteList(request):
    if request.method == 'POST':
    user_id =request.session['user_id']
    lists = []
    try:
        # all_lists
        all_lists = List.objects.filter(user_id=user_id, complete=True).order_by('-done_time')
        labels = Label.objects.all()
        for item in all_lists:
            list_id = item.list_id
            label_index_id = item.label_id - 1
            promoLists = Promo.objects.get(promo_id=list_id, user_id=user_id)
            # 获取第一次开始时间
            start_time = promoLists.order_by('start_date')[0].start_date
            # 获取最后一次结束时间
            end_time = promoLists.order_by('-end_date')[0].end_date
            obj = {
                'list_id': list_id,
                'title': item.title,
                'label': labels[label_index_id].name,
                'start_time': start_time.strftime('%Y-%m-%d'),
                'end_time': end_time.strftime('%Y-%m-%d'),
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
        "data": lists,
        "err_code": err_code
    }
    return JsonResponse(response)

# 修改完成清单数据
'''
updateCompleteList
@param user_id user_id
@param list_id list_id
@param summary 总结
'''
def updateCompleteList(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode())
        user_id = request.session['user_id']
        list_id = data['list_id']
        try:
            up_list = List.objects.get(user_id=user_id, list_id=list_id)
            up_list.summary = data['summary']
            up_list.save()
            status = True
            err_code = 1
        except Exception as e:
            print(e)
            status = False
            err_code = 100
        response = {
            "status": status,
            "err_code": err_code
        }
        return JsonResponse(response)


# 删除完成清单数据
'''
delCompleteList
@param list_id list_id
'''
def delCompleteList(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode())
        user_id = request.session['user_id']
        list_id = data['list_id']
        try:
            up_list = List.objects.get(user_id=user_id, list_id=list_id)
            up_list.complete = False
            up_list.save()
            status = True
            err_code = 1
        except Exception as e:
            print(e)
            status = False
            err_code = 100
        response = {
            "status": status,
            "err_code": err_code 
        }
        return JsonResponse(response)

# 获取初始统计数据
'''
getCountData
'''
def getCountData(request):
    pass

# 获取不同日期下的番茄数
'''
getLineChart
@param start_date 开始时间
@param end_date 结束时间
'''
def getLineChart(request):
    pass

# 获取标签分类
'''
getPieChart
'''
def getPieChart(request):
    pass

# 获取最佳工作时间最佳工作日
'''
getBarChart
'''
def getBarChart(request):
    pass

