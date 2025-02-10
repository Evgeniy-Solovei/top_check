from django.contrib import admin

from top_check_core.models import UserProfile, Referral, MatrixLevel, MatrixPosition


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Регистрация в админ панели модели UserProfile."""
    list_display = ['id', 'user_id', 'username', 'phone_number', 'registration_date', 'balance', 'lvl', 'pay_comfort',
                    'pay_premium', 'pay_exclusive']


@admin.register(MatrixLevel)
class MatrixLevelAdmin(admin.ModelAdmin):
    """Регистрация в админ панели модели MatrixLevel."""
    list_display = ['id', 'get_owner', 'level', 'max_positions', 'is_full', 'view_positions']
    list_filter = ['owner', 'level']

    def get_owner(self, obj):
        return f"{obj.owner.user_id} - {obj.owner.username}"
    get_owner.short_description = 'Владелец матрицы'

    def view_positions(self, obj):
        from django.urls import reverse
        from django.utils.html import format_html
        url = reverse('admin:top_check_core_matrixposition_changelist') + f'?level__id={obj.id}'
        return format_html('<a href="{}">Позиции в матрице</a>', url)
    view_positions.short_description = 'Позиции в матрице'


@admin.register(MatrixPosition)
class MatrixPositionAdmin(admin.ModelAdmin):
    """Регистрация в админ панели модели MatrixPosition."""
    list_display = ['id', 'get_owner', 'get_user', 'position']
    list_filter = ['level__owner', 'level__level']

    def get_owner(self, obj):
        return f"{obj.level.owner.user_id} - {obj.level.owner.username}"
    get_owner.short_description = 'Владелец матрицы'

    def get_user(self, obj):
        return f"{obj.user.user_id} - {obj.user.username}"
    get_user.short_description = 'Пользователь'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('level__owner', 'user')


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_referrer', 'get_referred_user']

    def get_referrer(self, obj):
        return str(obj.referrer)
    get_referrer.short_description = 'Реферал'

    def get_referred_user(self, obj):
        return str(obj.referred_user)
    get_referred_user.short_description = 'Новый игрок'

