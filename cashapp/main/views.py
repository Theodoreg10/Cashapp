from django.shortcuts import render

# Create your views here.


def handle_home_page(request):
    return render(request, "home.html")


def handle_login_page(request):
    return render(request, "login.html")


def handle_transaction_page(request):
    return render(request, "transaction.html")


def handle_budget_page(request):
    return render(request, "budget.html")


def handle_account_page(request):
    return render(request, "account.html")


def handle_category_page(request):
    return render(request, "category.html")


def handle_report_page(request):
    return render(request, "report.html")