import pytse_client

from crawler.exceptions import TSECrawlException


def update_symbol(symbol):
    try:
        ticker = pytse_client.Ticker(symbol.symbol)
        symbol.company_name = ticker.title
        symbol.url = ticker.url
        symbol.index = ticker.index
        symbol.eps = ticker.eps
        symbol.p_e_ratio = ticker.p_e_ratio
        symbol.group_p_e_ratio = ticker.group_p_e_ratio
        symbol.save()
        try:
            history_df = ticker.history
            data_list = history_df.iloc[[len(history_df) - 1]].values.flatten().tolist()
            symbol.open = data_list[0]
            symbol.high = data_list[1]
            symbol.low = data_list[2]
            symbol.adj_close = data_list[3]
            symbol.value = data_list[4]
            symbol.volume = data_list[5]
            symbol.count = data_list[6]
            symbol.close = data_list[7]
            symbol.save()
        except:
            raise TSECrawlException('دریافت اطلاعات ناقص ماند! پس از مدتی دوباره تلاش کنید.')

    except:
        raise TSECrawlException(
            'کرال اطلاعات با مشکل رو به رو شد!'
            'از صحت وجود نماد اطمینان حاصل کنید سپس بعد از مدتی دوباره تلاش کنید.'
        )
