from django.contrib import admin
from .models import User, UserConfig, Label, List, Promo
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    ''' Useradmin '''
    list_display = ('username', 'password')

class UserConfigAdmin(admin.ModelAdmin):
    ''' UserConfigAdmin '''
    list_display = ('user_id', 'focus_mins', 'relax_mins')

class LabelAdmin(admin.ModelAdmin):
    ''' LabelAdmin '''
    list_display = ('name')

class ListAdmin(admin.ModelAdmin):
    '''ListAdmin'''
    list_display = ('title', 'label_id', 'tmt_counts', 'complete_counts', 'create_time', 'done_time', 'status', 'summary')

class PromoAdmin(admin.ModelAdmin):
    ''' PromoAdmin '''
    readonly_fields = ('start_date', 'end_date')

admin.site.register(User, UserAdmin)