from django.contrib import admin

from questions.models import (FrequentlyAskedQuestion, UniqueQuestion)


class FrequentlyAskedQuestionAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'text',
        'answer',
        'category',
        'is_relevant'
    )
    list_display_links = ('text', 'answer')
    search_fields = ('text', 'answer')
    list_editable = ('category', 'is_relevant')


class UniqueQuestionAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'text',
        'owner',
        'answer'
    )
    list_display_links = ('text', 'owner', 'answer')
    search_fields = ('text', 'answer')


admin.site.register(FrequentlyAskedQuestion, FrequentlyAskedQuestionAdmin)
admin.site.register(UniqueQuestion, UniqueQuestionAdmin)
