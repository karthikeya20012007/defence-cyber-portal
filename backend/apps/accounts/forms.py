from django import forms
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()


# =========================
# REGISTER FORM
# =========================

class RegisterForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "input-field",
                "placeholder": "Enter secure password"
            }
        )
    )

    class Meta:
        model = User
        fields = ["username", "email", "password"]

        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "input-field",
                    "placeholder": "Enter service ID"
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "input-field",
                    "placeholder": "Enter official email"
                }
            ),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


# =========================
# LOGIN FORM
# =========================

class LoginForm(forms.Form):

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "input-field",
                "placeholder": "Enter service ID"
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "input-field",
                "placeholder": "Enter password"
            }
        )
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Invalid credentials")
            cleaned_data["user"] = user

        return cleaned_data