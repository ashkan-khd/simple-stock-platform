from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.shortcuts import resolve_url
from django.views.generic import RedirectView
from rest_framework.generics import get_object_or_404

from crawler import TSECrawlException, update_symbol
from symbols.models import Symbol


class SymbolUpdateRedirectView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        symbol = get_object_or_404(Symbol, id=kwargs['pk'])
        url = resolve_url(admin_urlname(symbol.__class__._meta, 'change'), symbol.id)
        try:
            update_symbol(symbol)
        except TSECrawlException as e:
            pass
        return url
