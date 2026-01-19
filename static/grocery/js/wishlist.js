
function removeFromWishlist(productId, btn) {
    fetch('/api/wishlist/', {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ product_id: productId })
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === 'success') {
            // remove the card from DOM
            btn.closest('.col-6').remove();
            alert(data.message);
        } else {
            alert(data.message || 'Error removing item');
        }
    })
    .catch(() => alert('Error removing item'));
}

function getCookie(name) {
    return document.cookie.split('; ').find(row => row.startsWith(name + '='))?.split('=')[1];
}