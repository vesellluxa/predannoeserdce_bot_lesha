from django.contrib import admin

from users.models import TelegramUser, User


class TelegramUserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'email',
        'name',
        'surname',
        'phone',
        'chat_id'
    )
    list_display_links = ('username', 'email', 'name',)
    list_filter = ('chat_id',)
    search_fields = ('username', 'surname', 'email', 'phone')


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'chat_id'
    )


admin.site.register(TelegramUser, TelegramUserAdmin)
admin.site.register(User, UserAdmin)
