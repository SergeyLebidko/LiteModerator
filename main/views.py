from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponseBadRequest

from .models import Review, Doctor
from .forms import UserRegisterForm, ReviewForm


# Контроллер главной страницы
def review(request):
    reviews = Review.objects.all()
    context = {'reviews': reviews}
    return render(request, 'main/index.html', context)


# Контроллер списка врачей
def doctors_list(request):
    doctors = Doctor.objects.all()
    context = {'doctors': doctors}
    return render(request, 'main/doctors_list.html', context)


# Контроллер добавления нового отзыва
def add_review(request, doctor_id):
    # Если пользователь запросил форму
    if request.method == 'GET':
        try:
            doctor = Doctor.objects.get(pk=doctor_id)
        except Doctor.DoesNotExist:
            HttpResponseBadRequest('Некорректный запрос к серверу')
        form = ReviewForm()
        url_for_action = reverse('add_review', kwargs={'doctor_id': doctor_id})
        context = {'doctor': doctor, 'form': form, 'url_for_action': url_for_action}
        return render(request, 'main/add_review.html', context)

    # Пользователь отправил заполненную форму
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(reverse_lazy('success_review'))
        else:
            return render(request, 'main/add_review.html', {
                'form': form
            })

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
            return HttpResponseRedirect(reverse_lazy('review'))

    if request.method == 'GET':
        form = UserRegisterForm()

    context = {'form': form}
    return render(request, 'main/user_register.html', context)


# Контроллер входа на сайт
class LoginController(LoginView):
    template_name = 'main/login.html'


# Контроллер выхода с сайта
class LogoutController(LogoutView):
    next_page = reverse_lazy('review')
