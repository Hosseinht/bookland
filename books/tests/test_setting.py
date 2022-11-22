import os

from django.conf import settings

from bookland.settings import *

path = settings.BASE_DIR
file_path = os.path.join(path, "books/tests/test_data/media/books/images/")

# MEDIA_ROOT = file_path / 'media'
