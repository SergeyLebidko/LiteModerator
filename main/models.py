from django.db import models
from django.contrib.auth.models import User


# Модель для хранения специальностей
class Specialty(models.Model):
    spec_name = models.CharField(max_length=100, verbose_name='Специальность')


# Модель для хранения врачей
class Doctor(models.Model):
    fio = models.CharField(max_length=250, verbose_name='ФИО врача')
    spec_name = models.ManyToManyField(Specialty)


# Модель для хранения отзывов
class Review(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name='ФИО врача')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь, оставивший отзыв')

    date_and_time_review = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время отзыва')
    origin_review_text = models.TextField(blank=False, verbose_name='Исходный отзыв')
    finished_review_text = models.TextField(blank=False, verbose_name='Обработанный отзыв')
    moderation_flag = models.BooleanField(default=False, null=False, verbose_name='Отзыв отмодерирован')

    user_ip = models.GenericIPAddressField(protocol='IPv4')


# Модель для хранения запрещенных слов
class ForbiddenWord(models.Model):
    word = models.CharField(max_length=100, verbose_name='Запрещенное слово')


# Модель для хранения слов исключений
class PermittedWords(models.Model):
    word = models.CharField(max_length=100, verbose_name='Слово-исключение')
