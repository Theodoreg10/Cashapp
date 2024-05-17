from django.urls import path
from . import views

urlpatterns = [
    path("", views.handle_home_page, name="home"),
    path("home", views.handle_home_page, name="home"),
    path("login", views.handle_login_page, name="login"),
    path("logout", views.handle_login_page, name="logout"),
    path("register", views.handle_login_page, name="register"),
    path("transaction", views.handle_transaction_page, name="transaction"),
    path("budget", views.handle_budget_page, name="budget"),
    path("account", views.handle_account_page, name="account"),
    path("category", views.handle_category_page, name="category"),
    path("report", views.handle_report_page, name="report"),
    ]
