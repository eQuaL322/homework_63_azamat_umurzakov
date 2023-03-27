from django.urls import path

from accounts.views import LoginView, logout_view, RegisterView, UserChangeView, SearchAccountListView, \
    AccountDetailView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout', logout_view, name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/<int:pk>/change', UserChangeView.as_view(), name='change'),
    path('accounts/search', SearchAccountListView.as_view(), name='account_search'),
    path('<str:username>/', AccountDetailView.as_view(), name='account_detail'),
]
