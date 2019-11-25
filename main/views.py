from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect

from .models import Review, Doctor
from .forms import UserRegisterForm


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
    doctor = Doctor.objects.get(pk=doctor_id)
    context = {'doctor': doctor}
    return render(request, 'main/add_review.html', context)


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
