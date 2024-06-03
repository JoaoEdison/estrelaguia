from django.contrib import admin
from .models import *

admin.site.register(EmailUser)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Publication)
admin.site.register(Comment)
admin.site.register(Attachment)
