from django.core.management.base import BaseCommand


class Hello(BaseCommand):

    def handle(self, *args, **options):
        print('Hell World!')
