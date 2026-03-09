from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Prefetch
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate
from django.views.generic import CreateView, FormView, UpdateView, DetailView, TemplateView

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
        # Вызываем родительский метод, который выполняет вход и возвращает редирект
        response = super().form_valid(form)

        # user = form.get_user()  # Получаем пользователя из формы
        # Вместо получения пользователя из формы, получаем из запроса
        user = self.request.user
        if session_key and user.is_authenticated:
                # Передаем корзины с товарами неавторизованного пользователя в его аккаунт
                Basket.objects.filter(session_key=session_key).update(user=user)
                messages.success(self.request, f"Добро пожаловать! {user.username}")

        return response

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


class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'profile.html'
    success_url = reverse_lazy('user:profile')

    def get_object(self, queryset=None):
        """
        Получаем объект пользователя
        """
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = Order.objects.filter(user=self.request.user).prefetch_related(Prefetch(
                    'orderitem_set',
                    queryset=OrderItem.objects.select_related('product')
                )).order_by('-id')
        context['title'] = 'Личный кабинет'
        context['orders'] = orders
        return context


# @login_required
# def logout(request):
#     messages.success(request, f"{request.user.username} Пока-Пока!")
#     auth.logout(request)
#     return redirect(reverse("shop:catalogue"))
