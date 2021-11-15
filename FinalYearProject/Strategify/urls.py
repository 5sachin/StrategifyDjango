from django.urls import path, include
from . import views

urlpatterns = [


path('', views.home,name="home"),
path('contactus/', views.contactus,name="contactus"),
path('registration/', views.registration,name="registrationpage"),
path('profilepage/', views.profilepage,name="profilepage"),
path('createstrategy/', views.createstrategy,name="createstrategy"),
path('creatingStrategy',views.createStrategyForm,name="createsStrategyForm")
]
