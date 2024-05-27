from django.shortcuts import render
from .models import Account, AccountType, Advice, Transaction, Budget, Category
from datetime import date, timedelta
from django.http import JsonResponse

# Create your views here.


def handle_home_page(request):
    accounts = Account.objects.filter(account_type=AccountType.PERSONAL)
    current_balance = 0
    for account in accounts:
        current_balance += account.balance
    advices = Advice.objects.all()
    first_day_of_current_month = date.today().replace(day=1)
    last_day_of_last_month = first_day_of_current_month - timedelta(days=1)
    last_month = last_day_of_last_month.replace(day=1)

    context = {
        'accounts': accounts,
        'current_balance': current_balance,
        'advices': advices,
        'today': date.today,
        'last_month': last_month
        }

    return render(request, 'home.html', context)


def handle_login_page(request):
    return render(request, "login.html")


def handle_transaction_page(request):
    transactions = Transaction.objects.all()
    advices = Advice.objects.all()
    first_day_of_current_month = date.today().replace(day=1)
    last_day_of_last_month = first_day_of_current_month - timedelta(days=1)
    last_month = last_day_of_last_month.replace(day=1)

    context = {
        'transactions': transactions,
        'advices': advices,
        'today': date.today,
        'last_month': last_month
        }
    return render(request, "transaction.html", context)


def handle_budget_page(request):
    budgets = Budget.objects.all()
    advices = Advice.objects.all()
    first_day_of_current_month = date.today().replace(day=1)
    last_day_of_last_month = first_day_of_current_month - timedelta(days=1)
    last_month = last_day_of_last_month.replace(day=1)

    context = {
        'budgets': budgets,
        'advices': advices,
        'today': date.today,
        'last_month': last_month
        }
    return render(request, "budget.html", context)


def handle_account_page(request):
    accounts = Account.objects.all()
    advices = Advice.objects.all()
    first_day_of_current_month = date.today().replace(day=1)
    last_day_of_last_month = first_day_of_current_month - timedelta(days=1)
    last_month = last_day_of_last_month.replace(day=1)

    context = {
        'accounts': accounts,
        'advices': advices,
        'today': date.today,
        'last_month': last_month
        }
    return render(request, "account.html", context)


def handle_category_page(request):
    categorys = Category.objects.all()
    advices = Advice.objects.all()
    first_day_of_current_month = date.today().replace(day=1)
    last_day_of_last_month = first_day_of_current_month - timedelta(days=1)
    last_month = last_day_of_last_month.replace(day=1)

    context = {
        'categorys': categorys,
        'advices': advices,
        'today': date.today,
        'last_month': last_month
        }
    return render(request, "category.html", context)


def handle_report_page(request):
    return render(request, "report.html")


def get_balance_data(request):
    accounts = Account.objects.filter(account_type=AccountType.PERSONAL)
    datas = {}
    first = True
    for account in accounts:
        data_points = account.get_data_points()
        if first:
            for i in data_points:
                datas[i[0]] = i[1]
            first = False
        else:
            for i in data_points:
                datas[i[0]] = datas[i[0]] + i[1]
        labels, data = list(datas.keys()), list(datas.values())
    return JsonResponse({'labels': labels, 'data': data})
