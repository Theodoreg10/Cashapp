from django.shortcuts import render
from .models import Account, AccountType

# Create your views here.


def handle_home_page(request):
    accounts = Account.objects.filter(account_type=AccountType.PERSONAL)
    current_balance = 0
    for account in accounts:
        current_balance += account.balance
    context = {
        'accounts': accounts,
        'current_balance': current_balance
        }

    return render(request, 'home.html', context)


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
