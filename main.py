from mean_reversion import MeanReversion
from binance.client import Client
import pprint
import pandas as pd
import ccxt


def ccxt_test():
    print(ccxt.exchanges)

def unit_test():
    # tickers = ['ENJUSDT', 'MATICUSDT',
    #            'AVAXUSDT', 'TRXUSDT', 'BTCUSDT',
    #            'ETHUSDT', 'BNBUSDT', 'XRPUSDT', 'FTMUSDT', 'ADAUSDT', 'DOTUSDT',
    #            'DOGEUSDT', 'SHIBUSDT', 'SANDUSDT', 'MANAUSDT']
    tickers = ['QNTUSDT']

    # windows = [Client.KLINE_INTERVAL_3MINUTE, Client.KLINE_INTERVAL_5MINUTE,
    #            Client.KLINE_INTERVAL_15MINUTE, Client.KLINE_INTERVAL_30MINUTE,
    #            Client.KLINE_INTERVAL_1HOUR, Client.KLINE_INTERVAL_2HOUR, Client.KLINE_INTERVAL_4HOUR]
    windows = [Client.KLINE_INTERVAL_3MINUTE, Client.KLINE_INTERVAL_5MINUTE,
               Client.KLINE_INTERVAL_15MINUTE, Client.KLINE_INTERVAL_30MINUTE]

    rsi_lengths = [5, 8, 13, 20]
    pnl = dict()

    for ticker in tickers:
        for length in rsi_lengths:
            ticker_pnl = []
            for window in windows:
                inst = MeanReversion(ticker, window=window, rsi=length)
                profit = round(inst.cumulative_profit, 4)
                ticker_pnl.append(profit)
            pnl[ticker+str(length)] = ticker_pnl
    # df_pnl = pd.DataFrame.from_dict(pnl, orient='index', columns=['3m','5m','15m','30m','1h','2h','4h'])
    # df_pnl = df_pnl.sort_values(by=['3m','5m','15m','30m','1h','2h','4h'], ascending=False)
    df_pnl = pd.DataFrame.from_dict(pnl, orient='index', columns=['3m', '5m', '15m','30m'])
    df_pnl = df_pnl.sort_values(by=['3m', '5m', '15m','30m'], ascending=False)
    print(df_pnl)

if __name__ == '__main__':
    unit_test()
    #ccxt_test()




