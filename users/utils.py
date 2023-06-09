import re
import jdatetime
import datetime
from PIL import Image


def convert_shamsi_to_georgian(s):
    s = s.split("/")
    gregorian_date = jdatetime.date(int(s[0]), int(s[1]), int(s[2])).togregorian()
    return gregorian_date


def convert_georgian_to_shamsi(s):
    s = s.split("-")
    jalili_date = jdatetime.date.fromgregorian(day=int(s[2]), month=int(s[1]), year=int(s[0]))
    return str(jalili_date).replace("-", "/")


def validate_password(password):
    # At least 8 characters
    if len(password) < 8:
        return False

    # At least one uppercase letter
    if not any(char.isupper() for char in password):
        return False

    # At least one lowercase letter
    if not any(char.islower() for char in password):
        return False

    # At least one number
    if not any(char.isdigit() for char in password):
        return False

    # Return true if all conditions are met
    return True


def validate_username(username):
    if re.search("^[a-zA-Z0-9_]+$", username):
        return True
    else:
        return False


def validate_iranian_phone_number(phone_number):
    if len(phone_number) == 11 and phone_number[0] == '0' and phone_number[1] in ['9', '2']:
        return True
    else:
        return False


def calculate_age(born):
    today = datetime.date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def validate_picture(filename):
    try:
        image = Image.open(filename)
        # validate the image
        if image.size[0] > 0 and image.size[1] > 0:
            return True
    except:
        return False