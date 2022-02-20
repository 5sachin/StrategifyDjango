from django.urls import path
from . import views


urlpatterns = [
    path('', views.home,name="home"),
    path('contactus/', views.contactus,name="contactus"),
    path('registration/', views.registration,name="registrationpage"),
    path('profilepage/', views.profilepage,name="profilepage"),
    path('deploypage/', views.deploypage,name="deploypage"),
    path('createstrategy/', views.createstrategy,name="createstrategy"),
    path('creatingStrategy',views.createStrategyForm,name="createsStrategyForm"),
    path('signup/', views.signup, name='signup'),
    path('checking/', views.checkUsername, name='checkUsername'),
    path('signin/', views.signIn, name='signIn'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('generateotp/',views.generateotp, name='generateotp'),
    path('checkstrategname',views.checkstrategyName,name="checkstrategyname"),
    path('topgainers',views.topgainers,name="topgainers"),
    path('toplosers',views.toplosers,name="toplosers"),
    path('indexdata',views.indexdata,name="indexdata"),
    path('openstrategy',views.openStrategy,name="openStrategy"),
]
