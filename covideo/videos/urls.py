from django.urls import path

from . import views

urlpatterns = [
    path('new/', views.SubmitView.as_view(), name="submit"),
    path('mine/', views.PersonalVideosView.as_view(), name="personal"),
]