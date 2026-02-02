# test_connection.py

from src.oanda_api import OandaAPI
import os


def main():
    """Test the OANDA API connection and data retrieval."""

    print("=" * 50)
    print("OANDA API CONNECTION TEST")
    print("=" * 50)

    # Step 1: Create an instance of the API class
    print("\n1. Initializing OANDA API...")
    api = OandaAPI()

    # Step 2: Test the connection
    print("\n2. Testing connection...")
    if api.test_connection():
        print("✅ Connection successful!")
    else:
        print("❌ Connection failed!")
        return

    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)

    # Step 3: Fetch and save EUR/USD data
    print("\n3. Fetching EUR/USD data (1H, 500 candles)...")
    df_eur = api.get_candles('EUR_USD', granularity='H1', count=500)

    if df_eur is not None:
        print(f"✅ Retrieved {len(df_eur)} candles")
        # Save to CSV
        df_eur.to_csv('data/eur_usd_1h.csv', index=False)
        print(f"💾 Saved to data/eur_usd_1h.csv")
        print("\nFirst 5 rows:")
        print(df_eur.head())
        print("\nLast 5 rows:")
        print(df_eur.tail())
    else:
        print("❌ Failed to retrieve EUR/USD data")
        return

    # Step 4: Fetch and save USD/JPY data
    print("\n4. Fetching USD/JPY data (4H, 500 candles)...")
    df_jpy = api.get_candles('USD_JPY', granularity='H4', count=500)

    if df_jpy is not None:
        print(f"✅ Retrieved {len(df_jpy)} candles")
        # Save to CSV
        df_jpy.to_csv('data/usd_jpy_4h.csv', index=False)
        print(f"💾 Saved to data/usd_jpy_4h.csv")
        print("\nFirst 5 rows:")
        print(df_jpy.head())
    else:
        print("❌ Failed to retrieve USD/JPY data")

    # Step 5: Fetch and save Bitcoin data
    print("\n5. Fetching BTC/USD data (Daily, 365 candles)...")
    df_btc = api.get_candles('BTC_USD', granularity='D', count=365)

    if df_btc is not None:
        print(f"✅ Retrieved {len(df_btc)} candles")
        # Save to CSV
        df_btc.to_csv('data/btc_usd_daily.csv', index=False)
        print(f"💾 Saved to data/btc_usd_daily.csv")
        print("\nFirst 5 rows:")
        print(df_btc.head())
        print("\nBasic statistics:")
        print(df_btc[['open', 'high', 'low', 'close']].describe())
    else:
        print("❌ Failed to retrieve BTC data")

    # Summary
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    print(f"✅ EUR/USD: {len(df_eur) if df_eur is not None else 0} rows")
    print(f"✅ USD/JPY: {len(df_jpy) if df_jpy is not None else 0} rows")
    print(f"✅ BTC/USD: {len(df_btc) if df_btc is not None else 0} rows")
    print(f"📊 Total rows: {(len(df_eur) if df_eur is not None else 0) + (len(df_jpy) if df_jpy is not None else 0) + (len(df_btc) if df_btc is not None else 0)}")
    print("=" * 50)


if __name__ == "__main__":
    main()
