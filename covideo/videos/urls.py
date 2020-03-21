from django.urls import path

from . import views

urlpatterns = [
    path('new/', views.SubmitView.as_view(extra_context={"tab": "submit", "title": "Submit"}), name="submit"),
    path('mine/', views.PersonalVideosView.as_view(extra_context={"title": "Your Videos"}), name="personal"),
    path('', views.BrowseView.as_view(extra_context={"tab": "browse"}), name="browse"),
]