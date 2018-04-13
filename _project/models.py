from django.db import models

# Create your models here.
# 用户表
class User(models.Model):
    """ User model """
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username
    __repr__ = __str__

class UserFirstIn(models.Model):
    ''' UserFirstIn '''
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    is_first_in = models.BooleanField(default=True)

    def __str__(self):
        return '用户 %s 第一次进来 %s' % (self.user_id, self.first_in)
    __repr__ = __str__

# 用户配置表
class UserConfig(models.Model):
    """ UserConfig model """
    focus_mins = models.IntegerField(default=25)
    relax_mins = models.IntegerField(default=5)
    relax_long_mins = models.IntegerField(default=20)
    relax_long_count = models.IntegerField(default=4)
    use_notification = models.BooleanField(default=True)
    auto_focus = models.BooleanField(default=False)
    auto_relax = models.BooleanField(default=False)

    user = models.ForeignKey('User', on_delete=models.CASCADE)

    def __str__(self):
        return '个人配置 - 专注时间: %s, 休息时间: %s, 是否通知: %s, 自动专注: %s, 自动休息: %s.' % (self.focus_mins, self.relax_mins, self.use_notification, self.auto_focus, self.auto_relax)

    __repr__ = __str__


# 标签表
class Label(models.Model):
    """ Label model """
    name = models.CharField(max_length=30)

    def __str__(self):
        return 'name: %s' % (self.name)
    __repr__ = __str__

# 任务清单表
class List(models.Model):
    """ List model """
    # id
    list_id = models.AutoField(primary_key=True)
    # 名称
    title = models.CharField(max_length=200)
    # 完成标志
    complete = models.BooleanField(default=False)
    # 预计番茄完成数量
    tmt_counts = models.IntegerField(default=1)
    # 实际番茄完成数量
    complete_counts = models.IntegerField(default=0)
    # 创立时间
    create_time = models.DateTimeField(auto_now_add=True)
    # 完成时间
    done_time = models.DateTimeField(null=True)
    # 预计开始时间
    start_time = models.DateField(null=True)
    # 预计结束时间
    end_time = models.DateField(null=True)
    # 第一次开始时间
    start_date = models.DateTimeField(null=True)
    # 最后一次结束时间
    end_date = models.DateTimeField(null=True)
    # 状态
    # status = models.CharField(max_length=30)
    # status = models.ForeignKey('Status', on_delete=models.CASCADE, null=True)
    # 总结
    summary = models.TextField(null=True)
    # 标签
    label = models.ForeignKey('Label', on_delete=models.CASCADE)
    # 用户
    user = models.ForeignKey('User', on_delete=models.CASCADE)

    def __str__(self):
        return '名称: %s, 预计开始时间: %s' % (self.title, self.start_time)
    __repr__ = __str__

# 番茄表
class Promo(models.Model):
    """ Promo model """
    # 开始时间 
    start_date = models.DateTimeField()
    # 结束时间
    end_date = models.DateTimeField(auto_now_add=True)
    # 总共时长
    pro_mins = models.IntegerField(default=0)
    # promo_id
    promo = models.ForeignKey('List', on_delete=models.CASCADE)
    # label_id
    label = models.ForeignKey('Label', on_delete=models.CASCADE)
    # user_id
    user = models.ForeignKey('User', on_delete=models.CASCADE) 

    def __str__(self):
        return '开始时间： %s， 结束时间： %s' % (self.start_date, self.end_date)
    __repr__ = __str__

# 当前完成分钟
class Count(models.Model):
    ''' Count '''
    today_date = models.DateField(auto_now_add=True)
    count_mins = models.IntegerField(default=0)
    count_promos = models.IntegerField(default=0)
    # user_id 
    user = models.ForeignKey('User', on_delete=models.CASCADE) 

    def __str__(self):
        return '日期： %s 完成分钟数 %s 完成番茄数 %s' % (self.today_date, self.count_mins, self.count_promos)
    __repr__ = __str__

class UserIn(models.Model):
    ''' UserIn '''
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    today_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return '%s 是否第一次进: %s' % (self.today_date, self.first_in)
    __repr__ = __str__