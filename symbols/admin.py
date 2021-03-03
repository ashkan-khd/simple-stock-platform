from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.conf.urls import url
from django.shortcuts import resolve_url
from django.utils import timezone
from django.utils.html import format_html
from jalali_date import datetime2jalali

from symbols.models import Symbol
from crawler.symbol_creating import add_new_symbols


@staff_member_required
def export(request):
    add_new_symbols()
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


@admin.register(Symbol)
class SymbolAdmin(admin.ModelAdmin):
    symbol_fields = [
        'symbol',
        'open',
        'high',
        'low',
        'adj_close',
        'value',
        'volume',
        'count'
    ]

    fields = symbol_fields + [
        'get_created',
        'get_updated',
        'open_link'
    ]

    readonly_fields = fields

    list_display = symbol_fields + [
        'get_updated'
    ]

    def get_created(self, obj):
        return datetime2jalali(obj.updated).strftime('%Y/%m/%d - %H:%m:%S')

    get_created.short_description = 'تاریخ اضافه شدن'
    get_created.admin_order_field = 'created'

    def get_updated(self, obj):
        if obj.created - obj.updated < timezone.timedelta(seconds=1):
            return 'تا کنون آپدیت نشده است!'
        return datetime2jalali(obj.updated).strftime('%Y/%m/%d - %H:%m:%S')

    get_updated.short_description = 'آخرین زمان آپدیت'
    get_updated.admin_order_field = 'updated'

    def open_link(self, obj):
        url = resolve_url(admin_urlname(obj.__class__._meta, 'change'), obj.id)
        return format_html(
            '<a '
            'href={} role="button" '
            'style="color:#fff;background-color:#337ab7;border-color:#2e6da4;padding: 10px;border-radius: 8px;">'
            'باز کردن لینک'
            '</a>'.format(url)
        )

    open_link.short_description = 'آپدیت کردن اطلاعات'

    def get_urls(self):
        urls = super(SymbolAdmin, self).get_urls()
        my_urls = [url(r"^export/$", export), ]
        return my_urls + urls

    def has_add_permission(self, request):
        return False

    class Meta:
        model = Symbol
