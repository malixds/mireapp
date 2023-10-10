from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('forworker/<int:pk>/', views.for_worker, name='for-worker'),
    path('formworker/', views.editProfile, name='form-worker'),
    path('tasks/', views.tasks, name='tasks'),
    # path('filter-tasks/', views.filterTasks, name='filter-tasks'),
    path('freetasks/', views.freeTask, name='free-tasks'),
    path('search/', views.search, name='search'),
    path('signin/', views.signinPage, name='signin'),
    path('signup/', views.signupPage, name='signup'),
    path('u/<str:username>/', views.otherProfile, name='otherprofile'),
    path('mytasks/', views.myTasks, name='mytasks'),
    path('logout/', views.logoutUser, name='logout'),
    path('profile/', views.currentProfile, name='currentprofile'),
    path('settings/', views.settings, name='settings'),
    path('fulltask/<int:pk>', views.fullTask, name='fulltask'),
    path('myjobs', views.myJobs, name='myjobs'),
    path('deljobs/<int:pk>/delete', views.deleteTask, name='deljobs'),
    path('myorder/<int:pk>', views.myOrder, name='myorder'),
    path('success/', views.success, name='success'),
    path('taskaccept/<int:pk>/accept', views.taskAccept, name='taskaccept'),
    path('taskcancel/<int:pk>/cancel', views.taskCancel, name='taskcancel'),
    path('rate/<int:pk>', views.rate, name='rate'),
]
