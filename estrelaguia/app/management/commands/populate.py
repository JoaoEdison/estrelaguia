from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password, is_password_usable
from app.models import *

base_users = [
    ('Kepler71', 'johanneskepler@sol.com', 'sol'),
    ('GalileuG', 'galileug@lua.com', 'lua'),
    ('Isaac', 'newton@marte.com', 'marte')
]

class Command(BaseCommand):
    def handle(self, *args, **options):
        for account in base_users: 
            password = make_password(account[2])
            if is_password_usable(password) == False:
                self.stderr.write("O hash da senha não pode ser feito.")
                return
            user = EmailUser(username=account[0], email=account[1], password=password)
            user.save()
        self.stdout.write("Fim")
