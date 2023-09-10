from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm
from django import forms


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
    username = UsernameField(required=True,
                             widget=forms.TextInput(
                                attrs={'class': 'form-control',
                                       'placeholder': 'Nazwa użytkownika',
                                       'id': 'username_input',
                                }
                            ))
    
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(
                                attrs={'class': 'form-control',
                                    'placeholder': 'Adres e-mail',
                                    'id': 'email_input',
                                }
                        ))
    
    password = forms.CharField(required=True, 
                               widget=forms.PasswordInput(
                                   attrs = {
                                        'class': 'form-control',
                                        'placeholder': 'Hasło',
                                        'id': 'password_input'
                                   }
                               ))
    
    
    password2 = forms.CharField(required=True,
                                widget=forms.PasswordInput(
                                    attrs={
                                        'class': 'form-control',
                                        'placeholder': 'Powtórz hasło',
                                        'id': 'password_input2'
                                    }
                                ))
    
    statute_accept = forms.BooleanField(required=True,
                                        error_messages={'required': 'Aby utworzyć konto musisz zaakceptować Regulamin serwisu.'},
                                        widget=forms.CheckboxInput(
                                            attrs={
                                                'id': 'statute_input'
                                            }
                                        ))
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'statute_accept')
 
    def clean_password2(self):
        cd = self.cleaned_data
        print(cd)
        print(cd['password'], cd['password2'])
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Hasła nie są identyczne.')
        return cd['password2']
