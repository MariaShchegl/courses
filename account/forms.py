from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from .models import User

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Введите логин'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Введите пароль'}))

    class Meta:
        model = User
        fields = ('username','password')

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class':'form-control'})

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введите имя'}), required=False)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введите фамилию'}), required=False)
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введите логин'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введите e-mail'}), required=False)
    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введите телефон'}), required=False)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Введите пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Повторите пароль'}))
    isRule = forms.BooleanField(widget=forms.CheckboxInput, required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'phone', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class':'form-control'})

class ChangePasswordForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Повторите пароль'}))

    class Meta:
        model = User
        fields = ('password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class':'form-control'})

class UserProfileForm(UserChangeForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'readonly': True}), required=False)
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введите e-mail'}), required=False)
    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введите телефон'}), required=False)
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введите имя'}), required=False)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введите фамилию'}), required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone')

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class':'form-control'})