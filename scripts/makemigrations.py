"""A stand-alone equivalent of `python manage.py makemigrations`."""

import django
from django.conf import settings
from django.core.management import call_command


if __name__ == "__main__":
    APP = "rest_framework_api_key"
    settings.configure(INSTALLED_APPS=[APP, "tests.project.heroes"])
    django.setup()
    call_command("makemigrations", APP, "heroes")
