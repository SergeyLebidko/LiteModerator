from django.shortcuts import render
from .models import Review


# Контроллер главной страницы
def review(request):
    # Получаем список отзывов
    reviews = Review.objects.all()

    context = {'reviews': reviews}
    return render(request, 'main/index.html', context)
