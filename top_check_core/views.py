from decimal import Decimal

from top_check_core.models import MatrixLevel, MatrixPosition, Referral, UserProfile


async def create_matrix(user):
    """
    Создает пустую матрицу для нового пользователя.
    Матрица состоит из 12 уровней, каждый уровень изначально пуст.
    """
    for level in range(1, 13):  # Создаем 12 уровней
        max_positions = 3 ** level  # Максимальное количество пользователей на уровне
        await MatrixLevel.objects.acreate(owner=user, level=level, max_positions=max_positions, is_full=False)


async def add_user_to_matrix(new_user, referrer):
    """
    Добавляет пользователя в матрицу реферера и всех вышестоящих участников.
    """
    # Создаем список referrers, который будет содержать цепочку рефереров.
    # Начинаем с нового пользователя и его реферера.
    referrers = [new_user, referrer]
    # Получаем всю цепочку рефереров вверх по матрице.
    while True:
        try:
            # Ищем запись в модели Referral, где referred_user равен текущему рефереру.
            # Используем select_related("referrer") для оптимизации запроса.
            referral = await Referral.objects.select_related("referrer").aget(referred_user=referrer)
            # Переходим к следующему рефереру по цепочке вверх.
            referrer = referral.referrer
            # Добавляем найденного реферера в список referrers.
            referrers.append(referrer)
        except Referral.DoesNotExist:
            # Если запись не найдена, значит, цепочка рефереров закончилась, и мы выходим из цикла.
            break
    # Выводим цепочку рефереров для отладки.
    print("Цепочка рефереров:", [user.user_id for user in referrers])
    # Начинаем с реферера и идем вверх по цепочке. enumerate(referrers[1:], start=1) позволяет нам пройтись
    # по всем реферерам, начиная с первого (исключая нового пользователя).
    for i, ref in enumerate(referrers[1:], start=1):
        # Уровень матрицы увеличивается с каждым шагом вверх по цепочке.
        matrix_level = i
        try:
            # Начинаем поиск свободного места в матрице с текущего уровня.
            current_level = matrix_level
            # Бесконечный цикл для поиска матрицы с свободными местами.
            while True:
                # Ищем матрицу на текущем уровне, которая еще не заполнена.
                level_matrix = await MatrixLevel.objects.filter(owner=ref, level=current_level, is_full=False).afirst()
                # Если нашли матрицу с свободными местами, выходим из цикла.
                if level_matrix:
                    print(
                        f"Найдена матрица уровня {current_level} с свободными местами для пользователя {ref.user_id}.")
                    break
                # Если матрица не найдена, переходим на следующий уровень.
                print(
                    f"Для пользователя {ref.user_id} нет свободных мест на уровне {current_level}, переходим на уровень {current_level + 1}.")
                current_level += 1
                # Если уровни закончились (достигнут максимальный уровень), завершаем процесс.
                if current_level > 12:  # 12 — максимальный уровень.
                    print(f"Для пользователя {ref.user_id} нет свободных мест ни на одном уровне.")
                    return
            # Проверяем, есть ли место в найденной матрице.
            positions = await MatrixPosition.objects.filter(level=level_matrix).acount()
            # Если есть свободные места, добавляем нового пользователя в матрицу.
            if positions < level_matrix.max_positions:
                await MatrixPosition.objects.acreate(level=level_matrix, user=new_user, position=positions + 1)
                # Если после добавления пользователя матрица заполнена, помечаем ее как заполненную.
                if positions + 1 == level_matrix.max_positions:
                    level_matrix.is_full = True
                    await level_matrix.asave()
                # Выводим сообщение об успешном добавлении пользователя.
                print(f"Пользователь {new_user.user_id} добавлен в матрицу уровня {matrix_level}, "
                      f"владелец матрицы — {ref.user_id}")
            else:
                # Если матрица уже заполнена, выводим сообщение.
                print(f"Матрица уровня {matrix_level} у {ref.user_id} уже заполнена.")
        except Exception as e:
            # Если произошла ошибка, выводим сообщение об ошибке.
            print(f"Ошибка при добавлении {new_user.user_id} в матрицу {ref.user_id}: {e}")


async def get_user_profile(user_id):
    """Получает профиль пользователя по user_id"""
    return await UserProfile.objects.filter(user_id=user_id).afirst()


async def process_subscription_payment(user_profile, price):
    """Обрабатывает списание средств за подписку"""
    if user_profile.balance >= price:
        # Если у пользователя достаточно средств
        user_profile.balance -= Decimal(price)
        await user_profile.asave()
        return True  # Оплата прошла успешно
    return False  # Недостаточно средств

# async def add_user_to_matrix(new_user, referrer):
#     """
#     Добавляет пользователя в матрицу реферера и всех вышестоящих участников.
#     """
#     referrers = [new_user, referrer]
#     # Получаем всю цепочку рефереров вверх по матрице
#     while True:
#         try:
#             referral = await Referral.objects.select_related("referrer").aget(referred_user=referrer)
#             referrer = referral.referrer
#             referrers.append(referrer)
#         except Referral.DoesNotExist:
#             break
#     print("Цепочка рефереров:", [user.user_id for user in referrers])
#
#     # Определяем уровни родителей
#     referrer_levels = {}
#     try:
#         level_new_user_in_matrix_referrer = await MatrixLevel.objects.filter(owner=referrer, is_full=False).afirst()
#         # Находим первую свободную позицию в этой матрице
#         positions = await MatrixPosition.objects.filter(level=level_new_user_in_matrix_referrer).acount()
#         if positions < level_new_user_in_matrix_referrer.max_positions:
#             # Создаём новую позицию для нового пользователя
#             new_position = MatrixPosition(level=level_new_user_in_matrix_referrer, user=new_user, position=positions + 1)
#             await new_position.asave()
#             # Проверяем, заполнена ли матрица
#             if positions + 1 == level_new_user_in_matrix_referrer.max_positions:
#                 level_new_user_in_matrix_referrer.is_full = True
#                 await level_new_user_in_matrix_referrer.asave()
#
#             print(f"Пользователь {new_user.user_id} добавлен в матрицу уровня {level_new_user_in_matrix_referrer.level}, "
#                   f"владелец матрицы — {referrer.user_id}")
#         else:
#             print(f"Матрица уровня {level_new_user_in_matrix_referrer.level} для пользователя {referrer.user_id} уже заполнена.")
#     except MatrixLevel.DoesNotExist:
#         print(f"Для пользователя {referrer.user_id} нет доступных матриц.")
#
#     for i in range(1, len(referrers) - 1):
#         current_referrer = referrers[i]
#         next_referrer = referrers[i + 1]  # Владелец матрицы
#         # Ищем позицию текущего реферера в матрице, владелец которой — следующий реферер
#         try:
#             matrix_position = await MatrixPosition.objects.select_related("level").aget(
#                                     user=current_referrer, level__owner=next_referrer)
#             # Получаем уровень матрицы
#             matrix_level = matrix_position.level.level
#             referrer_levels[current_referrer] = matrix_level
#             print(matrix_level)
#             print(f"Пользователь {current_referrer.user_id} находится в матрице уровня {matrix_level}, "
#                   f"владелец матрицы — {next_referrer.user_id}")
#         except MatrixPosition.DoesNotExist:
#             print(f"Пользователь {current_referrer.user_id} не находится в матрице, "
#                   f"владелец которой — {next_referrer.user_id}")
#         print("Словарь referrer_levels:")
#         for user, level in referrer_levels.items():
#             print(f"Пользователь {user.user_id}: уровень матрицы {level}")
