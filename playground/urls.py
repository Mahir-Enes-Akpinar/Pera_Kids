from django.urls import path
from django.contrib.auth import views as auth_views
from . import views  # views.py dosyasındaki fonksiyonları çağırıyoruz

# Uygulama isimlendirmesi, URL'leri şablonlarda daha kolay kullanmamızı sağlar.
app_name = 'playground'

urlpatterns = [
    # Ana sayfa URL'si: '' (boş) olarak belirtilir.
    # Kullanıcı sitenin kök dizinine geldiğinde (örn: http://127.0.0.1:8000/)
    # views.py dosyasındaki 'anasayfa' fonksiyonu çalışacak.
    # name='anasayfa' ifadesi, bu URL'ye kod içinde referans vermemizi kolaylaştırır.
    path('', views.anasayfa, name='anasayfa'),

    # Bu URL yapısı, 'urun/' kelimesinden sonra gelen slug formatındaki metni yakalar
    # ve 'slug' adıyla 'urun_detay' view'ına gönderir.
    path('urun/<slug:slug>/', views.urun_detay, name='urun_detay'),

    
    

    path('sohbet-baslat/<int:product_id>/', views.sohbet_baslat, name='sohbet_baslat'),

    
    path('hesap/', views.hesap_view, name='hesap'),
]