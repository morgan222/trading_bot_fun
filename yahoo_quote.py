from collections import defaultdict
import csv

import pandas.compat as compat
from pandas import DataFrame


from pandas_datareader.base import _BaseReader

_yahoo_codes ={
    'symbol': 's', #sybol code is needed for the pandas_datareader code
    #'Name':'n',
    'Stock Exchange':'x',
    'Market Capitalisation':'j1',
    'Float Shares':'f6',
    'Book Value':'b4',
    #'Ask':'a',
    #'Bid':'b',
    #'Ask Size':'a5',
    #'Bid Size':'b6',
    'Last trade Date':'d1',
    'Last trade Time':'t1',
    'Last trade Price':'l1',
    'Last trade Size':'k3',
    'Change':'c1',
    'Change in Percent':'p2',
    'Open':'o',
    'Day High':'h',
    'Day Low':'g',
    'Day Range':'m',
    'Volume':'v',
    'Average Daily Volume':'a2',
    'Previous Close':'p',
    #'52-week Range':'w',
    #'52-week High':'k',
    #'52-week Low':'j',
    #'Change From 52-week High':'k4',
    #'Change From 52-week Low':'j5',
    #'% Change From 52-week High':'k5',
    #'% Change From 52-week Low':'j6',
    'Earnings/Share':'e',
    'EBITDA':'j4',
    'P/E Ratio':'r',
    'PEG Ratio':'r5',
    'Dividend/Share':'d',
    'Ex-Dividend Date':'q',
    'Dividend Pay Date':'r1',
    'Dividend Yield':'y',
    '1 yr Target Price':'t8',
    #'50-day Moving Average':'m3',
    #'200-day Moving Average':'m4',
    # 'Change From 200-day Moving Average':'m5',
    # 'Percent Change From 200-day Moving Average':'m6',
    # 'Change From 50-day Moving Average':'m7',
    # 'Percent Change From 50-day Moving Average':'m8'
}

class YahooQuotesReader(_BaseReader):

    """Get current yahoo quote"""
    @property
    def url(self):
        return 'http://finance.yahoo.com/d/quotes.csv'

    @property
    def params(self):
        if isinstance(self.symbols, compat.string_types):
            sym_list = self.symbols
        else:
            sym_list = '+'.join(self.symbols)
        # for codes see: http://www.gummy-stuff.org/Yahoo-data.htm
        request = ''.join(compat.itervalues(_yahoo_codes))  # code request string
        params = {'s': sym_list, 'f': request}
        return params

    def _read_lines(self, out):
        data = defaultdict(list)
        header = list(_yahoo_codes.keys())

        for line in csv.reader(out.readlines()):
            for i, field in enumerate(line):
                if field[-2:] == '%"':
                    v = float(field.strip('"%'))
                elif field[0] == '"':
                    v = field.strip('"')
                else:
                    try:
                        v = float(field)
                    except ValueError:
                        v = field
                data[header[i]].append(v)

        idx = data.pop('symbol')
        return DataFrame(data, index=idx)


def get_yahoo_stats(*args, **kwargs):
    return YahooQuotesReader(*args, **kwargs).read()


