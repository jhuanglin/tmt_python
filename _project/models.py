from django.db import models

# Create your models here.
# 用户表
class User(models.Model):
    """ User model """
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username

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

# 状态表
class Status(models.Model):
    """ Status model """
    status = models.CharField(max_length=30)

    def __str__(self):
        return 'status: %s' % (self.status)

# 任务清单表
class List(models.Model):
    """ List model """
    # 名称
    title = models.CharField(max_length=200)
    # 完成标志
    comlete = models.BooleanField(default=False)
    # 预计番茄完成数量
    tmt_counts = models.IntegerField(default=1)
    # 实际番茄完成数量
    complete_counts = models.IntegerField()
    # 创立时间
    create_time = models.DateTimeField(auto_now_add=True)
    # 完成时间
    done_time = models.DateTimeField()
    # 预计开始时间
    start_time = models.DateField()
    # 预计结束时间
    end_time = models.DateField()
    # 状态
    # status = models.CharField(max_length=30)
    status = models.ForeignKey('Status', on_delete=models.CASCADE)
    # 总结
    summary = models.TextField()
    # 标签
    label = models.ForeignKey('Label', on_delete=models.CASCADE)
    # 用户
    user = models.ForeignKey('User', on_delete=models.CASCADE)


# 番茄表
class Promo(models.Model):
    """ Promo model """
    # 开始时间 
    start_date = models.DateTimeField()
    # 结束时间
    end_date = models.DateTimeField(auto_now_add=True)
    # promo_id
    promo = models.ForeignKey('List', on_delete=models.CASCADE)