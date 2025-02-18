#   Copyright 2025 João E. R. Manica
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

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
