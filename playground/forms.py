# playground/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Message
from django.db import transaction

class CustomUserCreationForm(UserCreationForm):
    # User modelindeki standart alanları forma ekliyoruz
    first_name = forms.CharField(max_length=30, required=True, label="Ad")
    last_name = forms.CharField(max_length=150, required=True, label="Soyad")
    email = forms.EmailField(max_length=254, required=True, label="E-posta Adresi")

    # UserProfile modelindeki özel alanları forma ekliyoruz
    company_name = forms.CharField(max_length=200, required=False, label="Firma Adı")
    phone_number = forms.CharField(max_length=20, required=False, label="Telefon Numarası")
    street = forms.CharField(max_length=255, required=False, label="Sokak ve Numara")
    city = forms.CharField(max_length=100, required=False, label="Şehir / İl")
    state = forms.CharField(max_length=100, required=False, label="İlçe")
    postal_code = forms.CharField(max_length=10, required=False, label="Posta Kodu")

    class Meta(UserCreationForm.Meta):
        model = User
        # forma dahil edilecek standart alanlar
        fields = ("username", "email", "first_name", "last_name")

    @transaction.atomic
    def save(self, commit=True):
        # Önce User nesnesini normal şekilde oluşturuyoruz
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        
        if commit:
            user.save()
            # Şimdi de UserProfile nesnesini gelen form verileriyle güncelliyoruz.
            profile = user.profile
            profile.company_name = self.cleaned_data.get('company_name')
            profile.phone_number = self.cleaned_data.get('phone_number')
            profile.street = self.cleaned_data.get('street')
            profile.city = self.cleaned_data.get('city')
            profile.state = self.cleaned_data.get('state')
            profile.postal_code = self.cleaned_data.get('postal_code')
            profile.save()
            
        return user

# Mesaj gönderme formu (henüz kullanmıyoruz ama burada kalabilir)
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'placeholder': 'Mesajınızı buraya yazın...',
                'class': 'message-input',
                'rows': 3,
            })
        }
        labels = { 'text': '' }