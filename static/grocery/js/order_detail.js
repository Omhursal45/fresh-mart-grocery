const CONFIG = {
    steps: ['placed', 'packed', 'out_for_delivery', 'delivered'],
    labels: { placed: 'Placed', packed: 'Packed', out_for_delivery: 'Out for Delivery', delivered: 'Delivered' },
    icons: { placed: 'bi-check2-circle', packed: 'bi-box-seam', out_for_delivery: 'bi-truck', delivered: 'bi-house-check' }
};

// Fetch order status and render timeline
async function fetchStatus() {
    try {
        const res = await fetch(`/api/orders/{{ order.id }}/status/`);
        const data = await res.json();
        let html = '';

        CONFIG.steps.forEach((step, i) => {
            const isDone = CONFIG.steps.indexOf(data.current_status) >= i;
            const isActive = data.current_status === step;
            const hist = data.status_history.find(h => h.status === step);
            const time = hist ? new Date(hist.timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) : '';

            html += `
                <div class="stepper-item ${isDone ? 'completed' : ''} ${isActive ? 'active' : ''}">
                    <div class="step-dot"><i class="bi ${isDone && step !== 'delivered' ? 'bi-check-lg' : CONFIG.icons[step]}"></i></div>
                    <div class="step-content">
                        <strong class="${isActive ? 'text-success' : ''}">${CONFIG.labels[step]}</strong>
                        <small class="text-muted d-block">${time ? 'at ' + time : (isDone ? '' : 'Pending')}</small>
                    </div>
                </div>`;
        });

        document.getElementById('tracking-status').innerHTML = html;
    } catch (e) {
        document.getElementById('tracking-status').innerHTML = '<p class="text-muted small">Timeline currently unavailable.</p>';
    }
}

// Place order function
async function placeOrder() {
    try {
        const res = await fetch(`/api/orders/{{ order.id }}/place/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token }}'
            },
            body: JSON.stringify({ action: 'place_order' })
        });

        if (res.ok) {
            alert('Order placed successfully!');
            fetchStatus();  // Refresh timeline
            document.getElementById('place-order-btn').style.display = 'none'; // Hide button
        } else {
            const data = await res.json();
            alert('Error: ' + (data.message || 'Could not place order'));
        }
    } catch (e) {
        alert('Something went wrong while placing the order.');
    }
}

// Event listener
const placeBtn = document.getElementById('place-order-btn');
if (placeBtn) placeBtn.addEventListener('click', placeOrder);

// Initial fetch
fetchStatus();
