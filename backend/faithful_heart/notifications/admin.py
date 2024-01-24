from django.contrib import admin

from notifications.models import TelegramNewsletter


class TelegramNewsletterAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'is_finished',
        'sending_date'
    )
    list_display_links = ('text',)


admin.site.register(TelegramNewsletter, TelegramNewsletterAdmin)
