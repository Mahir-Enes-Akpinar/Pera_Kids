# Generated by Django 5.2.4 on 2025-07-08 19:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Kategori Adı')),
                ('slug', models.SlugField(help_text="URL'de görünecek metin, otomatik oluşur.", max_length=120, unique=True)),
            ],
            options={
                'verbose_name': 'Kategori',
                'verbose_name_plural': 'Kategoriler',
            },
        ),
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Müşteri')),
            ],
            options={
                'verbose_name': 'Sohbet',
                'verbose_name_plural': 'Sohbetler',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Mesaj Metni')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Gönderim Zamanı')),
                ('conversation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='playground.conversation', verbose_name='Ait Olduğu Sohbet')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Gönderen')),
            ],
            options={
                'verbose_name': 'Mesaj',
                'verbose_name_plural': 'Mesajlar',
                'ordering': ('timestamp',),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Ürün Adı')),
                ('slug', models.SlugField(help_text="URL'de görünecek metin, otomatik oluşur.", max_length=220, unique=True)),
                ('image', models.ImageField(upload_to='products/', verbose_name='Ürün Fotoğrafı')),
                ('description', models.TextField(verbose_name='Ürün Açıklaması')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Seri Fiyatı')),
                ('age_group_set', models.CharField(help_text='Örn: 8-10-12 Yaş', max_length=100, verbose_name='Yaş Grubu (Seri)')),
                ('available_colors', models.CharField(help_text='Renkleri virgülle ayırarak yazın. Örn: Mavi, Kırmızı, Yeşil', max_length=255, verbose_name='Mevcut Renkler')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')),
                ('is_available', models.BooleanField(default=True, verbose_name='Mevcut mu?')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='playground.category', verbose_name='Kategorisi')),
            ],
            options={
                'verbose_name': 'Ürün',
                'verbose_name_plural': 'Ürünler',
                'ordering': ('-created_at',),
            },
        ),
        migrations.AddField(
            model_name='conversation',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='playground.product', verbose_name='İlgili Ürün'),
        ),
        migrations.AlterUniqueTogether(
            name='conversation',
            unique_together={('product', 'customer')},
        ),
    ]
