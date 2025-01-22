from django.contrib import admin

from top_check_core.models import UserProfile, Referral


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Регистрация в админ панели модели UserProfile."""
    list_display = ['id', 'user_id', 'username', 'phone_number', 'registration_date', 'lvl']


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_referrer', 'get_referred_user']

    def get_referrer(self, obj):
        return str(obj.referrer)
    get_referrer.short_description = 'Реферал'

    def get_referred_user(self, obj):
        return str(obj.referred_user)
    get_referred_user.short_description = 'Новый игрок'

