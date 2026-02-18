document.addEventListener('DOMContentLoaded', function() {
    const trigger = document.querySelector('.search-trigger');
    const overlay = document.querySelector('.search-overlay');
    const closeBtn = document.querySelector('.search-overlay-close');
    const searchInput = document.querySelector('.search-overlay-input');

    const cartTrigger = document.querySelector('.cart-trigger');
    const cartOverlay = document.querySelector('.cart-overlay');
    const closeButton = document.querySelector('.cart-panel-close');

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

        // Открыть корзину
    cartTrigger.addEventListener('click', function(e) {
        e.preventDefault();
        cartOverlay.classList.add('active');
    });

    // Закрыть по крестику
    closeButton.addEventListener('click', function() {
        cartOverlay.classList.remove('active');
    });

    // Закрыть по клику на затемнённый фон
    cartOverlay.addEventListener('click', function(e) {
        if (e.target === cartOverlay) {
            cartOverlay.classList.remove('active');
        }
    });
        // Закрыть по Escape
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && cartOverlay.classList.contains('active')) {
            cartOverlay.classList.remove('active');
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


// Закрытие уведомлений
document.addEventListener('DOMContentLoaded', function() {
    const notifications = document.querySelectorAll('.notification');

    notifications.forEach(function(notification) {
        // Функция скрытия уведомления
        const hideNotification = function() {
            // Добавляем класс для анимации исчезновения
            notification.classList.add('fade-out');
            // После окончания анимации удаляем элемент из DOM
            notification.addEventListener('animationend', function() {
                notification.remove();
                // Если контейнер стал пустым, можно его тоже скрыть или оставить
            }, { once: true });
        };

        // Автоматическое скрытие через 5 секунд
        const timer = setTimeout(hideNotification, 3000);

        // Кнопка закрытия
        const closeBtn = notification.querySelector('.notification-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', function() {
                clearTimeout(timer); // отменяем таймер, чтобы не было конфликта
                hideNotification();
            });
        }
    });
});
