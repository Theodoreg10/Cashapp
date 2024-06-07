from django.db import models
# from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from datetime import date, timedelta
from django.urls import reverse


# Create your models here.
class AccountType(models.IntegerChoices):
    """model for the account type

    Args:
        models (_type_): _description_
    """
    PERSONAL = 1, _('Personal')
    FOREIGN = 2, _('Foreign')
    SYSTEM = 3, _('System')
# Transaction


class TransactionQuerySet(models.QuerySet):
    def last_10(self):
        return self.order_by('-date')[:10]

    def date_range(self, dstart, dend):
        return self.filter(date__gte=dstart, date__lte=dend)


class Transaction(models.Model):
    DEPOSIT = 1
    WITHDRAW = 2
    TRANSFER = 3
    SYSTEM = 4
    TRANSACTION_TYPES = (
        (DEPOSIT, 'Deposit'),
        (WITHDRAW, 'Withdrawal'),
        (TRANSFER, 'Transfer'),
        (SYSTEM, 'Reconcile'),
    )

    class Meta:
        ordering = ['-date', 'title']

    title = models.CharField(max_length=64)
    date = models.DateField(default=date.today)
    notes = models.TextField(blank=True, null=True)
    transaction_type = models.IntegerField(choices=TRANSACTION_TYPES)
    src = models.ForeignKey('Account', models.CASCADE, 'debits')
    dst = models.ForeignKey('Account', models.CASCADE, 'credits')
    amount = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    category = models.ForeignKey('Category', models.CASCADE, 'transactions')
    last_modified = models.DateTimeField(auto_now=True)
    recurrence = models.BooleanField(default=False)

    objects = TransactionQuerySet.as_manager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('transaction_detail', args=[self.pk])

    def get_transaction_type_str(self):
        for i, name in self.TRANSACTION_TYPES:
            if i == self.transaction_type:
                return name

    @property
    def is_recurrence(self):
        return self.recurrence

    @property
    def is_system(self):
        return self.transaction_type == self.SYSTEM

    @property
    def is_transfer(self):
        return self.transaction_type == self.TRANSFER

    @property
    def is_withdraw(self):
        return self.transaction_type == self.WITHDRAW

    @property
    def is_deposit(self):
        return self.transaction_type == self.DEPOSIT


# model for account


class AccountQuerySet(models.QuerySet):
    def personal(self):
        return self.filter(account_type=AccountType.PERSONAL)

    def foreign(self):
        return self.filter(account_type=AccountType.FOREIGN)

    def active(self):
        return self.filter(active=True)

    def inactive(self):
        return self.filter(active=False)

    def shown_on_dashboard(self):
        return self.filter(show_on_dashboard=True)


class Account(models.Model):

    name = models.CharField(max_length=64)
    account_type = models.IntegerField(choices=AccountType.choices,
                                       default=AccountType.PERSONAL)
    active = models.BooleanField(default=True)
    last_modified = models.DateTimeField(auto_now=True)
    show_on_dashboard = models.BooleanField(default=False)
    iban = models.CharField(max_length=34, blank=True, null=True)
    import_ibans = models.TextField(default='[]')
    import_names = models.TextField(default='[]')

    objects = AccountQuerySet.as_manager()

    class Meta:
        ordering = ['-active', 'name']
        unique_together = (('name', 'account_type'),)

    def __str__(self):
        return self.name

    @property
    def account_type_str(self):
        return AccountType.labels[self.account_type - 1]

    @property
    def is_personal(self):
        return self.account_type == AccountType.PERSONAL

    @property
    def transaction_num(self):
        """
        TODO do we really want the number of splits?
        """
        return Transaction.objects.filter(src=self).count()

    @property
    def balance(self):
        return self.balance_on(date.today())

    def income(self, dstart, dend=date.today()):
        return self.income_on(dend) - self.income_on(dstart)

    def expense(self, dstart, dend=date.today()):
        return self.expense_on(dend) - self.expense_on(dstart)

    def balance_on(self, date):
        return round(
            Transaction.objects.filter(dst=self, date__lte=date).aggregate(
                models.Sum('amount')
            )['amount__sum'] or 0, 2
        ) - round(
            Transaction.objects.filter(src=self, date__lte=date).aggregate(
                models.Sum('amount')
            )['amount__sum'] or 0, 2
        )

    def income_on(self, date):
        return round(
            Transaction.objects.filter(dst=self, date__lte=date).aggregate(
                models.Sum('amount')
            )['amount__sum'] or 0, 2
        )

    def expense_on(self, date):
        return round(
            Transaction.objects.filter(src=self, date__lte=date).aggregate(
                models.Sum('amount')
            )['amount__sum'] or 0, 2
        )

    def get_absolute_url(self):
        return reverse('account_view', args=[self.pk])

    def get_data_points(self, dstart=date.today() - timedelta(days=365),
                        dend=date.today(), steps=30):
        data_points = []
        labels = []
        step_size = (dend - dstart) / steps
        current_date = dstart
        while current_date <= dend:
            labels.append(current_date)
            balance = self.balance_on(current_date)
            data_points.append((current_date, balance))
            current_date += step_size
        return data_points

    def set_initial_balance(self, amount):
        system = Account.objects.get(account_type=AccountType.SYSTEM)
        Transaction.objects.create(
            title=_('Initial Balance'),
            transaction_type=Transaction.SYSTEM,
            src=system,
            dst=self,
            amount=amount
        )


# category model
class Category(models.Model):
    name = models.CharField(max_length=64)
    active = models.BooleanField(default=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def money_spent(self):
        return abs(Transaction.objects.filter(
            transaction_type=Transaction.WITHDRAW,
            category=self).aggregate(
            models.Sum('amount'))['amount__sum'] or 0)

    @property
    def money_spent_this_month(self):
        today = date.today()
        first_day_of_month = today.replace(day=1)
        return abs(Transaction.objects.filter(
            transaction_type=Transaction.WITHDRAW,
            category=self,
            date__gte=first_day_of_month,
            date__lte=today).aggregate(
            models.Sum('amount'))['amount__sum'] or 0)

    def get_absolute_url(self):
        return reverse('category_detail', args=[self.id])


class BudgetQuerySet(models.QuerySet):
    def for_month(self, month):
        return self.filter(month=month)


class Budget(models.Model):
    category = models.ForeignKey(Category, models.CASCADE)
    month = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    last_modified = models.DateTimeField(auto_now=True)

    objects = BudgetQuerySet.as_manager()

    class Meta:
        ordering = ['category']

    def __str__(self):
        return self.category.name

    @property
    def spent(self):
        return abs(Transaction.objects.filter(
            transaction_type=Transaction.WITHDRAW,
            category=self.category,
            date__month=self.month.month,
            date__year=self.month.year).aggregate(
            models.Sum('amount'))['amount__sum'] or 0)

    @property
    def remaining(self):
        return self.amount - self.spent

    @property
    def percent_spent(self):
        return round(self.spent / self.amount * 100, 2)

    def get_absolute_url(self):
        return reverse('budget_detail', args=[self.id])


class Advice(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField()
    text = models.TextField()

    def __str__(self):
        return self.title
