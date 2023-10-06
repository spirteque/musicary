from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm, UsernameField, SetPasswordForm, PasswordResetForm, PasswordChangeForm
from django.forms.widgets import ClearableFileInput
from django.utils.translation import gettext_lazy as _
from django import forms
from django.forms.utils import ErrorList
from .models import Profile

ErrorList.template_name = "main/errors.html"

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Nazwa użytkownika lub e-mail',
               'id': 'username_input'
        }
    ))
    
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Hasło',
            'id': 'password_input'
        }
    ))


class UserRegistrationForm(forms.ModelForm):            
    username = UsernameField(
        error_messages={'unique': 'Podana nazwa użytkownika już istnieje.'},
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Nazwa użytkownika',
                   'id': 'username_input',}))
    
    email = forms.EmailField(
        error_messages={'invalid': 'Podany adres e-mail jest nieprawidłowy.'},
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                    'placeholder': 'Adres e-mail',
                    'id': 'email_input'}))
    
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs = {'class': 'form-control',
                     'placeholder': 'Hasło',
                     'id': 'password_input'}))
    
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Powtórz hasło',
                   'id': 'password_input2'}))
    
    statute_accept = forms.BooleanField(
        error_messages={'required': 'Aby utworzyć konto musisz zaakceptować Regulamin serwisu.'},
        widget=forms.CheckboxInput(
            attrs={'id': 'statute_input'}))
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'statute_accept')
 
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Hasła nie są identyczne.')
        return cd['password2']
    
    
class UserSetNewPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(UserSetNewPasswordForm, self).__init__(*args, **kwargs)
    
    error_messages = {
        "password_mismatch": _("Nowe hasło nie jest identyczne w obu polach."),
    }
    
    new_password1 = forms.CharField(
        required=True,
        label=_("New password"),
        widget=forms.PasswordInput(attrs = {
            'class': 'form-control',
            'placeholder': 'Nowe hasło',
            'id': 'new_password_input',
            'autocomplete': 'new-password',}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
        )
    
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Powtórz nowe hasło',
            'id': 'new_password2_input',
            "autocomplete": "new-password"}),
    )
    

class UserPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordResetForm, self).__init__(*args, **kwargs)
    
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={
            "autocomplete": "email",
            'class': 'form-control',
            'placeholder': 'Adres e-mail',
            'id': 'email_input'}),
    )


class UserPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordChangeForm, self).__init__(*args, **kwargs)
        
    error_messages = {
        **UserSetNewPasswordForm.error_messages,
        "password_incorrect": _(
            "Twoje stare hasło jest niepoprawne. Wprowadź go ponownie"
        ),
    }
    
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',
                   'id': 'old_password_input',
                   "autocomplete": "current-password",}))
    
    new_password1 = forms.CharField(
        required=True,
        label=_("New password"),
        widget=forms.PasswordInput(attrs = {
            'class': 'form-control',
            'id': 'new_password_input',
            'autocomplete': 'new-password',}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
        )
    
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'new_password2_input',
            "autocomplete": "new-password"}),
    )

class UserEditForm(forms.ModelForm):
    username = UsernameField(
        error_messages={'unique': 'Podana nazwa użytkownika już istnieje.'},
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Nazwa użytkownika',
                   'id': 'username_input',}))
    
    email = forms.EmailField(
        error_messages={'invalid': 'Podany adres e-mail jest nieprawidłowy.'},
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                    'placeholder': 'Adres e-mail',
                    'id': 'email_input'}))
    
    class Meta:
        model = User
        fields = ('username', 'email')
        

class ProfileEditForm(forms.ModelForm):
    photo = forms.ImageField(
        error_messages={'invalid_image': _('Prześlij poprawny obraz, np. w formacie .png, .jpeg.')})
        
    ClearableFileInput.template_name = "main/clearable_file_input.html"
    
    class Meta:
        model = Profile
        fields = ('photo',)


class DeleteAccountForm(forms.Form):
    confirmation = forms.BooleanField()
    

class ProfilePrivacyEditForm(forms.ModelForm):
    private_mode = forms.BooleanField(label="Tryb prywatny",
                                      required=False)
    
    class Meta:
        model = Profile
        fields = ('private_mode',)
        

