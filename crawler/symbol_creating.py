from pytse_client import symbols_data

from symbols.models import Symbol


def add_new_symbols():
    symbol_names = symbols_data.all_symbols()
    symbols = []
    for symbol in symbol_names:
        if not Symbol.objects.filter(symbol=symbol).count():
            symbols.append(Symbol.objects.create(symbol=symbol))
    return symbols
