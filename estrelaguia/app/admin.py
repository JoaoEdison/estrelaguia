from django.contrib import admin
from .models import *

admin.site.register(EmailUser)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(Attachment)
