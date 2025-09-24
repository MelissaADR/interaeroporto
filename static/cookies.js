function aceitarCookies() {
    fetch('/aceitar_cookies')
        .then(() => {
            document.getElementById('cookie-banner').style.display = 'none';
        });
}

function rejeitarCookies() {
    fetch('/rejeitar_cookies')
        .then(() => {
            document.getElementById('cookie-banner').style.display = 'none';
        });
}
