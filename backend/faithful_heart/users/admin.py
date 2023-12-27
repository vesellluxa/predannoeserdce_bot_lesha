from django.contrib import admin

from users.models import TelegramUser, User


class TelegramUserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'email',
        'name',
        'second_name',
        'surname',
        'phone_number',
        'chat_id'
    )
    list_display_links = ('username', 'email', 'name',)
    list_filter = ('chat_id',)
    search_fields = ('username', 'surname', 'email',  'phone_number')


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'chat_id'
    )


admin.site.register(TelegramUser, TelegramUserAdmin)
admin.site.register(User, UserAdmin)
