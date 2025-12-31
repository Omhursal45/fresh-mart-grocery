document.querySelectorAll('.add-to-cart-btn').forEach(btn => {
    btn.addEventListener('click', function () {
        const pId = this.dataset.productId;

        // 🔹 Instant UI feedback
        this.disabled = true;
        this.innerText = 'ADDING...';

        fetch(`/add-to-cart/${pId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCSRFToken()
            }
        })
        .then(res => {
            if (!res.ok) throw new Error('Request failed');
            return res.json();
        })
        .then(data => {
            if (data.status === 'success') {
                // 🔹 Update cart count immediately
                document.getElementById('cart-count').innerText = data.cart_count;

                // 🔹 Success UI
                this.innerText = '✓ ADDED';
                this.classList.add('btn-success');
                this.classList.remove('btn-add-v2');

                // 🔹 Reset after 1.2s (not 2s)
                setTimeout(() => {
                    this.innerText = 'ADD';
                    this.disabled = false;
                    this.classList.remove('btn-success');
                    this.classList.add('btn-add-v2');
                }, 1200);
            } else {
                window.location.href = '/login';
            }
        })
        .catch(err => {
            console.error(err);
            this.innerText = 'ADD';
            this.disabled = false;
        });
    });
});
