from django.urls import path
from django.contrib.auth import views as auth_views
from .views import RegisterView, SubscriptionsView, subscribe, unfollow

app_name = 'account'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('subscriptions/', SubscriptionsView.as_view(), name='subscriptions'),
    path('unfollow/<int:user_id>/', unfollow, name='unfollow'),
    path('subscribe/', subscribe, name='subscribe'),
]
