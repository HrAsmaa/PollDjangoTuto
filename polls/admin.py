from django.contrib import admin
from .models import Question, Choice

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
            (None, {"fields":["pub_date"]}), 
            ("Date information",{"fields":["question_text"]}),
        ]
    inlines = [ChoiceInline]
    list_filter = ["pub_date"]
    search_fields = ["question_text"]
    list_display = ["question_text", "pub_date","was_published_recently"]


admin.site.register(Question, QuestionAdmin)

# Register your models here.
