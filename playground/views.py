from django.shortcuts import render, get_object_or_404
from .models import Product  # Veritabanından Product modelimizi çağırıyoruz

# Create your views here.

def anasayfa(request):
    """
    Bu fonksiyon, ana sayfa isteği geldiğinde çalışır.
    Veritabanındaki tüm mevcut ürünleri alır ve anasayfa.html şablonuna gönderir.
    """
    # Sadece stokta olan (is_available=True) ürünleri alıyoruz
    # ve en yeniden eskiye doğru sıralıyoruz.
    urunler = Product.objects.filter(is_available=True).order_by('-created_at')

    # 'urunler' verisini bir "context" sözlüğü içinde şablona gönderiyoruz.
    # Şablon içinde bu verilere 'urunler_listesi' anahtar kelimesiyle erişeceğiz.
    context = {
        'urunler_listesi': urunler
    }

    # render fonksiyonu, isteği, şablon dosyasını ve verileri birleştirerek
    # kullanıcıya tam bir HTML sayfası olarak gönderir.
    return render(request, 'playground/anasayfa.html', context)


def urun_detay(request, slug):
    """
    Tek bir ürünün detay sayfasını gösterir.
    URL'den gelen 'slug' bilgisini kullanarak ilgili ürünü bulur.
    """
    # get_object_or_404: Belirtilen modelde (Product) ve kriterde (slug=slug)
    # bir nesne bulmaya çalışır. Eğer bulamazsa, otomatik olarak "404 Sayfa Bulunamadı"
    # hatası gösterir. Bu, try-except blokları yazmaktan çok daha pratiktir.
    urun = get_object_or_404(Product, slug=slug, is_available=True)

    context = {
        'urun_detay_verisi': urun
    }

    # render fonksiyonunu yeni şablonumuz olan urun_detay.html'e yönlendiriyoruz.
    return render(request, 'playground/urun_detay.html', context)