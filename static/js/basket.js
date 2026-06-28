document.addEventListener('DOMContentLoaded', function () {
    // Существующие элементы (successMessage, goodsInCartCount, cartItemsContainer, cartCountNav, cartIcon)
    const successMessage = document.getElementById('jq-notification');
    // const cartItemsContainer = document.getElementById('cart-panel-content'); // или другой контейнер
    // const cartCountNav = document.getElementById('cart-count');
    const cartIcon = document.getElementById('cart-icon');

    // Вспомогательная функция для получения CSRF-токена
    function getCsrfToken() {
        const csrfInput = document.querySelector('[name=csrfmiddlewaretoken]');
        return csrfInput ? csrfInput.value : '';
    }

    // --- Функция анимации полёта в корзину ---
    function animateFlyToCart(button, target) {
        if (!target) return; // если нет цели, выходим

        const btnRect = button.getBoundingClientRect();
        const targetRect = target.getBoundingClientRect();

        const flyer = document.createElement('div');
        flyer.className = 'flying-item';
        flyer.innerHTML = button.innerHTML; // копируем иконку

        // Начальная позиция – там же, где кнопка
        flyer.style.left = btnRect.left + 'px';
        flyer.style.top = btnRect.top + 'px';
        flyer.style.width = btnRect.width + 'px';
        flyer.style.height = btnRect.height + 'px';

        document.body.appendChild(flyer);

        // Принудительный reflow, чтобы transition применился
        flyer.offsetHeight;

        // Конечная позиция – на иконке корзины, с уменьшением и исчезновением
        flyer.style.left = targetRect.left + 'px';
        flyer.style.top = targetRect.top + 'px';
        flyer.style.width = '30px';
        flyer.style.height = '30px';
        flyer.style.opacity = '0';

        flyer.addEventListener('transitionend', function () {
            flyer.remove();
        }, { once: true });
    }

    // Функция обновления интерфейса после любого изменения корзины
    function updateCartUI(data) {
        // Показываем сообщение (если есть)
        if (successMessage && data.message) {
            successMessage.innerHTML = data.message;
            successMessage.style.display = 'block';
            setTimeout(() => {
                successMessage.style.display = 'none';
            }, 5000);
        }

         // Обновляем все возможные контейнеры корзины
        const cartContainers = document.querySelectorAll('#cart-panel-content, #cart-items-container');
        cartContainers.forEach(container => {
            if (container && data.basket_items_html) {
                container.innerHTML = data.basket_items_html;
            }
        });

        // Обновляем счётчик товаров везде
        const cartCounter = document.getElementById('cart-count');
        if (cartCounter && data.total_quantity !== undefined) {
            cartCounter.textContent = data.total_quantity;
        }
    }

    // Функция отправки запроса на изменение количества
    function changeQuantity(basketItemId, action, url) {
        const postData = new URLSearchParams({
            'basket_item_id': basketItemId,
            'action': action,  // 'increment' или 'decrement'
            'csrfmiddlewaretoken': getCsrfToken()
        });

        fetch(url, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: postData
        })
        .then(response => response.json())
        .then(data => {
            console.log('Изменение количества:', data.message);
            updateCartUI(data);
        })
        .catch(error => console.error('Ошибка при изменении количества:', error));
    }

    // Функция отправки запроса на удаление товара
    function removeFromCart(basketItemId, url) {
        const postData = new URLSearchParams({
            'basket_item_id': basketItemId,
            'csrfmiddlewaretoken': getCsrfToken()
        });

        fetch(url, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: postData
        })
        .then(response => response.json())
        .then(data => {
            console.log('Удаление товара:', data.message);
            updateCartUI(data);
        })
        .catch(error => console.error('Ошибка при удалении:', error));
    }

    // --- Существующая функция добавления товара (добавляем вызов updateCartUI) ---
    function addToCart(productId, url) {
        const csrfToken = getCsrfToken();
        const postData = new URLSearchParams({
            'product_id': productId,
            'csrfmiddlewaretoken': csrfToken
        });

        fetch(url, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: postData
        })
        .then(response => response.json())
        .then(data => {
            console.log('Товар добавлен:', data.message);
            updateCartUI(data);
        })
        .catch(error => console.error('Ошибка добавления:', error));
    }


    // --- Обработчик кликов на странице ---
    document.addEventListener('click', function (event) {
        // 1. Кнопка добавления в корзину
        const addBtn = event.target.closest('.add-to-cart');
        if (addBtn) {
            event.preventDefault(); // предотвращаем переход по ссылке
            showUnavailableMessage();
            
        }
        // if (addBtn) {
        //     event.preventDefault();
        //     if (cartIcon) animateFlyToCart(addBtn, cartIcon);
        //     const productId = addBtn.dataset.productId;
        //     const url = addBtn.getAttribute('href');
        //     addToCart(productId, url);
        //     return;
        // }

        // 2. Кнопки изменения количества (+ и -)
        const quantityBtn = event.target.closest('.quantity-btn');
        if (quantityBtn) {
            event.preventDefault();
            const basketItemId = quantityBtn.dataset.productId; // id элемента корзины
            const url = quantityBtn.dataset.cartChangeUrl;
            const action = quantityBtn.classList.contains('increment') ? 'increment' : 'decrement';
            if (basketItemId && url) {
                changeQuantity(basketItemId, action, url);
            }
            return;
        }

        // 3. Кнопка удаления
        const removeLink = event.target.closest('.remove-link');
        if (removeLink) {
            event.preventDefault();
            const basketItemId = removeLink.dataset.productId; // id элемента корзины
            const url = removeLink.getAttribute('href');
            if (basketItemId && url) {
                removeFromCart(basketItemId, url);
            }
        }
    });
});


// Радио-кнопки для доставки заказа
$(document).ready(function() {
    function toggleDeliveryAddress() {
        const selected = $('input[name="requires_delivery"]:checked').val();
        if (selected === '1') {
            $('#deliveryAddressField').show();  // или slideDown()
        } else {
            $('#deliveryAddressField').hide();  // или slideUp()
        }
    }

    // Проверяем при загрузке страницы
    toggleDeliveryAddress();

    // Следим за изменением радио-кнопок
    $('input[name="requires_delivery"]').change(toggleDeliveryAddress);
});

// Функция для показа окна о невозможности делать заказы
function showUnavailableMessage() {
    const modal = new bootstrap.Modal(document.getElementById('unavailableModal'));
    modal.show();
}