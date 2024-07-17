from django.urls import path
from . import views

urlpatterns = [
    path("signup", views.signup, name="signup"),
    path("signin", views.signin, name="signin"),
    path("signout", views.signout, name="signout"),
    path("user/profile/<str:username>/", views.profile, name="profile"),
    path("update-profile", views.update_profile, name="update-profile"),
    path("user/follow/<str:username>/", views.follow, name='follow'),
    path("user/unfollow/<str:username>/", views.unfollow, name='unfollow'),
    path("users/", views.user_list, name='user_list')
]