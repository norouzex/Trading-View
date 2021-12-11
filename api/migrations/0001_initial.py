# Generated by Django 3.2.9 on 2021-12-11 10:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Coin_list',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coin', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Paper_trading',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enter_balance', models.FloatField()),
                ('balance', models.FloatField()),
                ('enter_date', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='paper_trading', to=settings.AUTH_USER_MODEL, verbose_name='paper trading')),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trade_type', models.CharField(choices=[('b', 'Buy'), ('s', 'Sell')], max_length=1, verbose_name='type')),
                ('entert_price', models.FloatField()),
                ('amount', models.FloatField(verbose_name='token amount')),
                ('status', models.CharField(choices=[('w', 'Working'), ('d', 'Done'), ('c', 'close')], max_length=1, verbose_name='trade status')),
                ('oreder_set_date', models.DateTimeField(auto_now_add=True)),
                ('oreder_reach_date', models.DateTimeField(blank=True, null=True)),
                ('coin1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coin1', to='api.coin_list')),
                ('coin2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coin2', to='api.coin_list')),
                ('paper_trading', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='position', to='api.paper_trading', verbose_name='position')),
            ],
        ),
        migrations.CreateModel(
            name='Position_option',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(verbose_name='token amount')),
                ('status', models.CharField(choices=[('t', 'Take Profit'), ('s', 'Stop loss'), ('w', 'Working')], max_length=1, verbose_name='trade status')),
                ('stoploss', models.FloatField(blank=True, null=True)),
                ('take_profit', models.FloatField(blank=True, null=True)),
                ('oreder_reach_date', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('in_position', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='in_position', to='api.position', verbose_name='in_position')),
            ],
        ),
    ]
