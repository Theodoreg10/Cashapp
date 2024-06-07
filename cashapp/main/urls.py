from django.urls import path
from . import views

urlpatterns = [
    path("", views.handle_home_page, name="home"),
    path("home", views.handle_home_page, name="home"),
    path("transaction", views.handle_transaction_page, name="transaction"),
    path("budget", views.handle_budget_page, name="budget"),
    path("account", views.handle_account_page, name="account"),
    path("category", views.handle_category_page, name="category"),
    path("report", views.handle_report_page, name="report"),
    path('api_balance', views.get_balance_data, name='api_balance'),
    path('account_new', views.create_account, name='account_new'),
    path('account/<int:pk>/edit/',
         views.update_account, name='account_update'),
    path('transaction_new', views.create_transaction, name='transaction_new'),
    path('transaction/<int:pk>/edit/',
         views.update_transaction, name='transaction_update'),
    path("login", views.handle_login_page, name="login"),
    path("logout", views.handle_logout_view, name="logout"),
    path("register", views.handle_register_page, name="register"),
    ]
