from django.urls import path

from . import views

urlpatterns = [
    path('register/complete/', views.RegisterCompleteView.as_view(), name="register_complete"),
    path('register/', views.RegisterView.as_view(), name="register"),
]