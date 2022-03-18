from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

from users.forms import UserChangeForm, UserCreationForm

User = get_user_model()

@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    def mark_premium(modeladmin, request, queryset):
        for user in queryset:
            user.is_premium = True
            user.save()

    mark_premium.short_description = 'Mark User Premium'

    def mark_flaged(modeladmin, request, queryset):
        for user in queryset:
            user.is_flaged = True
            user.save()

    mark_flaged.short_description = 'Mark User Flaged'

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (("User", {"fields": ("name",)}),) + auth_admin.UserAdmin.fieldsets
    search_fields = ["name"]
    actions = [mark_premium, mark_flaged]

    list_display = ('username', 'email', 'name', 'is_staff', 'is_subscribe', 'is_superuser' )
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'is_subscribe', 'is_premium', 'is_flaged')

