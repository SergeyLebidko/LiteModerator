from django.shortcuts import render
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
