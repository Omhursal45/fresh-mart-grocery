function changeQty(itemId, delta) {
    const input = document.getElementById(`qty-${itemId}`);
    let quantity = parseInt(input.value, 10) + delta;

    if (quantity < 1) {
        removeFromCart(itemId);
        return;
    }

    fetch(`/api/cart/update/${itemId}/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken()
        },
        body: JSON.stringify({ quantity })
    })
    .then(res => res.json())
    .then(data => {
        if (!data.success) return;

        input.value = data.quantity;
        document.getElementById(`total-${itemId}`).innerText =
            "₹" + data.total_price.toFixed(2);

        document.getElementById("cart-count").innerText = data.cart_count;
        updateCartTotal();
    });
    
}


function removeFromCart(itemId) {
    if (!confirm("Remove this item?")) return;

    fetch(`/api/cart/remove/${itemId}/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCSRFToken()
        }
    })
    .then(res => res.json())
    .then(data => {
        if (!data.success) return;

        document.getElementById(`cart-item-${itemId}`).remove();
        document.getElementById("cart-count").innerText = data.cart_count;

        if (data.cart_count === 0) location.reload();
        updateCartTotal();
    });
}


function updateCartTotal() {
    fetch("/api/cart/total/")
        .then(res => res.json())
        .then(data => {
            const subtotal = data.total;

            document.getElementById("cart-subtotal").innerText =
                "₹" + subtotal.toFixed(2);

            document.getElementById("cart-total").innerText =
                "₹" + (subtotal + 2).toFixed(2); // handling fee
        });
}

