from django.contrib import admin
from .models import Specialty, Doctor, Review, ForbiddenWord, PermittedWords

admin.site.register(Specialty)
admin.site.register(Doctor)
admin.site.register(Review)
admin.site.register(ForbiddenWord)
admin.site.register(PermittedWords)
