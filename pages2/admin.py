from django.contrib import admin

from .models import Estimate, Question, Forum

admin.site.register(Estimate)
admin.site.register(Question)
admin.site.register(Forum)
