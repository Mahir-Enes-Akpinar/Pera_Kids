# playground/forms.py

from django.contrib.auth.forms import UserCreationForm
from django import forms

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Alanların etiketlerini (label) kaldırıyoruz çünkü onları HTML'de kendimiz yazacağız.
        self.fields['username'].label = ""
        self.fields['password1'].label = ""
        self.fields['password2'].label = ""
        
        # Placeholder'ları boşluk karakteriyle güncelliyoruz.
        self.fields['username'].widget.attrs.update({
            'placeholder': ' ' 
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': ' '
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': ' '
        })