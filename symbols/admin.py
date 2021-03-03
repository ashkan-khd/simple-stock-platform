from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.conf.urls import url

from symbols.models import Symbol
from utility.add_symbols import check_updated_symbols_existence


@staff_member_required
def export(request):
    check_updated_symbols_existence()
    return HttpResponseRedirect(request.META["HTTP_REFERER"])

@admin.register(Symbol)
class SymbolAdmin(admin.ModelAdmin):
    fields = [
        'symbol',
        'open',
        'high',
        'low',
        'adj_close',
        'value',
        'volume',
        'count',
        'updated'
    ]

    readonly_fields = ['updated']

    list_display = fields

    def get_urls(self):
        urls = super(SymbolAdmin, self).get_urls()
        my_urls = [url(r"^export/$", export), ]
        return my_urls + urls

    class Meta:
        model = Symbol
