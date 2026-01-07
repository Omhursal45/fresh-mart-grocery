// grocery/js/checkout.js

function applyCoupon() {
    const subtotalElement = document.getElementById('subtotal-display');
    // Get numeric value from data attribute, NOT the text content
    const subtotal = parseFloat(subtotalElement.getAttribute('data-value'));
    const handlingFee = 2;
    const codeInput = document.getElementById('coupon-code');
    const code = codeInput.value.trim().toUpperCase();

    if (code === 'FRESH50') {
        const discount = 50;
        const newTotal = (subtotal - discount) + handlingFee;

        // Update UI Elements
        document.getElementById('discount-row').style.display = 'flex';
        document.getElementById('discount-amount').innerText = `-₹${discount}`;
        document.getElementById('final-total').innerText = `₹${newTotal}`;
        document.getElementById('btn-total').innerText = `₹${newTotal}`;
        document.getElementById('applied-discount').value = discount;
        
        document.getElementById('coupon-message').innerText = "Coupon Applied!";
        document.getElementById('coupon-message').className = "px-3 pb-2 small fw-bold text-success";
    }
}
// Ensure at least one address is selected if not default
document.getElementById('checkout-form').addEventListener('submit', function(e) {
    const addressSelected = document.querySelector('input[name="address_id"]:checked');
    if (!addressSelected) {
        e.preventDefault();
        alert("Please select a delivery address");
    }
});
// Add this to your existing checkout.js
document.getElementById('checkout-form').addEventListener('submit', function() {
    const placeOrderBtn = document.getElementById('place-order-btn');
    // Disable to prevent double-click and show loading
    placeOrderBtn.style.opacity = "0.7";
    placeOrderBtn.style.pointerEvents = "none";
    placeOrderBtn.querySelector('.fw-bold').innerHTML = 'PROCESSING...';
});