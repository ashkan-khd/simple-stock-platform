from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import admin
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.conf.urls import url
from django.shortcuts import resolve_url
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html
from jalali_date import datetime2jalali

from crawler import TSECrawlException, update_symbol
from symbols.models import Symbol
from crawler.symbol_creating import add_new_symbols


@staff_member_required
def export(request):
    add_new_symbols()
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


@admin.register(Symbol)
class SymbolAdmin(admin.ModelAdmin):
    list_per_page = 25

    search_fields = (
        'symbol',
        'index',
        'company_name',
        'group_name'
    )

    fieldsets = (
        (
            None, {
                'fields': (
                    'index',
                    'symbol',
                    'company_name',
                    'group_name',
                    'open_url',
                    'update_symbol',
                )
            },
        ),
        (
            'وضعیت سهام', {
                'fields': (
                    'eps',
                    'get_p_e_ratio',
                    'get_group_p_e_ratio'
                )
            }
        ),
        (
            'تاریخ ها', {
                'fields': (
                    'get_created',
                    'get_updated'
                )
            }
        ),
        (
            'ارزش ها', {
                'fields': (
                    'open',
                    'high',
                    'low',
                    'adj_close',
                    'value',
                    'volume',
                    'count'
                )
            }
        )
    )

    def get_readonly_fields(self, request, obj=None):
        fieldsets = self.get_fieldsets(request, obj)
        readonly_fields = []
        for fieldset in fieldsets:
            readonly_fields.extend(fieldset[1]['fields'])
        return readonly_fields

    list_display = [
        'symbol',
        'open',
        'high',
        'low',
        'adj_close',
        'value',
        'volume',
        'count',
        'eps',
        'get_p_e_ratio',
        'get_updated'
    ]

    actions = [
        'update_symbols'
    ]

    def get_created(self, obj):
        return datetime2jalali(obj.created).strftime('%Y/%m/%d - %H:%m:%S')

    get_created.short_description = 'تاریخ اضافه شدن'
    get_created.admin_order_field = 'created'

    def get_updated(self, obj):
        if obj.updated - obj.created < timezone.timedelta(seconds=0.5):
            return 'تا کنون آپدیت نشده است!'
        return datetime2jalali(obj.updated).strftime('%Y/%m/%d - %H:%m:%S')

    get_updated.short_description = 'آخرین زمان آپدیت'
    get_updated.admin_order_field = 'updated'

    def get_p_e_ratio(self, obj):
        if not obj.p_e_ratio:
            return '-'
        return "% {:.3f}".format(obj.p_e_ratio)

    get_p_e_ratio.short_description = 'P/E'
    get_p_e_ratio.admin_order_field = 'p_e_ratio'

    def get_group_p_e_ratio(self, obj):
        if not obj.group_p_e_ratio:
            return '-'
        return "% {:.3f}".format(obj.group_p_e_ratio)

    get_group_p_e_ratio.short_description = 'Group P/E'
    get_group_p_e_ratio.admin_order_field = 'group_p_e_ratio'

    def open_url(self, obj):
        if not obj.url:
            return '-'
        return format_html(
            '<a '
            'href={} role="button" '
            'style="color:#fff;background-color:#4caf50;border-color:#235025;padding: 10px;border-radius: 8px;">'
            'باز کردن'
            '</a>'.format(obj.url)
        )

    open_url.short_description = 'لینک صفحه نماد'

    def update_symbol(self, obj):
        url = reverse('admin-symbol-update', kwargs={'pk': obj.id})
        return format_html(
            '<a '
            'href={} role="button" '
            'style="color:#fff;background-color:#337ab7;border-color:#2e6da4;padding: 10px;border-radius: 8px;">'
            'آپدیت کردن اطلاعات'
            '</a>'.format(url)
        )

    update_symbol.short_description = 'آپدیت کردن اطلاعات'

    def update_symbols(self, request, queryset):
        if queryset.count() > 10:
            messages.error(request, 'قابلیت آپدیت کردن بیش از ۱۰ نماد بصورت همزمان را ندارید!')
            return
        for symbol in queryset:
            try:
                update_symbol(symbol)
            except TSECrawlException as e:
                messages.error(request, str(symbol) + ': ' + str(e))

    update_symbols.short_description = 'آپدیت نماد های انتخاب شده'

    def get_urls(self):
        urls = super(SymbolAdmin, self).get_urls()
        my_urls = [url(r"^export/$", export), ]
        return my_urls + urls

    def has_add_permission(self, request):
        return False

    class Meta:
        model = Symbol
