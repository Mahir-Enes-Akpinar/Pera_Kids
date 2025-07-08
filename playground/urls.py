from django.urls import path
from . import views  # views.py dosyasındaki fonksiyonları çağırıyoruz

# Uygulama isimlendirmesi, URL'leri şablonlarda daha kolay kullanmamızı sağlar.
app_name = 'playground'

urlpatterns = [
    # Ana sayfa URL'si: '' (boş) olarak belirtilir.
    # Kullanıcı sitenin kök dizinine geldiğinde (örn: http://127.0.0.1:8000/)
    # views.py dosyasındaki 'anasayfa' fonksiyonu çalışacak.
    # name='anasayfa' ifadesi, bu URL'ye kod içinde referans vermemizi kolaylaştırır.
    path('', views.anasayfa, name='anasayfa'),
]