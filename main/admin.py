from django.contrib import admin
from .models import Specialty, Doctor, Review, ForbiddenWord, PermittedWords


# Редактор модели специальностей
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_display_links = ['name']
    search_fields = ['name']
    list_per_page = 50


# Редактор модели врачей
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['fio']
    list_display_links = ['fio']
    search_fields = ['fio']
    list_per_page = 50


# Редактор модели для отзывов
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'user', 'dt_created', 'dt_updated', 'origin_text', 'finished_text',
                    'moderation_flag',
                    'user_ip']
    list_display_links = ['doctor', 'user']
    search_fields = ['doctor', 'user']
    fields = ['doctor', 'user', 'dt_created', 'dt_updated', 'origin_text', 'finished_text', 'moderation_flag',
              'user_ip']
    readonly_fields = ['user', 'dt_created', 'dt_updated', 'origin_text', 'user_ip']
    list_per_page = 50


# Редактор модели для запрещенных слов
class ForbiddenWordsAdmin(admin.ModelAdmin):
    list_display = ['word']
    list_display_links = ['word']
    search_fields = ['word']
    list_per_page = 50


# Редактор модели для разрешенных слов
class PermittedWordsAdmin(admin.ModelAdmin):
    list_display = ['word']
    list_display_links = ['word']
    search_fields = ['word']
    list_per_page = 50


admin.site.register(Specialty, SpecialtyAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(ForbiddenWord, ForbiddenWordsAdmin)
admin.site.register(PermittedWords, PermittedWordsAdmin)
