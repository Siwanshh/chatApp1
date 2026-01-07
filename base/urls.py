from django.urls import path
from . import views
urlpatterns=[
    path('',views.home,name="home"),
    path('start/<str:sttr>/',views.start,name="start"),
    path('create/',views.formrqst,name="create"),
    path('submit/',views.submit,name="submit"),
    path('update/<int:pk>/',views.updateRoom,name="update"),
    path('delete/<int:pk>/',views.deleteRoom,name="delete"),
    path('login',views.loginPage,name='login'),
    path('logout',views.logoutsection,name='logout'),
    path('register/',views.regPage,name="register"),
    path('comment/',views.commentAdd,name="comment"),
    path('delete/<str:pk>',views.deleteMessage,name='delmsg'),
    path('userprofile/<str:pk>',views.userProfile,name='user-profile')

]