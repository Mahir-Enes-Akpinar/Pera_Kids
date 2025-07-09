from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Conversation, Message
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm # AuthenticationForm'u ekliyoruz
from django.contrib.auth import login
from .forms import CustomUserCreationForm 
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

@login_required
def sohbet_baslat(request, product_id):
    """
    Giriş yapmış bir kullanıcı ile bir ürün arasında bir sohbet oluşturur
    veya mevcut olanı bulur, ardından kullanıcıyı sohbetler sayfasına yönlendirir.
    """
    # URL'den gelen id ile ürünü buluyoruz. Bulamazsa 404 hatası verir.
    product = get_object_or_404(Product, id=product_id)
    
    # Bu ürün ve şu anki kullanıcı (request.user) arasında bir sohbet arıyoruz.
    # Eğer yoksa, yeni bir tane oluşturuyoruz. Varsa, mevcut olanı getiriyoruz.
    # get_or_create() bu işi tek satırda yapar ve bize iki değer döndürür:
    # 1. nesnenin kendisi (sohbet)
    # 2. nesnenin yeni mi oluşturulduğu (created - True/False)
    sohbet, created = Conversation.objects.get_or_create(
        customer=request.user,
        product=product
    )

    # Şimdilik, sohbeti başlattıktan sonra kullanıcıyı ana sayfaya yönlendirelim.
    # Daha sonra burayı direkt sohbetin kendisine yönlendirecek şekilde güncelleyeceğiz.
    # TODO: Kullanıcıyı sohbet detay sayfasına yönlendir.
    return redirect('playground:anasayfa')


def hesap_view(request):
    login_form = AuthenticationForm(request)
    # Standart form yerine kendi özel formumuzu kullanıyoruz
    register_form = CustomUserCreationForm()

    if request.method == 'POST':
        if 'login_submit' in request.POST:
            login_form = AuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                return redirect('playground:anasayfa')
        
        elif 'register_submit' in request.POST:
            # Standart form yerine kendi özel formumuzu kullanıyoruz
            register_form = CustomUserCreationForm(request.POST)
            if register_form.is_valid():
                user = register_form.save()
                login(request, user)
                return redirect('playground:anasayfa')

    context = {
        'login_form': login_form,
        'register_form': register_form,
        'hesap_sayfasi': True
    }
    return render(request, 'playground/hesap.html', context)


@login_required
def sohbetlerim_view(request):
    """
    Giriş yapmış kullanıcının mevcut tüm sohbetlerini listeler.
    """
    # Conversation modelinde, 'customer' alanı o an giriş yapmış kullanıcı (request.user)
    # olan tüm kayıtları buluyoruz. En yeniden eskiye doğru sıralıyoruz.
    sohbetler = Conversation.objects.filter(customer=request.user).order_by('-created_at')

    context = {
        'sohbet_listesi': sohbetler
    }
    return render(request, 'playground/sohbetlerim.html', context)