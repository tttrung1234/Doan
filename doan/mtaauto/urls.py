from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='Homepage'),
    path('AutoFB', views.Getpost_tuyentruyen, name='autofb_tuyentruyen'),
    path('AutoFB', views.Dongtientrinh, name='dongtientrinh'),
    path('AutoFB', views.Getpost_phandong, name='autofb_phandong'),
    path('TrinhsatFB', views.TrinhsatFB, name='trinhsatfb'),
    path('contact/', views.getContact, name='contact'),
    path('contact/<int:id>', views.detailContact, name='detailContact'),
    path('saveContact/', views.saveContact, name='saveContact'),

]
