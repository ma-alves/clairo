from django.forms import ModelForm
from django import forms
from .models import ChatMessage


class MessageForm(ModelForm):
    class Meta:
        model: ChatMessage
        fields = ['body']
        widgets = {
            'body': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Digite sua mensagem...'
            }),
        }