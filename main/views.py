from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponseBadRequest

from .models import Review, Doctor
from .forms import UserRegisterForm, ReviewForm


# Контроллер страницы со ссылками для входа и оставления отзывов
def index(request):
    return render(request, 'main/index.html', {})


# Контроллер страницы со списком отзывов
@user_passes_test(lambda user: user.is_staff)
def review(request):
    reviews_list = Review.objects.filter(moderation_flag=True)
    context = {'reviews_list': reviews_list}
    return render(request, 'main/review.html', context)


# Контроллер списка врачей
def doctors_list(request):
    doctors = Doctor.objects.all()
    context = {'doctors': doctors}
    return render(request, 'main/doctors_list.html', context)


# Контроллер добавления нового отзыва
def add_review(request, doctor_id):
    doctor = get_object_or_404(Doctor, **{'pk': doctor_id})

    # Пользователь запросил форму
    if request.method == 'GET':
        return handle_get_method_for_add_review(request, doctor)

    # Пользователь отправил заполненную форму
    if request.method == 'POST':
        return handle_post_method_for_add_review(request, doctor)

    # В случае, если запрос некорректен - возвращаем страницу с ошибкой
    return HttpResponseBadRequest('Некорректный запрос к серверу')


# Контроллер, возвращающий страницу с сообщением об успешном добавлении отзыва
def success_review(request):
    return render(request, 'main/success_review_msg.html', {})


# Контроллер регистрации нового пользователя
def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            new_user = authenticate(request, username=request.POST['username'], password=request.POST['password1'])
            login(request, new_user)
            return HttpResponseRedirect(reverse_lazy('index'))

    if request.method == 'GET':
        form = UserRegisterForm()

    context = {'form': form}
    return render(request, 'main/user_register.html', context)


# Контроллер входа на сайт
class LoginController(LoginView):
    template_name = 'main/login.html'


# Контроллер выхода с сайта
class LogoutController(LogoutView):
    next_page = reverse_lazy('index')


# Функция для обработки GET-запросов в контроллере добавления отзыва
def handle_get_method_for_add_review(request, doctor):
    form = ReviewForm()
    context = {'doctor': doctor, 'form': form}
    return render(request, 'main/add_review.html', context)


# Функция для обрботки POST-запросов в контроллере добавления отзыва
def handle_post_method_for_add_review(request, doctor):
    # Проверяем форму. Если она не валидна, то выводим страницу ввода отзыва ещё раз
    form = ReviewForm(request.POST)
    if not form.is_valid():
        return render(request, 'main/add_review.html', {
            'form': form, 'doctor': doctor
        })

    # Если форма успешно проверена, то готовим данные к сохранению
    new_review = form.save(commit=False)
    new_review.doctor = doctor
    new_review.moderation_flag = False
    if request.user.is_authenticated:
        new_review.user = request.user
    new_review.user_ip = request.META['REMOTE_ADDR']
    new_review.finished_text = new_review.create_text_for_moderator()

    # Сохраняем данные и переводим пользователя на страничку с сообщением об успехе
    new_review.save()
    return HttpResponseRedirect(reverse_lazy('success_review'))
