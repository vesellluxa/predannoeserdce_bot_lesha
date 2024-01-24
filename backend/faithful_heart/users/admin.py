from django.contrib import admin
from django.contrib.auth.models import Group
from rest_framework_simplejwt.tokens import BlacklistedToken, OutstandingToken

from users.models import TelegramUser, User

admin.site.unregister(OutstandingToken)
admin.site.unregister(BlacklistedToken)
admin.site.unregister(Group)


class TelegramUserAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "username",
        "email",
        "name",
        "surname",
        "middle_name",
        "phone_number",
        "chat_id",
    )
    list_display_links = (
        "username",
        "email",
        "name",
    )
    list_filter = ("chat_id",)
    search_fields = ("username", "surname", "email", "phone_number")


class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "first_name", "last_name", "telegram_username")


admin.site.register(TelegramUser, TelegramUserAdmin)
admin.site.register(User, UserAdmin)
