from django.urls import path

from . import views

urlpatterns = [
    path('new/', views.SubmitView.as_view(extra_context={"tab": "submit"}), name="submit"),
    path('mine/', views.PersonalVideosView.as_view(), name="personal"),
    path('', views.BrowseView.as_view(extra_context={"tab": "browse"}), name="browse"),
]