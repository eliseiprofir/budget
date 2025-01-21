from django import forms
from django.forms import EmailField
from allauth.account.forms import SignupForm, LoginForm
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model

User = get_user_model()

class UserAdminChangeForm(admin_forms.UserChangeForm):
    """
    Form for User modification in the Admin Area.
    """
    class Meta:
        model = User
        fields = ("email", "full_name", "is_active", "is_staff")
        field_classes = {"email": EmailField}


class UserAdminCreationForm(admin_forms.UserCreationForm):
    """
    Form for User Creation in the Admin Area.
    """

    class Meta:
        model = User
        fields = ("email",)
        field_classes = {"email": EmailField}
        error_message = {
            "email": {"unique": "This email has already been taken."}
        }


class UserSignupForm(SignupForm):
    """
    Form that will be rendered on a user sign up section/screen.
    Default fields will be added automatically.
    """

    full_name = forms.CharField(
        max_length=255,
        required=False,
        label="Full Name",
    )

    def save(self, request):
        user = super().save(request)
        if self.cleaned_data.get("full_name"):
            user.full_name = self.cleaned_data["full_name"]
            user.save()
        return user


class UserLoginForm(LoginForm):
    """
    Form that will be rendered on a user login up section/screen.
    Default fields will be added automatically.
    """

    error_message = {
        "account_inactive": "This account is currently inactive.",
        "email_password_mismatch": "The email or password you entered is incorrect."
    }

    def login(self, *args, **kwargs):
        ret = super().login(*args, **kwargs)
        self.user.update_last_login()
        return ret
