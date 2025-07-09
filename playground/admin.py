# playground/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Modellerimizin tamamını import ediyoruz
from .models import (
    UserProfile,
    Category,
    Product,
    ProductColor,
    ProductImage,
    Conversation,
    Message
)


# -----------------------------------------------------------------------------
# KULLANICI YÖNETİMİ
# Amacımız: Kullanıcı profili bilgilerini (adres, telefon vb.) doğrudan
# standart kullanıcı sayfasının içinde göstermek ve düzenlemek.
# -----------------------------------------------------------------------------

class UserProfileInline(admin.StackedInline):
    """Bu sınıf, UserProfile modelini User admin sayfasına gömmemizi sağlar."""
    model = UserProfile
    can_delete = False  # Profillerin silinmesini engeller
    verbose_name_plural = 'Müşteri Ek Bilgileri (Adres, Telefon vb.)'
    fk_name = 'user'

# Django'nun varsayılan UserAdmin sınıfını genişletiyoruz
class CustomUserAdmin(BaseUserAdmin):
    """Varsayılan kullanıcı adminine bizim profil inline'ımızı ekler."""
    inlines = (UserProfileInline,)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)

# Django'nun varsayılan User kaydını kaldırıp, yerine bizimkini kaydediyoruz
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


# -----------------------------------------------------------------------------
# KATEGORİ YÖNETİMİ
# -----------------------------------------------------------------------------

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Kategoriler için basit bir admin arayüzü."""
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


# -----------------------------------------------------------------------------
# ÜRÜN YÖNETİMİ
# Amacımız: Tek bir Ürün sayfasından, o ürüne ait tüm renkleri,
# resimleri, fiyatları ve stokları yönetebilmek.
# -----------------------------------------------------------------------------

class ProductImageInline(admin.TabularInline):
    """Resim ekleme formunu, Renk formunun içine gömmek için kullanılır."""
    model = ProductImage
    extra = 1  # Varsayılan olarak 1 boş resim yükleme alanı göster
    verbose_name = "Bu Renge Ait Resim"
    verbose_name_plural = "Bu Renge Ait Resimler"

class ProductColorInline(admin.StackedInline):
    """Renk, fiyat ve stok ekleme formunu, Ürün formunun içine gömmek için kullanılır."""
    model = ProductColor
    inlines = [ProductImageInline]  # Resim formunu da bu formun içine gömüyoruz
    extra = 1  # Varsayılan olarak 1 boş renk formu göster
    verbose_name = "Ürün Rengi, Fiyatı ve Stoğu"
    verbose_name_plural = "Ürün Renkleri, Fiyatları ve Stokları"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Ana ürün admin arayüzü."""
    list_display = ('name', 'category', 'is_available', 'created_at')
    list_filter = ('is_available', 'category')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    
    # Renk/Fiyat/Stok/Resim formlarını bu sayfaya dahil ediyoruz
    inlines = [ProductColorInline]


# -----------------------------------------------------------------------------
# SOHBET YÖNETİMİ
# -----------------------------------------------------------------------------

class MessageInline(admin.TabularInline):
    """Mesajları, ait oldukları sohbetin içinde göstermek için kullanılır."""
    model = Message
    extra = 0
    readonly_fields = ('sender', 'text', 'timestamp')
    can_delete = False

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    """Sohbetleri ve içindeki mesajları yönetmek için arayüz."""
    list_display = ('product', 'customer', 'created_at')
    readonly_fields = ('product', 'customer', 'created_at')
    search_fields = ('product__name', 'customer__username')
    inlines = [MessageInline]