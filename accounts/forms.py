from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    # email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "password1", "password2")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizar mensagens de ajuda
        self.fields['username'].help_text = None # type: ignore
        self.fields['password1'].help_text = None # type: ignore
        self.fields['password2'].help_text = None # type: ignore

    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     if User.objects.filter(email=email).exists():
    #         raise forms.ValidationError("Este email já está em uso.")
    #     return email
    