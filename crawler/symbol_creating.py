from pytse_client import symbols_data

from crawler.exceptions import TSECrawlException
from symbols.models import Symbol


def add_new_symbols():
    try:
        symbol_names = symbols_data.all_symbols()
    except:
        raise TSECrawlException('دریافت اطلاعات با مشکل رو به رو شد! پس از مدتی دوباره تلاش کنید.')

    symbols = []
    for symbol in symbol_names:
        if not Symbol.objects.filter(symbol=symbol).count():
            symbols.append(Symbol.objects.create(symbol=symbol))
    return symbols
