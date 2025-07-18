// Bu script'in çalışması için, şablondan gelen colorsData nesnesine ihtiyacı var.
// Bu yüzden bu script'i çağırmadan önce şablonda bu veriyi tanımlamalıyız.

function initializeProductGallery(colorsData) {
    const mainImage = document.getElementById('mainProductImage');
    const thumbnailContainer = document.getElementById('thumbnailContainer');
    const productPrice = document.getElementById('productPrice');
    const productStock = document.getElementById('productStock');

    // Küçük resme tıklandığında ana resmi değiştirir
    window.changeMainImage = function(element, imageUrl) {
        if (mainImage) {
            mainImage.src = imageUrl;
        }
        document.querySelectorAll('.thumbnail').forEach(thumb => thumb.classList.remove('active'));
        element.classList.add('active');
    }

    // Renk butonuna tıklandığında tüm bilgileri günceller
    window.selectColor = function(element, colorId) {
        const selectedColor = colorsData[colorId];
        if (!selectedColor) return;

        // Ana resmi, fiyatı ve stok bilgilerini güncelle
        if (selectedColor.images.length > 0) {
            if (mainImage) mainImage.src = selectedColor.images[0];
        } else {
            // Eğer resim yoksa varsayılan resmi göster (bu path'i kendi projenize göre ayarlayın)
            if (mainImage) mainImage.src = "/static/playground/img/placeholder.png";
        }
        
        if (productPrice) productPrice.textContent = `${selectedColor.price} TL`;
        if (productStock) {
            productStock.textContent = selectedColor.quantity > 0 ? `Stokta: ${selectedColor.quantity} adet` : 'Stokta Yok';
        }

        // Küçük resim (thumbnail) galerisini güncelle
        if (thumbnailContainer) {
            thumbnailContainer.innerHTML = ''; // Mevcut küçük resimleri temizle
            selectedColor.images.forEach(imageUrl => {
                const thumb = document.createElement('img');
                thumb.src = imageUrl;
                thumb.className = 'thumbnail';
                thumb.onclick = () => changeMainImage(thumb, imageUrl);
                thumbnailContainer.appendChild(thumb);
            });
            // İlk küçük resmi aktif yap
            if (thumbnailContainer.firstChild) {
                thumbnailContainer.firstChild.classList.add('active');
            }
        }
        
        // Aktif buton stilini ayarla
        document.querySelectorAll('.renk-butonu').forEach(button => button.classList.remove('active'));
        element.classList.add('active');
    }

    // Sayfa yüklendiğinde ilk thumbnail'i aktif yap
    if (thumbnailContainer && thumbnailContainer.firstChild) {
        thumbnailContainer.firstChild.classList.add('active');
    }
}