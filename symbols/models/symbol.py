from django.db import models

from utility.models import UpdateHistoryModel


class Symbol(UpdateHistoryModel):
    symbol = models.CharField(max_length=255, verbose_name='نماد', unique=True)

    open = models.PositiveIntegerField(verbose_name='اولین')
    high = models.PositiveIntegerField(verbose_name='بیشترین')
    low = models.PositiveIntegerField(verbose_name='کمترین')
    adj_close = models.PositiveIntegerField(verbose_name='پایانی')

    value = models.PositiveBigIntegerField(verbose_name='ارزش معاملات')
    volume = models.PositiveBigIntegerField(verbose_name='حجم معاملات')
    count = models.PositiveBigIntegerField(verbose_name='تعداد معاملات')

    class Meta:
        verbose_name = 'نماد'
        verbose_name_plural = 'نماد ها'

