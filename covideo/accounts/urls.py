from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.RegisterCompleteView.as_view(extra_context={"title": "Welcome"}), name="register_complete"),
    path('login/', views.LoginView.as_view(extra_context={"title": "Log In or Sign Up"}), name="login"),
    path('email/unsubscribe/', views.UnsubscribeEmailView.as_view(), name="email_unsubscribe"),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('redirect/', views.AuthenticatedRedirectView.as_view(), name="redirect")
]