
        // Smooth shadow transition on scroll
        window.onscroll = function() {
            const nav = document.querySelector('.zepto-nav');
            if (window.pageYOffset > 30) {
                nav.style.boxShadow = "0 10px 30px rgba(0,0,0,0.08)";
                nav.style.borderBottomColor = "transparent";
            } else {
                nav.style.boxShadow = "none";
                nav.style.borderBottomColor = "#f1f1f1";
            }
        };