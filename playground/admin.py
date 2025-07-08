from django.contrib import admin
from .models import Category, Product, Conversation, Message

# Admin panelini daha kullanışlı hale getirmek için özelleştirme sınıfları
# Bu sınıflar, admin panelinde modellerimizin nasıl görüneceğini ve davranacağını kontrol eder.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Kategori modeli için admin paneli ayarları.
    """
    list_display = ('name', 'slug')
    # 'slug' alanının, 'name' alanından otomatik olarak doldurulmasını sağlar.
    # Bu, her seferinde URL'yi elle yazma zahmetinden kurtarır.
    prepopulated_fields = {'slug': ('name',)}


class MessageInline(admin.TabularInline):
    """
    Bu, mesajları doğrudan ait oldukları sohbetin içinde görmemizi sağlar.
    """
    model = Message
    extra = 1 # Varsayılan olarak 1 tane boş mesaj kutusu gösterir.
    readonly_fields = ('sender', 'text', 'timestamp') # Mesajları buradan değiştiremeyiz, sadece görürüz.


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    """
    Sohbet modeli için admin paneli ayarları.
    """
    list_display = ('product', 'customer', 'created_at')
    list_filter = ('customer', 'product')
    search_fields = ('product__name', 'customer__username')
    # Yukarıda tanımladığımız MessageInline'ı buraya ekliyoruz.
    # Bu sayede her bir sohbetin detayına girdiğimizde, içindeki mesajları da liste halinde görebiliriz.
    inlines = [MessageInline]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Ürün modeli için admin paneli ayarları.
    """
    list_display = ('name', 'category', 'price', 'is_available', 'created_at')
    list_filter = ('category', 'is_available')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

# Message modelini ayrıca kaydetmeye gerek yok çünkü Conversation içinde gösteriyoruz,
# ama isterseniz ayrı bir sayfada görmek için aşağıdaki satırı ekleyebilirsiniz.
# admin.site.register(Message)