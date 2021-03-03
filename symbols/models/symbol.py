from django.db import models

from utility.models import null_blank, BaseHistoryModel


class Symbol(BaseHistoryModel):
    symbol = models.CharField(max_length=255, verbose_name='نماد', unique=True)
    company_name = models.CharField(max_length=255, verbose_name='نام شرکت', **null_blank())
    url = models.URLField(verbose_name='آدرس صفحه سهم', **null_blank())

    eps = models.IntegerField(verbose_name='eps', **null_blank())
    p_e_ratio = models.FloatField(verbose_name='P/E', **null_blank())
    group_p_e_ratio = models.FloatField(verbose_name='Group P/E', **null_blank())

    open = models.PositiveIntegerField(verbose_name='اولین', **null_blank())
    high = models.PositiveIntegerField(verbose_name='بیشترین', **null_blank())
    low = models.PositiveIntegerField(verbose_name='کمترین', **null_blank())
    adj_close = models.PositiveIntegerField(verbose_name='پایانی', **null_blank())
    close = models.PositiveIntegerField(verbose_name='آخرین معامله', **null_blank())

    value = models.PositiveBigIntegerField(verbose_name='ارزش معاملات', **null_blank())
    volume = models.PositiveBigIntegerField(verbose_name='حجم معاملات', **null_blank())
    count = models.PositiveBigIntegerField(verbose_name='تعداد معاملات', **null_blank())

    class Meta:
        verbose_name = 'نماد'
        verbose_name_plural = 'نماد ها'

