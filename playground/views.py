from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Conversation, Message
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm # AuthenticationForm'u ekliyoruz
from django.contrib.auth import login
from .forms import CustomUserCreationForm 

import json
from django.core.serializers.json import DjangoJSONEncoder


def anasayfa(request):
    """
    Ana sayfayı gösterir. Satışta olan ve en az bir rengi tanımlanmış
    tüm ürünleri verimli bir şekilde çeker.
    """
    # prefetch_related, ilgili tüm renk ve resimleri tek seferde çekerek
    # veritabanına yüzlerce sorgu atılmasını engeller. Bu, performans için kritiktir.
    urunler = Product.objects.filter(is_available=True, colors__isnull=False).distinct().prefetch_related(
        'colors__images'
    ).order_by('-created_at')

    context = {
        'urunler_listesi': urunler
    }
    return render(request, 'playground/anasayfa.html', context)


def urun_detay(request, slug):
    """
    Tek bir ürünün detay sayfasını gösterir.
    Ürünü, tüm renk ve resim varyasyonlarıyla birlikte çeker.
    """
    product = get_object_or_404(
        Product.objects.prefetch_related('colors__images'), 
        slug=slug, 
        is_available=True
    )

    # Renk verilerini JavaScript'e göndermek için hazırlıyoruz
    colors_data = {}
    for color in product.colors.all():
        images_urls = [img.image.url for img in color.images.all()]
        colors_data[color.id] = {
            'color_name': color.color_name,
            'price': color.price,
            'quantity': color.quantity,
            'images': images_urls
        }

    context = {
        'product': product,
        # Veriyi JSON formatında şablona güvenli bir şekilde gönderiyoruz
        'colors_data_json': json.dumps(colors_data, cls=DjangoJSONEncoder)
    }
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

