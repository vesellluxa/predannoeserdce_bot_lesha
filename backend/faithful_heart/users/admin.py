from django.contrib import admin

from users.models import TelegramUser, User

from rest_framework_simplejwt.tokens import OutstandingToken, BlacklistedToken
from django.contrib.auth.models import Group

admin.site.unregister(OutstandingToken)
admin.site.unregister(BlacklistedToken)
admin.site.unregister(Group)


class TelegramUserAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "username",
        "email",
        "name",
        "second_name",
        "surname",
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
    list_display = ("pk",)


admin.site.register(TelegramUser, TelegramUserAdmin)
admin.site.register(User, UserAdmin)
