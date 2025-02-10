# Generated by Django 5.1.5 on 2025-02-01 23:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('top_check_core', '0002_userprofile_lvl_userprofile_registration_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user_id',
            field=models.BigIntegerField(db_index=True, unique=True, verbose_name='ID пользователя в Telegram'),
        ),
        migrations.CreateModel(
            name='MatrixLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.IntegerField(verbose_name='Уровень матрицы')),
                ('max_positions', models.IntegerField(verbose_name='Максимальное количество людей в уровне')),
                ('is_full', models.BooleanField(default=False, verbose_name='Заполнена ли матрица')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matrix_levels', to='top_check_core.userprofile', verbose_name='Владелец матрицы')),
            ],
        ),
        migrations.CreateModel(
            name='MatrixPosition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField(verbose_name='Позиция пользователя в уровне')),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='positions', to='top_check_core.matrixlevel', verbose_name='Матрица и её владелец')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='top_check_core.userprofile', verbose_name='Пользователи уровня')),
            ],
            options={
                'indexes': [models.Index(fields=['level'], name='top_check_c_level_i_9e11c6_idx'), models.Index(fields=['user'], name='top_check_c_user_id_765232_idx'), models.Index(fields=['level', 'position'], name='top_check_c_level_i_d14c20_idx')],
                'unique_together': {('level', 'position')},
            },
        ),
    ]
