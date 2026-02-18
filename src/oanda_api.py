# src/oanda_api.py

import os
import requests
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime

from src.utils.logger import setup_logger
from src.utils.parsers import parse_candles

load_dotenv()


class OandaAPI:

    def __init__(self):
        self.logger = setup_logger('OandaAPI')
        self.logger.info('API initialisation...')

        self.api_token = os.getenv('OANDA_API_TOKEN')
        self.account_id = os.getenv('OANDA_ACCOUNT_ID')
        self.base_url = os.getenv('OANDA_BASE_URL')

        # Set up request headers for authentication
        self.headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json'
        }

        # Validate credentials on initialization
        self._validate_credentials()

    def _validate_credentials(self):
        if not self.api_token:
            raise ValueError(
                "OANDA_API_TOKEN not found in environment variables")
        if not self.account_id:
            raise ValueError(
                "OANDA_ACCOUNT_ID not found in environment variables")
        if not self.base_url:
            raise ValueError(
                "OANDA_BASE_URL not found in environment variables")

        self.logger.info("Credentials validated successfully")

    def get_candles(self, instrument, granularity='H1', count=100):
        """
        Retrieve historical candlestick data for a given instrument.

        Parameters:
        -----------
        instrument : str
            Currency pair (e.g., 'EUR_USD', 'USD_JPY')
        granularity : str
            Timeframe (e.g., 'H1' = 1 hour, 'H4' = 4 hours, 'D' = daily)
        count : int
            Number of candles to retrieve (max 5000)

        Returns:
        --------
        pandas.DataFrame
            DataFrame with columns: time, open, high, low, close, volume
        """
        try:
            # Construct API endpoint
            url = f"{self.base_url}/v3/instruments/{instrument}/candles"

            # Set query parameters
            params = {
                'granularity': granularity,
                'count': count
            }

            self.logger.info(
                f"Fetching {count} candles for {instrument} ({granularity})")

            # Make API request
            response = requests.get(url, headers=self.headers, params=params)

            # Check if request was successful
            if response.status_code == 200:
                data = response.json()
                candles = data['candles']

                # Convert to DataFrame
                df = parse_candles(candles)
                self.logger.info(f"✅ Successfully retrieved {len(df)} candles")
                return df
            else:
                self.logger.error(
                    f"❌ Failed to fetch data: {response.status_code}")
                return None

        except Exception as e:
            self.logger.error(f"❌ Error fetching candles: {str(e)}")
            return None
