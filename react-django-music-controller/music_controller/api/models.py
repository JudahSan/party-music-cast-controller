from django.db import models
import string
import random

# Create your models here.
# function to generate unique code to identify the room

def generate_unique_code():
    length = 6


    while True:
        code = ''.join(random.choices(string.ascii_uppercase, k=length))
        if Room.objects.filter(code=code).count() == 0:
            break

    return code
# Create first model -- room


# room class with attributes code,host, guest_can_pause
# votes_to_skip and created at
class Room(models.Model):
    code = models.CharField(
        max_length=8, default=generate_unique_code, unique=True)
    host = models.CharField(max_length=50, unique=True)
    guest_can_pause = models.BooleanField(null=False, default=False)
    votes_to_skip = models.IntegerField(null=False, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    