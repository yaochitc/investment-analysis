import os
import sys

import tushare as ts

def _cachpath(symbol, type_):
    return '-'.join((symbol.replace(os.path.sep, '_'), type_))

def tushare_bundle(
                   symbol,
                   start,
                   end
                   ):
    try:
        df = ts.get_h_data(
            symbol,
            start=start.strftime("%Y-%m-%d") if start != None else None,
            end=end.strftime("%Y-%m-%d") if end != None else None,
            # session=session,
        ).sort_index()
    except Exception:
        print('Got a Exception - for stock(%s) in tushare, ignore it' % (symbol))
        sys.exit(-1)

    new_index= ['open', 'high', 'low', 'close','volume']
    df.reindex(new_index,copy=False)
    return df
