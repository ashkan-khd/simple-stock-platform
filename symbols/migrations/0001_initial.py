# Generated by Django 3.1.7 on 2021-03-03 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Symbol',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('symbol', models.CharField(max_length=255, unique=True, verbose_name='نماد')),
                ('open', models.PositiveIntegerField(verbose_name='اولین')),
                ('high', models.PositiveIntegerField(verbose_name='بیشترین')),
                ('low', models.PositiveIntegerField(verbose_name='کمترین')),
                ('adj_close', models.PositiveIntegerField(verbose_name='پایانی')),
                ('value', models.PositiveBigIntegerField(verbose_name='ارزش معاملات')),
                ('volume', models.PositiveBigIntegerField(verbose_name='حجم معاملات')),
                ('count', models.PositiveBigIntegerField(verbose_name='تعداد معاملات')),
            ],
            options={
                'verbose_name': 'نماد',
                'verbose_name_plural': 'نماد ها',
            },
        ),
    ]
