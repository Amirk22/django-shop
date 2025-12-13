from django import forms
from django.core import validators
from django.core.validators import MinValueValidator

class RegisterForm(forms.Form):
    email = forms.EmailField(
        label='ایمیل',
        max_length=100,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'ایمیل خود را وارد کنید'
        }),
        validators=[
            validators.EmailValidator(),
            validators.MaxLengthValidator(100)
        ]
    )

    password = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'رمز عبور خود را وارد کنید'
        })
    )

    confirm_password = forms.CharField(
        label='تکرار رمز عبور',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'رمز عبور را دوباره وارد کنید'
        })
    )


    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password == confirm_password :
            return confirm_password
        raise forms.ValidationError('کلمه عبور و تکرار کلمه عبور مغایرت دارند')

class RegisterActiveCodeForm(forms.Form):
    code = forms.CharField(
        max_length=5,
        label="کد فعال‌سازی",
        validators=[
            validators.MaxLengthValidator(5),
            validators.MinLengthValidator(5)
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'کد ۵ رقمی را وارد کنید',
            'inputmode': 'numeric',
        })
    )

class LoginForm(forms.Form):
    email = forms.EmailField(
        label='ایمیل',
        max_length=100,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'ایمیل خود را وارد کنید'
        }),
        validators=[
            validators.EmailValidator(),
            validators.MaxLengthValidator(100)
        ]
    )
    password = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'رمز عبور خود را وارد کنید'
        })
    )

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        label='ایمیل',
        max_length=100,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'ایمیل خود را وارد کنید'
        }),
        validators=[
            validators.EmailValidator(),
            validators.MaxLengthValidator(100)
        ]
    )

class ForgotPasswordCodeForm(forms.Form):
    code = forms.CharField(
        max_length=5,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'کد ۵ رقمی را وارد کنید'
        })
    )

class ChangePasswordForm(forms.Form):
    password = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'رمز عبور جدید'
        })
    )
    confirm_password = forms.CharField(
        label='تکرار رمز عبور',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'رمز عبور را دوباره وارد کنید'
        })
    )

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password == confirm_password:
            return confirm_password
        raise forms.ValidationError('کلمه عبور و تکرار کلمه عبور مغایرت دارند')