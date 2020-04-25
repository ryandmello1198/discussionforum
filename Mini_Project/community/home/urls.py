from django.urls import path
from django.conf.urls import url
from home import views
from django.contrib.auth.views import login,logout
app_name= 'home'
urlpatterns= [
    path('login/',login,{'template_name': 'home/login.html'}),
    path('about/',views.about,name='About'),
    path('register/',views.register,name='register'),
    path('logout/',logout,{'template_name': 'home/homepage.html'}),
    path('',views.list_of_questions,name='testpage'),
    path('ask/', views.ask_question,name='ask_question'),
    path('profile/',views.view_profile, name='view_profile'),
    path('profile/edit/',views.edit_profile, name='edit_profile'),
    path('profile/edit/change-password/',views.change_password, name='change_password'),
    path('profile/password/',views.redirect_password, name='redirect_password'),
    path('<slug:slug>/',views.view_question,name='view_question'),
    path('<slug:slug>/answer/',views.add_answer,name='add_answer')
]
