from PIL import Image
from django.db.models.signals import post_save
from .models import Post


def image_compressor(sender, **kwargs):
    if kwargs["created"]:
        with Image.open(kwargs["instance"].image.path) as image:
            print("Inside with statement")
            image.save(kwargs["instance"].image.path, optimize=True, quality=20)


post_save.connect(image_compressor, sender=Post)

