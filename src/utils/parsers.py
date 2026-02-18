# src/utils/parser.py

import pandas as pd


def parse_candles(candles):
    data = []
    for candle in candles:
        data.append({
            'time': candle['time'],
            'open': float(candle['mid']['o']),
            'high': float(candle['mid']['h']),
            'low': float(candle['mid']['l']),
            'close': float(candle['mid']['c']),
            'volume': int(candle['volume'])
        })

    df = pd.DataFrame(data)
    df['time'] = pd.to_datetime(df['time'])
    return df
