from django.urls import path
from django.contrib import admin
from . import views
urlpatterns=[
    path('',views.dashboard,name="base"),
    path('report/',views.generate_report,name="report"),
    path('report_details/<int:report_id>/',views.report_details,name="report_details"),
    path('make_payment/<int:member_id>/',views.make_payment,name="make_payment"),
    path('create_member/',views.create_member,name="create_member"),
    path('update_member/<int:pk>/', views.update_member, name="update_member"),
    path('delete_member/<int:pk>/', views.deleteOrder, name="delete_member"),
    path('signup',views.SignUp,name="signup"),
    path('signin', views.SignIn, name="signin"),
    path('signout', views.SignOut, name="signout"),
    path('activate/<uidb64>/<token>', views.activate, name="activate"),

]