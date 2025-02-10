from django.db import models


class UserProfile(models.Model):
    """Профиль пользователя"""
    user_id = models.BigIntegerField(unique=True, db_index=True, verbose_name="ID пользователя в Telegram")
    username = models.CharField(max_length=255, null=True, blank=True, verbose_name="Имя пользователя")
    phone_number = models.CharField(max_length=20, null=True, blank=True, verbose_name="Номер телефона")
    registration_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации игрока")
    lvl = models.IntegerField(default=1, verbose_name="Уровень игрока")
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=100000.00, verbose_name='Баланс пользователя')
    pay_comfort = models.BooleanField(default=False, verbose_name='Оплачен тариф комфорт')
    pay_premium = models.BooleanField(default=False, verbose_name='Оплачен тариф премиум')
    pay_exclusive = models.BooleanField(default=False, verbose_name='Оплачен тариф эксклюзив')

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        if self.username:
            return f"{self.user_id} ({self.username})"
        return self.user_id


# Модель уровня матрицы
class MatrixLevel(models.Model):
    """Модель уровня матрицы"""
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='matrix_levels',
                              verbose_name='Владелец матрицы', db_index=True)
    level = models.IntegerField(verbose_name='Уровень матрицы')
    max_positions = models.IntegerField(verbose_name='Максимальное количество людей в уровне')
    is_full = models.BooleanField(default=False, verbose_name='Заполнена ли матрица')

    class Meta:
        verbose_name = "Матрица пользователя"
        verbose_name_plural = "Матрицы пользователя"

    def __str__(self):
        owner_info = f"{self.owner.user_id}"
        if self.owner.username:
            owner_info += f" - {self.owner.username}"
        return f"Матрица уровня {self.level} (Владелец: {owner_info})"


class MatrixPosition(models.Model):
    """Позиция пользователя в матрице"""
    level = models.ForeignKey(MatrixLevel, on_delete=models.CASCADE, related_name='positions',
                              verbose_name='Матрица и её владелец', db_index=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='Пользователи уровня', db_index=True)
    position = models.IntegerField(verbose_name='Позиция пользователя в уровне')

    class Meta:
        verbose_name = "Матрица с рефералами"
        verbose_name_plural = "Матрицы с рефералами"
        unique_together = ('level', 'position')  # Уникальная связка уровень + позиция
        indexes = [
            models.Index(fields=['level']),  # Индекс для поиска по уровню
            models.Index(fields=['user']),  # Индекс для поиска по пользователю
            models.Index(fields=['level', 'position']),  # Составной индекс для поиска по уровню и позиции
        ]


class Referral(models.Model):
    """Модель реферальной системы"""
    referrer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='referrals_made',
                                 verbose_name="Пригласивший")
    referred_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='referred_by',
                                      verbose_name="Приглашённый пользователь ")

    class Meta:
        verbose_name = "Реферальная система"
        verbose_name_plural = "Реферальная системы"
