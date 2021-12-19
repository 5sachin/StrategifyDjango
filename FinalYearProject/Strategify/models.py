from django.db import models
from django.contrib import admin


class UserRegistration(models.Model):
	username = models.CharField(max_length=100)
	name = models.CharField(max_length=100)
	email = models.CharField(max_length=15)
	phone = models.CharField(max_length=200)
	password = models.CharField(max_length=100)


class UserRegistrationAdmin(admin.ModelAdmin):
    list_display = ('username', 'name','email','phone','password')

admin.site.register(UserRegistration,UserRegistrationAdmin)