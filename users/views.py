from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db.models import Prefetch
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate
from django.views.generic import CreateView

from basket.models import Basket
from basket.utils import get_user_baskets
from orders.models import Order, OrderItem
from users.forms import UserLoginForm, UserRegisterForm, ProfileForm
from users.models import User


# Create your views here.

class UserLoginView(LoginView):
    template_name = 'login.html'
    form_class = UserLoginForm

    def get_success_url(self):
        redirect_page = self.request.POST.get('next', None)
        # если пользователь вышел, перенаправляем на logout
        if redirect_page and redirect_page != reverse('user:logout'):
            return redirect_page
        return reverse_lazy('shop:catalogue')

    def form_valid(self, form):
        # Сессионный ключ для перенесения корзины неавторизованного пользователя, авторизованному
        session_key = self.request.session.session_key
        # Получаем пользователя из формы
        user = form.get_user()
        if user:
            # Возвращаем пользователя
            auth.login(self.request, user)
            if session_key:
                # Передаем корзины с товарами неавторизованного пользователя в его аккаунт
                Basket.objects.filter(session_key=session_key).update(user=user)
                messages.success(self.request, f"Добро пожаловать! {user.username}")

                return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Авторизация'
        return context


class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'registration.html'
    success_url = reverse_lazy('user:profile')

    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.instance  # Получаем юзера из формы

        if user:
            form.save()  # сохраняем в бд
            auth.login(self.request, user)
            messages.success(self.request, "Регистрация прошла успешно.")

        if session_key:
            Basket.objects.filter(session_key=session_key).update(user=user)

        messages.success(self.request, f"Добро пожаловать! {user.username}")
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Регистрация'
        return context


@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()  # сохраняем в бд
            # Перенаправляем
            return HttpResponseRedirect(reverse("shop:catalogue"))
    else:
        # instance=request.user берем и передаем юзера в форму профиля
        form = ProfileForm(instance=request.user)

    # Получаем заказы юзера через его ID
    # В запросе к бд user=request.user через ORM передается именно ID

    # 1. Фильтруем по юзеру
    # 2. Используем обратный порядок фильтрации Prefetch
    # 3. Выбираем все OrderItem через связанный 'product'
    # 4. Сортируем в обратном порядке по id
    orders = Order.objects.filter(user=request.user).prefetch_related(Prefetch(
        'orderitem_set',
        queryset=OrderItem.objects.select_related('product')
    )).order_by('-id')

    context = {'title': 'Профиль',
               'form': form,
               'orders': orders}
    return render(request, 'profile.html', context)


@login_required
def user_basket(request):
    return render(request, 'user_basket.html')


@login_required
def logout(request):
    messages.success(request, f"{request.user.username} Пока-Пока!")
    auth.logout(request)
    return redirect(reverse("shop:catalogue"))
