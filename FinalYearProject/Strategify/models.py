from django.db import models
from django.contrib import admin


class UserRegistration(models.Model):
    username = models.CharField(max_length=100, primary_key=True, blank=False)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)
    phone = models.CharField(max_length=200)
    password = models.CharField(max_length=100)


class UserRegistrationAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'email', 'phone', 'password')


class StrategyRegistration(models.Model):
    strategyid = models.CharField(max_length=100, primary_key=True, blank=False)
    username = models.ForeignKey(UserRegistration, max_length=100, blank=False, on_delete=models.CASCADE)
    strategyname = models.CharField(max_length=100)
    quantity = models.CharField(max_length=100)
    scripname = models.CharField(max_length=100)
    entrycondition = models.CharField(max_length=100)
    stoploss = models.CharField(max_length=100)
    target = models.CharField(max_length=100)
    exitcondition = models.CharField(max_length=100)
    startdate = models.CharField(max_length=100)
    enddate = models.CharField(max_length=100)
    createDate = models.CharField(max_length=50)


class StrategyRegistrationAdmin(admin.ModelAdmin):
    list_display = (
    'strategyid', 'username', 'strategyname', 'quantity', 'scripname', 'entrycondition', 'stoploss', 'target',
    'exitcondition', 'startdate', 'enddate', 'createDate')


class Deploy(models.Model):
    deployid = models.CharField(max_length=100, primary_key=True, blank=False)
    strategyid= models.ForeignKey(StrategyRegistration, max_length=100, blank=False, on_delete=models.CASCADE)
    username = models.ForeignKey(UserRegistration, max_length=100, blank=False, on_delete=models.CASCADE)
    scripname = models.CharField(max_length=100)
    deploytime = models.CharField(max_length=100)
    algocycles = models.CharField(max_length=100)

class DeployAdmin(admin.ModelAdmin):
    list_display = ('deployid','strategyid','username','scripname','deploytime','algocycles')


admin.site.register(UserRegistration, UserRegistrationAdmin)
admin.site.register(StrategyRegistration, StrategyRegistrationAdmin)
admin.site.register(Deploy, DeployAdmin)
