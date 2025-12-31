
window.onscroll = function () {
    const nav = document.querySelector('.zepto-nav');
    if (!nav) return;

    if (window.pageYOffset > 30) {
        nav.style.boxShadow = "0 10px 30px rgba(0,0,0,0.08)";
        nav.style.borderBottomColor = "transparent";
    } else {
        nav.style.boxShadow = "none";
        nav.style.borderBottomColor = "#f1f1f1";
    }
};

function getCSRFToken() {
    const tokenInput = document.querySelector('[name=csrfmiddlewaretoken]');
    return tokenInput ? tokenInput.value : '';
}
function getCSRFToken() {
    const el = document.querySelector('[name=csrfmiddlewaretoken]');
    return el ? el.value : '';
}

function getCSRFToken() {
    return document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
}
function getCSRFToken() {
    let cookieValue = null;
    if (document.cookie) {
        document.cookie.split(';').forEach(cookie => {
            cookie = cookie.trim();
            if (cookie.startsWith('csrftoken=')) {
                cookieValue = cookie.substring('csrftoken='.length);
            }
        });
    }
    return cookieValue;
}