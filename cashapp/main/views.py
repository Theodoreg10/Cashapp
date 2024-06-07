from .models import Account, AccountType, Advice, Transaction, Budget, Category
from datetime import date, timedelta
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import (AccountCreateForm,
                    TransactionCreateForm, LoginForm, RegistrationForm)
import random
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import logging
# Create your views here.
# from django.contrib.auth.decorators import login_required
logger = logging.getLogger(__name__)


def template(context={}):
    advices = list(Advice.objects.all())
    random.shuffle(advices)
    context['advices'] = advices[:5]
    return context


def handle_home_page(request):
    first_day_of_current_month = date.today().replace(day=1)
    last_day_of_last_month = first_day_of_current_month - timedelta(days=1)
    last_month = last_day_of_last_month.replace(day=1)
    accounts = Account.objects.filter(account_type=AccountType.PERSONAL)
    current_balance = 0
    current_month_expense = 0
    current_month_income = 0
    for account in accounts:
        current_balance += account.balance
        current_month_expense += account.expense(last_day_of_last_month)
        current_month_income += account.income(last_day_of_last_month)
    advices = Advice.objects.all()
    transactions = Transaction.objects.order_by('date')[:5]
    movement = current_month_income - current_month_expense
    context = {
        'accounts': accounts,
        'current_balance': current_balance,
        'advices': advices,
        'today': date.today,
        'last_month': last_month,
        'recent_transactions': transactions,
        'movement': movement,
        'current_month_income': current_month_income,
        'current_month_expense': current_month_expense,
        }

    return render(request, 'home.html', template(context=context))


def handle_login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect("home")
            else:
                error_message = "Invalid login credentials"
                messages.error(request, 'Invalid login credentials')
    else:
        form = LoginForm()
        error_message = None
    context = {"form": form, "error_message": error_message}
    return render(request, "login.html", template(context))


def handle_logout_view(request):
    logout(request)
    return redirect("login")


def handle_register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            password = form.cleaned_data["password"]
            email = form.cleaned_data["email"]

            if User.objects.filter(username=name).exists():
                messages.error(request, 'Username already exists')
                return redirect('register')  # or your view name
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
                return redirect('register')  # or your view name
            else:
                # Create a new user
                user = User.objects.create_user(
                    username=name, password=password, email=email
                )

                # Log in the new user
                user = authenticate(request, username=name, password=password)
                login(request, user)

                return redirect("home")

    else:
        form = RegistrationForm()

    return render(request, "register.html", template({"form": form}))


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
    return render(request, "transaction.html", template(context=context))


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
    return render(request, "budget.html", template(context=context))


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
    return render(request, "account.html", template(context=context))


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
    return render(request, "category.html", template(context=context))


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


@login_required
def create_account(request):
    if request.method == 'POST':
        form = AccountCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('account')
    else:
        form = AccountCreateForm()
    context = {'form': form, 'title': 'Create Account'}
    return render(request, 'add_account.html', template(context=context))


@login_required
def update_account(request, pk):
    account = get_object_or_404(Account, pk=pk)
    if account.account_type == AccountType.SYSTEM:
        return HttpResponseForbidden(
            "You are not allowed to edit this account")

    if request.method == 'POST':
        form = AccountCreateForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            return redirect('account')
    else:
        form = AccountCreateForm(instance=account)
    context = {'form': form,
               'title': 'Update Account',
               'update': True, 'account': account}
    return render(request, 'add_account.html', template(context=context))


@login_required
def delete_account(request, pk):
    account = get_object_or_404(Account, pk=pk)
    if account.account_type == AccountType.SYSTEM:
        return HttpResponseForbidden(
            "You are not allowed to delete this account")

    if request.method == 'POST':
        account.delete()
        return redirect('account')  # Assuming you have an account list view
    context = {'account': account}
    return render(request, 'account_confirm_delete.html',
                  template(context=context))


@login_required
def create_transaction(request):
    if request.method == 'POST':
        form = TransactionCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transaction')
    else:
        form = TransactionCreateForm()
    context = {'form': form, 'title': 'Create Transaction'}
    return render(request, 'add_transaction.html', template(context=context))


@login_required
def update_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        form = TransactionCreateForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('transaction')
    else:
        form = TransactionCreateForm(instance=transaction)
    context = {'form': form,
               'title': 'Update transaction',
               'update': True, 'transaction': transaction}
    return render(request, 'add_transaction.html', template(context=context))


@login_required
def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        transaction.delete()
        return redirect('transaction')
    context = {'transaction': transaction}
    return render(request, 'account_confirm_delete.html',
                  template(context=context))
