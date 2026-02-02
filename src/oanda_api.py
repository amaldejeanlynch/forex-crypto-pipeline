# src/oanda_api.py

import os
import requests
import pandas as pd
from dotenv import load_dotenv
import logging
from datetime import datetime

# Load environment variables from .env file
load_dotenv()


class OandaAPI:
    """
    A class to handle interactions with the OANDA API.

    This class manages API authentication, data retrieval,
    and basic error handling for forex data extraction.
    """

    def __init__(self):
        """
        Initialize the OANDA API connection.
        Sets up API credentials and base configuration.
        """
        # Load credentials from environment variables
        self.api_token = os.getenv('OANDA_API_TOKEN')
        self.account_id = os.getenv('OANDA_ACCOUNT_ID')
        self.base_url = os.getenv('OANDA_BASE_URL')

        # Set up request headers for authentication
        self.headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json'
        }

        # Set up logging
        self._setup_logging()

        # Validate credentials on initialization
        self._validate_credentials()

    def _setup_logging(self):
        """Configure logging for debugging and monitoring."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('oanda_api.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def _validate_credentials(self):
        """
        Validate that all required credentials are present.
        Raises ValueError if any credentials are missing.
        """
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

    def test_connection(self):
        """
        Test the API connection by fetching account details.
        Returns True if successful, False otherwise.
        """
        try:
            url = f"{self.base_url}/v3/accounts/{self.account_id}"
            response = requests.get(url, headers=self.headers)

            if response.status_code == 200:
                self.logger.info("✅ Connection successful!")
                return True
            else:
                self.logger.error(
                    f"❌ Connection failed: {response.status_code}")
                return False

        except Exception as e:
            self.logger.error(f"❌ Connection error: {str(e)}")
            return False

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
                df = self._parse_candles(candles)
                self.logger.info(f"✅ Successfully retrieved {len(df)} candles")
                return df
            else:
                self.logger.error(
                    f"❌ Failed to fetch data: {response.status_code}")
                return None

        except Exception as e:
            self.logger.error(f"❌ Error fetching candles: {str(e)}")
            return None

    def _parse_candles(self, candles):
        """
        Parse raw candle data into a structured DataFrame.

        Parameters:
        -----------
        candles : list
            Raw candle data from API response

        Returns:
        --------
        pandas.DataFrame
            Cleaned and structured data
        """
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
