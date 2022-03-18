from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

from users.forms import UserChangeForm, UserCreationForm
from users.models import Subscription

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

class SubscriptionAdmin(admin.ModelAdmin):

    def turn_subscription_on_off(modeladmin, request, queryset):
        for subscription in queryset:
            if subscription.is_active:
                subscription.is_active = False
                subscription.save()
            else:
                subscription.is_active = True
                subscription.save()

    turn_subscription_on_off.short_description = 'Turn subscription on/off'

    model = Subscription
    search_fields = ["name"]
    list_display = ['name', 'price', 'number_of_alerts', 'is_active']
    list_filter = ('is_active', 'price')

    actions = [turn_subscription_on_off]


admin.site.register(Subscription, SubscriptionAdmin)