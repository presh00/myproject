from django.urls import path
from . import views


urlpatterns=[
    path('',views.home, name= 'home'),
    path('rooms/<str:pk>/',views.rooms, name= 'rooms'),
    path('create-room/',views.createRoom,name='create-room'),
    path('update-room/<str:pk>/',views.updateRoom,name='update-room'),
    path('delete-room/<str:pk>/',views.deleteRoom,name='delete-room'),
    path('delete-message/<str:pk>/',views.deleteMessage,name='delete-message'),
    
    
    path('log-in/',views.loginPage,name= 'login'),
    path('log-out/',views.logoutUser,name= 'logout'),
    path('register/',views.registerPage,name= 'register'),
    path('user-profile/<str:pk>/',views.userProfile,name='user-profile'),
    path('edit-user/', views.updateUser, name= 'update-user'),
    path('topic-pag/',views.topicPage,name='topics'),
]