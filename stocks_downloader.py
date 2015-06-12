#!/usr/bin/env python
__author__ = "Oto Brglez <otobrglez@gmail.com>"

from requests import get
from urllib import urlencode
import argparse
import time
import csv
import sys


class YFStock(object):
    ticker = None
    granularity = "m"
    data = []

    def __init__(self, ticker, granularity="m"):
        self.ticker = ticker
        self.granularity = granularity

    def load(self, params={}):
        url_params = dict({'s': self.ticker}, **params)
        url = "http://ichart.finance.yahoo.com/table.csv?" + urlencode(url_params)
        data = get(url)
        self.data = [line.split(',') for line in data.text.strip().split('\n')]
        return self

    def __process_row(self, i, row):
        if i == 0:
            return ["Ticker", "Granularity",
                    # len(row)
                   ] + row

        return [self.ticker, self.granularity,
                # len(row)
               ] + row

    def toCSV(self, fileobj=sys.stdout):
        if self.data is []:
            raise Exception("Data is empty!")

        writer = csv.writer(fileobj, quotechar='"', quoting=csv.QUOTE_ALL)
        for i, row in enumerate([self.__process_row(j, jrow) for j, jrow in enumerate(self.data)]):
            writer.writerow(row)

        sys.stdout.flush()

    def __sql_insert(self, i, row):
        fields = "ticker,granularity,mdate,open,high,low,close,volume,adj_close"
        values = ",".join([("'%s'" % s) for s in ([self.ticker, self.granularity] + row)])
        return "INSERT INTO stocks (%s) VALUES (%s);" % (fields, values)

    def toSQL(self):
        if self.data is []:
            raise Exception("Data is empty!")

        for i, row in enumerate([self.__sql_insert(j, jrow) for j, jrow in enumerate(self.data)]):
            if i == 0:
                continue

            print row

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')

    parser.add_argument('ticker', metavar='ticker', type=str)

    start = [int(x) for x in time.strftime("%Y-01-01").split("-")]
    current = [int(x) for x in time.strftime("%Y-%m-%d").split("-")]

    ws_args = {
        'a': ["from month - 1", start[1] - 1],
        'b': ["from day (two digits)", start[2]],
        'c': ["from year", start[0]],
        'd': ["to month - 1", current[1] - 1],
        'e': ["to day (two digits)", current[2]],
        'f': ["to year", current[0]],
        'g': ['granularity (d for day, m for month, y for yearly)', "m"],
    }

    for key, desc in ws_args.iteritems():
        parser.add_argument("-" + key,
                            metavar=key,
                            default=desc[1],
                            help=desc[0])

    parser.add_argument("-x", metavar="x", default="csv", help="output format (csv or sql)")

    args = parser.parse_args()
    options = vars(args)

    s = YFStock(args.ticker, args.g).load(options)
    if options['x'] is "csv":
        s.toCSV()
    else:
        s.toSQL()