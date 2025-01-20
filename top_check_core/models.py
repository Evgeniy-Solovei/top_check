from django.db import models


class UserProfile(models.Model):
    """Профиль пользователя"""
    user_id = models.BigIntegerField(unique=True, verbose_name="ID пользователя в Telegram")
    username = models.CharField(max_length=255, null=True, blank=True, verbose_name="Имя пользователя")
    phone_number = models.CharField(max_length=20, null=True, blank=True, verbose_name="Номер телефона")

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        if self.username:
            return f"{self.user_id} ({self.username})"
        return self.user_id


class Referral(models.Model):
    """Модель реферальной системы"""
    referrer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='referrals_made',
                                 verbose_name="Реферал")
    referred_user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='referred_by',
                                         verbose_name="Новый игрок")

    class Meta:
        verbose_name = "Реферальная система"
        verbose_name_plural = "Реферальная системы"
