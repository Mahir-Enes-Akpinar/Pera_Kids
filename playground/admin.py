# playground/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import (
    UserProfile, Category, Product, 
    ProductColor, ProductImage, Conversation, Message
)

# --- KULLANICI YÖNETİMİ ---
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Müşteri Ek Bilgileri'

class CustomUserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


# --- KATEGORİ YÖNETİMİ ---
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


# --- ÜRÜN YÖNETİMİ ---

# ÖNEMLİ DEĞİŞİKLİK: ProductColor için ayrı bir admin sınıfı oluşturuyoruz.
# Bu, her rengin kendi düzenleme sayfasına sahip olmasını sağlar.

class ProductImageInline(admin.TabularInline):
    """Resim ekleme formunu, Renk formunun içine gömmek için kullanılır."""
    model = ProductImage
    extra = 1

@admin.register(ProductColor)
class ProductColorAdmin(admin.ModelAdmin):
    """
    Bu, her bir rengin kendi admin sayfasında resimlerinin yönetilmesini sağlar.
    """
    list_display = ('product', 'color_name', 'price', 'quantity')
    # Resim ekleme formunu bu sayfaya dahil ediyoruz.
    inlines = [ProductImageInline]


# ProductColor formunu artık Product içinde göstermeyeceğiz çünkü kendi sayfası var.
# Sadece temel bilgileri görebiliriz.
class ProductColorInlineForProduct(admin.TabularInline):
    """
    Ürün sayfasında renkleri daha basit bir listede göstermek için.
    Bu inline'da resim ekleme yoktur.
    """
    model = ProductColor
    extra = 1
    fields = ('color_name', 'price', 'quantity', 'is_main_color')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Ana ürün admin arayüzü."""
    list_display = ('name', 'category', 'is_available')
    list_filter = ('is_available', 'category')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    # Renkleri yönetmek için basitleştirilmiş inline'ı kullanıyoruz.
    inlines = [ProductColorInlineForProduct]


# --- SOHBET YÖNETİMİ ---
# (Bu kısım aynı kalabilir)
class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ('sender', 'text', 'timestamp')

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('product', 'customer', 'created_at')
    inlines = [MessageInline]