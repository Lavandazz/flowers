document.addEventListener('DOMContentLoaded', function() {
    const trigger = document.querySelector('.search-trigger');
    const overlay = document.querySelector('.search-overlay');
    const closeBtn = document.querySelector('.search-overlay-close');
    const searchInput = document.querySelector('.search-overlay-input');

    if (!trigger || !overlay || !closeBtn) return;

    // Открыть оверлей
    trigger.addEventListener('click', function(e) {
        e.preventDefault();
        overlay.classList.add('active');
        // Фокус на поле ввода после анимации
        setTimeout(() => searchInput.focus(), 100);
    });

    // Закрыть по крестику
    closeBtn.addEventListener('click', function() {
        overlay.classList.remove('active');
    });

    // Закрыть по клику на фон (сам оверлей)
    overlay.addEventListener('click', function(e) {
        if (e.target === overlay) {
            overlay.classList.remove('active');
        }
    });

    // Закрыть по Escape
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && overlay.classList.contains('active')) {
            overlay.classList.remove('active');
        }
    });

    // При отправке формы оверлей автоматически закроется (стандартное поведение браузера)
});