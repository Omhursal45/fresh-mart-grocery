document.querySelectorAll('.add-to-cart-btn').forEach(button => {
    button.addEventListener('click', function (e) {
        e.preventDefault();

        const productId = this.dataset.productId;
        const btn = this;

        const csrfToken = document
            .querySelector('meta[name="csrf-token"]')
            .getAttribute('content');

        if (btn.classList.contains('disabled')) return;

        btn.classList.add('disabled');
        btn.innerHTML = `<span class="spinner-border spinner-border-sm"></span>`;

        fetch(`/add-to-cart/${productId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json'
            }
        })
        .then(res => res.json())
        .then(data => {
            if (data.status === 'success') {

                const cartBadge = document.getElementById('cart-count');
                if (cartBadge) {
                    cartBadge.innerText = data.cart_count;
                }

                btn.innerText = '✓ ADDED';
                btn.classList.replace('btn-outline-danger', 'btn-success');

                setTimeout(() => {
                    btn.innerText = 'ADD';
                    btn.classList.replace('btn-success', 'btn-outline-danger');
                    btn.classList.remove('disabled');
                }, 1500);

            } else {
                window.location.href = '/login/';
            }
        })
        .catch(err => {
            console.error('Error:', err);
            btn.classList.remove('disabled');
            btn.innerText = 'ADD';
        });
    });
});
