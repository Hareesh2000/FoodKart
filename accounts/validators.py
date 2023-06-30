
import os

from django.forms import ValidationError


def image_validator(value):
    ext=os.path.splitext(value.name)[1]
    valid_extensions=['.jpg','.png','.jpeg']
    if not ext.lower() in valid_extensions:
        raise ValidationError("Unsupported File , Valid Extensions:" + str(valid_extensions))