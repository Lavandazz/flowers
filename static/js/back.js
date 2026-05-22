window.addEventListener('scroll', () => {
    const btn = document.querySelector('.back-to-top');
    if (window.scrollY > 300) {
        btn.classList.add('show');
    } else {
        btn.classList.remove('show');
    }
});

const backButton = document.querySelector('.back-to-top');
backButton.addEventListener('click', function () {
    window.scrollTo({top: 0, behavior: 'smooth'})
})