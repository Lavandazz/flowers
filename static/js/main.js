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

// Открытие фильтра для фильтрации каталога цен
document.addEventListener('DOMContentLoaded', function() {
    const filterTrigger = document.querySelector('.filter-trigger');
    const filterDropdown = document.querySelector('.filter-dropdown');

    if (filterTrigger && filterDropdown) {
        // Клик по кнопке переключает дропдаун
        filterTrigger.addEventListener('click', function(e) {
            e.stopPropagation();  // чтобы не сработал обработчик на document
            filterDropdown.classList.toggle('active');
        });

        // Закрытие при клике вне дропдауна
        document.addEventListener('click', function(e) {
            if (!filterTrigger.contains(e.target) && !filterDropdown.contains(e.target)) {
                filterDropdown.classList.remove('active');
            }
        });
    }
});

// Появление глазика для просмотра пароля в поле входа
function PasswordVisibility(fieldId, iconId) {
    const field = document.getElementById(fieldId);
    const icon = document.getElementById(iconId);

    // Определяем текущий тип поля
    const isPassword = field.getAttribute('type') === 'password';

    if (isPassword) {
        // Если пароль скрыт type="password", меняем на text и картинку
        field.setAttribute('type', 'text');
        // Меняем иконку: убираем закрытый глаз, добавляем открытый
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    } else {
        // Пароль виден, удаляем картинку и меняем
        field.setAttribute('type', 'password');
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    }
}