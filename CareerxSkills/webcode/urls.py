from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="webcode"),
    path('dashboard/',views.dashboard,name="webcode"),
    path('auth/',views.auth,name='webcode'),
    path('ai/',views.aiadvisor,name='webcode'),
    path('roadmap/',views.roadmap,name='webcode'),
    path('profile/',views.profile,name='webcode'),
    path('dev/',views.dev,name='webcode')
]
