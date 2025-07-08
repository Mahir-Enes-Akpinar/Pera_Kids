# playground/models.py

from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Kategori Adı")
    slug = models.SlugField(max_length=120, unique=True, help_text="URL'de görünecek metin, otomatik oluşur.")

    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategoriler"

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name="Kategorisi")
    name = models.CharField(max_length=200, verbose_name="Ürün Adı")
    slug = models.SlugField(max_length=220, unique=True, help_text="URL'de görünecek metin, otomatik oluşur.")
    image = models.ImageField(upload_to='products/', verbose_name="Ürün Fotoğrafı")
    description = models.TextField(verbose_name="Ürün Açıklaması")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Seri Fiyatı")
    age_group_set = models.CharField(max_length=100, verbose_name="Yaş Grubu (Seri)", help_text="Örn: 8-10-12 Yaş")
    available_colors = models.CharField(max_length=255, verbose_name="Mevcut Renkler", help_text="Renkleri virgülle ayırarak yazın. Örn: Mavi, Kırmızı, Yeşil")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    is_available = models.BooleanField(default=True, verbose_name="Mevcut mu?")

    class Meta:
        verbose_name = "Ürün"
        verbose_name_plural = "Ürünler"
        ordering = ('-created_at',)

    def __str__(self):
        return self.name

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