from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='Homepage'),
    path('AutoFB', views.Getpost_tuyentruyen, name='autofb_tuyentruyen'),
    path('AutoFB', views.test, name='test'),
    path('AutoFB', views.Getpost_phandong, name='autofb_phandong'),
    path('TrinhsatFB', views.TrinhsatFB, name='trinhsatfb'),

]
