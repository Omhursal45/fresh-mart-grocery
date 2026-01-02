let currentQty = 1;
let currentWeight = 1;

// Read base price safely
const basePrice = parseFloat(document.getElementById('productPrice').dataset.price) || 0;

// Handle Weight Selection
document.querySelectorAll('.weight-chip').forEach(chip => {
    chip.addEventListener('click', function() {
        document.querySelectorAll('.weight-chip').forEach(c => c.classList.remove('active'));
        this.classList.add('active');
        currentWeight = parseFloat(this.dataset.val) || 1;
        updateDisplayPrice();
    });
});

function updateQty(delta) {
    currentQty = Math.max(1, currentQty + delta);
    document.getElementById('qtyVal').innerText = currentQty;
    updateDisplayPrice();
}

function updateDisplayPrice() {
    const total = (basePrice || 0) * (currentWeight || 1) * (currentQty || 1);
    const formatted = total.toFixed(2);
    document.getElementById('displayPrice').innerText = formatted;
    document.getElementById('mobileTotal').innerText = formatted;
}

// Modern AJAX Add to Cart
async function handleAddToCart() {
    const btn = document.getElementById('addBtn');
    const originalText = btn.innerHTML;

    btn.disabled = true;
    btn.innerHTML = `<span class="spinner-border spinner-border-sm me-2"></span> Adding...`;

    const csrftoken = document.querySelector('meta[name="csrf-token"]').content;

    const payload = {
        product_id: "{{ product.id }}",
        quantity: currentQty,
        weight: currentWeight,
        is_weight_based: "{{ product.is_weight_based }}" === "True"
    };

    try {
        const response = await fetch(`/add-to-cart/${payload.product_id}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (data.status === 'success') {
            btn.classList.replace('btn-success', 'btn-dark');
            btn.innerHTML = `<i class="bi bi-check-lg me-2"></i> Added to Cart`;
            if (window.updateCartCount) window.updateCartCount(data.cart_count);
        } else {
            alert(data.message);
            btn.disabled = false;
            btn.innerHTML = originalText;
        }
    } catch (error) {
        console.error('Error:', error);
        btn.disabled = false;
        btn.innerHTML = originalText;
    }
}
