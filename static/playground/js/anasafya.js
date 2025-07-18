
document.addEventListener('DOMContentLoaded', function() {
    // Sayfadaki tüm renk kutucuklarını seç
    const colorSwatches = document.querySelectorAll('.renk-kutusu');

    // Her bir renk kutucuğuna tıklama olayı ekle
    colorSwatches.forEach(swatch => {
        swatch.addEventListener('click', function(event) {
            // Ana ürün linkine gitmesini engelle, sadece rengi değiştir
            event.preventDefault();
            event.stopPropagation();

            const productId = this.dataset.productId;
            const newImageUrl = this.dataset.imageUrl;

            // Tıklanan renge ait ürün kartının resmini bul
            const productImage = document.getElementById(`product-image-${productId}`);
            
            // Resmin kaynağını (src) yeni resim URL'i ile değiştir
            if (productImage && newImageUrl) {
                productImage.src = newImageUrl;
            }

            // 'active' stilini yönet:
            // Önce aynı karttaki tüm aktif stillerini kaldır
            const parentCard = this.closest('.urun-karti');
            parentCard.querySelectorAll('.renk-kutusu').forEach(s => s.classList.remove('active'));
            // Sadece tıklanan kutucuğa 'active' stilini ekle
            this.classList.add('active');
        });
    });
});