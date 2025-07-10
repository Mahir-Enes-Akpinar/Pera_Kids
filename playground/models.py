from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# --- KULLANICI PROFİLİ VE ADRES MODELİ ---
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile', verbose_name="Kullanıcı")
    company_name = models.CharField(max_length=200, blank=True, null=True, verbose_name="Firma Adı")
    tax_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="Vergi Numarası")
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefon Numarası")
    street = models.CharField(max_length=255, blank=True, null=True, verbose_name="Sokak ve Numara")
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name="Şehir / İl")
    state = models.CharField(max_length=100, blank=True, null=True, verbose_name="İlçe")
    postal_code = models.CharField(max_length=10, blank=True, null=True, verbose_name="Posta Kodu")

    def __str__(self):
        return f"{self.user.username}'nin Profili"

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.profile.save()


# --- ÜRÜN KATALOĞU MODELLERİ ---
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Kategori Adı")
    slug = models.SlugField(max_length=120, unique=True, help_text="URL'de görünecek metin, otomatik oluşur.")
    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategoriler"
    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name="Kategorisi")
    name = models.CharField(max_length=200, verbose_name="Ürün Adı")
    slug = models.SlugField(max_length=220, unique=True, help_text="URL'de görünecek metin, otomatik oluşur.")
    description = models.TextField(verbose_name="Ürün Açıklaması")
    age_group_set = models.CharField(max_length=100, verbose_name="Yaş Grubu (Seri)", help_text="Örn: 8-10-12 Yaş")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    is_available = models.BooleanField(default=True, verbose_name="Satışta mı?")
    is_notification_sent = models.BooleanField(default=False, verbose_name="Yeni Ürün Bildirimi Gönderildi mi?")

    class Meta:
        verbose_name = "Ürün"
        verbose_name_plural = "Ürünler"
        ordering = ('-created_at',)

    def __str__(self):
        return self.name

    def get_main_color(self):
        return self.colors.filter(is_main_color=True).first()

    def get_main_image(self):
        main_color = self.get_main_color()
        if main_color:
            return main_color.images.first()
        return None

class ProductColor(models.Model):
    """
    Bir ürünün renk varyasyonunu, fiyatını, ana renk olup olmadığını ve 
    en önemlisi STOK ADEDİNİ belirtir.
    """
    product = models.ForeignKey(Product, related_name='colors', on_delete=models.CASCADE, verbose_name="Ait Olduğu Ürün")
    color_name = models.CharField(max_length=50, verbose_name="Renk Adı", help_text="Örn: Bebek Mavisi, Fuşya")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Bu Rengin Seri Fiyatı")
    
    # YENİ EKLENEN STOK ALANI
    quantity = models.PositiveIntegerField(default=0, verbose_name="Stok Adedi (Seri)", help_text="Bu renkten kaç seri stokta olduğunu belirtin.")
    
    is_main_color = models.BooleanField(default=False, verbose_name="Ana Renk mi?", help_text="Bu renk, ürün kartlarında gösterilecek. Her ürün için sadece BİR tane ana renk seçin.")
    
    class Meta:
        verbose_name = "Ürün Rengi ve Stoğu"
        verbose_name_plural = "Ürün Renkleri ve Stokları"
        unique_together = ('product', 'color_name')
    def __str__(self):
        return f"{self.product.name} - {self.color_name} ({self.quantity} adet)"

class ProductImage(models.Model):
    color_variant = models.ForeignKey(ProductColor, related_name='images', on_delete=models.CASCADE, verbose_name="Ait Olduğu Renk")
    image = models.ImageField(upload_to='products/', verbose_name="Resim")

    class Meta:
        verbose_name = "Ürün Resmi"
        verbose_name_plural = "Ürün Resimleri"
    def __str__(self):
        return f"Resim: {self.color_variant.product.name} - {self.color_variant.color_name}"


# --- SOHBET MODELLERİ (Değişiklik yok) ---
class Conversation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="İlgili Ürün")
    customer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Müşteri")
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = "Sohbet"
        verbose_name_plural = "Sohbetler"
        unique_together = ('product', 'customer')
    def __str__(self):
        return f"{self.customer.username} - {self.product.name} Sohbeti"

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE, verbose_name="Ait Olduğu Sohbet")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Gönderen")
    text = models.TextField(verbose_name="Mesaj Metni")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Gönderim Zamanı")
    class Meta:
        verbose_name = "Mesaj"
        verbose_name_plural = "Mesajlar"
        ordering = ('timestamp',)
    def __str__(self):
        return f"{self.sender.username}: {self.text[:30]}..."