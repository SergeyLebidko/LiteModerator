from django.shortcuts import render


# Контроллер главной страницы
def index(request):
    return render(request, 'main/index.html', {})
