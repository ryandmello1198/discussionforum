from django.contrib import admin
from home.models import UserProfile, Question, Answer
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Question)

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('user','email', 'approved')

admin.site.register(Answer,AnswerAdmin)
