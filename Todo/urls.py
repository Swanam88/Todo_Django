"""
URL configuration for Todo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from my_app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',IndexView.as_view(),name="index"),
    path('signup/',UserRegistrationView.as_view(),name="signup"),
    path('login/',LoginView.as_view(), name="login"),     # as_view to show it as function based
    path('logout/',LogoutView.as_view(),name="logout"),
    path('todo/create/', TaskView.as_view(), name ="create"),
    path('todo/read/',TaskReadView.as_view(), name="task_read"),
    path('todo/update/<int:pk>',TaskUpdateView.as_view(),name="update"),
    path('todo/delete/<int:pk>', TaskDeleteView.as_view(),name="delete"),
    path('todo/detail/<int:pk>',TaskDetailView.as_view(),name="detail"),
    path('todo/edit/<int:pk>',TaskEditView.as_view(),name="edit"),
    path('todo/forgotpwd/',ForgotPasswordView.as_view(),name="forgot"),
    path('todo/otpverify/',OtpVerifyView.as_view(),name="otpverify"),
    path('todo/resetpwd/',ResetPasswordView.as_view(),name="resetpwd"),
    path('todo/filter/',TaskFilterView.as_view(),name="filter"),
    path('todo/addtask/',TaskView.as_view(),name="addtask")
]
