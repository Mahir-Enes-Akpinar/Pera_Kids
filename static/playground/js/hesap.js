document.addEventListener('DOMContentLoaded', function() {
    const loginTab = document.getElementById('loginTab');
    const signupTab = document.getElementById('signupTab');
    const loginSection = document.getElementById('loginSection');
    const signupSection = document.getElementById('signupSection');

    // Elementlerin sayfada var olup olmadığını kontrol et
    if (loginTab && signupTab && loginSection && signupSection) {
        loginTab.onclick = function() {
            loginTab.classList.add('active');
            signupTab.classList.remove('active');
            loginSection.classList.add('active');
            signupSection.classList.remove('active');
        };
        
        signupTab.onclick = function() {
            signupTab.classList.add('active');
            loginTab.classList.remove('active');
            signupSection.classList.add('active');
            loginSection.classList.remove('active');
        };
    }
});