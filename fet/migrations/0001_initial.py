# Generated by Django 2.2 on 2019-04-03 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ForeignCurrencyTrades',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.CharField(max_length=9, unique=True)),
                ('sell_currency', models.CharField(max_length=3)),
                ('sell_amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('buy_currency', models.CharField(max_length=3)),
                ('buy_amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('rate', models.DecimalField(decimal_places=20, max_digits=40)),
                ('date_booked', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
