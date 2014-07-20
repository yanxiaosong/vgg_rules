from django.core.management.base import BaseCommand, CommandError
from django.utils import translation


class Command(BaseCommand):

    can_import_settings = True

    def handle(self, *args, **options):

        # Activate a fixed locale, e.g. Russian
        translation.activate('ru')

        # Or you can activate the LANGUAGE_CODE # chosen in the settings:
        #
        #from django.conf import settings
        #translation.activate(settings.LANGUAGE_CODE)

        # Your command logic here
        # ...

        translation.deactivate()