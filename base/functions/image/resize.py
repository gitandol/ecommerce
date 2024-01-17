import os
from django.conf import settings
from PIL import Image


def resize_image(img, new_width=800):
    img_full_path = os.path.join(settings.MEDIA_ROOT, img.name)
    img_pil = Image.open(img_full_path)
    original_width, original_height = img_pil.size

    if original_width <= new_width:
        img_pil.close()
        return False

    new_height = round((new_width * original_height) / original_width)
    new_img = img_pil.resize((new_width, new_height), Image.LANCZOS)
    new_img.save(
        img_full_path,
        optimize=True,
        quality=50
    )
    return True


def crop_image(img):
    crop = False
    new_height, new_width = 800, 800
    img_full_path = os.path.join(settings.MEDIA_ROOT, img.name)
    img_pil = Image.open(img_full_path)
    original_width, original_height = img_pil.size
    diferenca = int(abs(original_height-original_width)/2)

    if original_width > original_height:
        new_width = original_height
        new_height = original_height
        crop = True
    elif original_width < original_height:
        new_width = original_width
        new_height = original_width
        crop = True

    if crop:
        new_img = img_pil.crop((int(diferenca/2), int(diferenca/2), new_width, new_height))
        new_img.save(
            img_full_path,
            optimize=True,
            quality=50
        )
        return True
    return False
