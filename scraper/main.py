# This is a sample Python script.
import time
import sqlite3
import sys

from marketdata.nasdaq import Nasdaq
from marketdata.snapshot import Snapshot


def get_nasdaq_topN(topN, db_file):
    nasdaq = Nasdaq(False)
    symbol_list = nasdaq.get_symbol_list()

    # get top 10 last sale symbols
    symbol_list.sort(key=lambda x: x['market_cap'], reverse=True)
    symbol_list = symbol_list[:topN]

    conn = sqlite3.connect(db_file)
    Snapshot.create_table(conn)

    while True:
        for symbol in symbol_list:
            snapshot = nasdaq.get_one_symbol(symbol['symbol'])
            if snapshot is None:
                continue
            print(snapshot)
            snapshot.update_or_insert(conn)
        time.sleep(1)

    conn.close()

if __name__ == '__main__':
    get_nasdaq_topN(10, sys.argv[1])

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
