from django import forms
from .models import Account, AccountType, Transaction


class LoginForm(forms.Form):
    """
    Form for user login.

    Fields:
    - username (CharField): User's username.
    - password (CharField): User's password (masked).

    """
    username = forms.CharField(label="Username")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")


class RegistrationForm(forms.Form):
    """
    Form for user registration.

    Fields:
    - name (CharField): User's name.
    - password (CharField): User's password (masked).
    - email (EmailField): User's email address.

    """
    name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()


class AccountCreateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name',
                  'account_type',
                  'active',
                  'show_on_dashboard',
                  'iban']
        widgets = {
            'account_type': forms.Select(choices=AccountType.choices),
        }


class TransactionCreateForm(forms.ModelForm):
    src = forms.ModelChoiceField(queryset=Account.objects.all(),
                                 label="Source Account")
    dst = forms.ModelChoiceField(queryset=Account.objects.all(),
                                 label="Destination Account")

    class Meta:
        model = Transaction
        fields = ['title', 'date', 'notes', 'transaction_type', 'src',
                  'dst', 'amount', 'category', 'recurrence']
