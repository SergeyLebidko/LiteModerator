from django.shortcuts import render


# Контроллер главной страницы
def review(request):
    return render(request, 'main/index.html', {})
