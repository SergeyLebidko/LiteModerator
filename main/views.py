from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from .models import Review, Doctor


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


# Контроллер входа на сайт
class LoginController(LoginView):
    template_name = 'main/login.html'


# Контроллер выхода с сайта
class LogoutController(LogoutView):
    next_page = reverse_lazy('review')
