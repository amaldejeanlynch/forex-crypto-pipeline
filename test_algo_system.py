# test_all.py
"""
Comprehensive test script for Day 1 & Day 2.

This script tests:
1. Configuration setup
2. Logger functionality
3. API connection
4. Data extraction
5. Data parsing
6. Data validation
"""

from src.oanda_api import OandaAPI
from src.utils.validators import check_nulls, check_duplicates, validate_data
from src.utils.parsers import parse_candles
from src.utils.logger import setup_logger
from config import (
    APIConfig, DataConfig, PathConfig,
    LogConfig, DatabaseConfig, validate_config
)
import os
import sys

# Add src to path if needed
sys.path.insert(0, 'src')


def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def test_configuration():
    """Test that configuration is valid."""
    print_header("TEST 1: CONFIGURATION")

    try:
        validate_config()
        print("✅ Configuration validation: PASSED")
        print(f"   - API max retries: {APIConfig.MAX_RETRIES}")
        print(f"   - API timeout: {APIConfig.TIMEOUT}s")
        print(f"   - Default granularity: {DataConfig.DEFAULT_GRANULARITY}")
        print(f"   - Default count: {DataConfig.DEFAULT_COUNT}")
        print(
            f"   - Supported instruments: {len(DataConfig.SUPPORTED_INSTRUMENTS)}")
        print(
            f"   - Supported timeframes: {len(DataConfig.SUPPORTED_TIMEFRAMES)}")
        return True
    except Exception as e:
        print(f"❌ Configuration validation: FAILED - {e}")
        return False


def test_logger():
    """Test logger setup."""
    print_header("TEST 2: LOGGER")

    try:
        logger = setup_logger('TestLogger')
        logger.info("Testing logger functionality")
        print("✅ Logger setup: PASSED")
        print(f"   - Log file: {LogConfig.LOG_FILE}")
        print(f"   - Log level: {LogConfig.LOG_LEVEL}")
        return True
    except Exception as e:
        print(f"❌ Logger setup: FAILED - {e}")
        return False


def test_environment_variables():
    """Test that required environment variables are set."""
    print_header("TEST 3: ENVIRONMENT VARIABLES")

    required_vars = ['OANDA_API_TOKEN', 'OANDA_ACCOUNT_ID', 'OANDA_BASE_URL']
    all_present = True

    for var in required_vars:
        value = os.getenv(var)
        if value:
            # Show first 10 chars only for security
            display = value[:10] + "..." if len(value) > 10 else value
            print(f"✅ {var}: {display}")
        else:
            print(f"❌ {var}: NOT FOUND")
            all_present = False

    if all_present:
        print("\n✅ Environment variables: PASSED")
    else:
        print("\n❌ Environment variables: FAILED - Some variables missing")

    return all_present


def test_api_connection():
    """Test OANDA API connection."""
    print_header("TEST 4: API CONNECTION")

    try:
        api = OandaAPI()
        print("✅ API class initialization: PASSED")

        # Test connection
        if api.test_connection():
            print("✅ API connection test: PASSED")
            return True, api
        else:
            print("❌ API connection test: FAILED")
            return False, None
    except Exception as e:
        print(f"❌ API initialization: FAILED - {e}")
        return False, None


def test_data_extraction(api):
    """Test data extraction."""
    print_header("TEST 5: DATA EXTRACTION")

    if api is None:
        print("❌ Skipping - API not available")
        return False, None

    try:
        # Extract small sample
        print("Fetching EUR_USD (H1, 10 candles)...")
        df = api.get_candles('EUR_USD', granularity='H1', count=10)

        if df is not None and len(df) > 0:
            print(f"✅ Data extraction: PASSED")
            print(f"   - Rows retrieved: {len(df)}")
            print(f"   - Columns: {list(df.columns)}")
            print(f"\nFirst 3 rows:")
            print(df.head(3))
            return True, df
        else:
            print("❌ Data extraction: FAILED - No data returned")
            return False, None
    except Exception as e:
        print(f"❌ Data extraction: FAILED - {e}")
        return False, None


def test_data_validation(df):
    """Test data validation functions."""
    print_header("TEST 6: DATA VALIDATION")

    if df is None:
        print("❌ Skipping - No data available")
        return False

    try:
        # Test individual validators
        nulls = check_nulls(df)
        duplicates = check_duplicates(df)

        print(f"✅ Null check: {nulls}")
        print(f"✅ Duplicate check: {duplicates}")

        # Test combined validator
        results = validate_data(df)
        print(
            f"\n✅ Complete validation: {'PASSED' if results['passed'] else 'FAILED'}")

        return results['passed']
    except Exception as e:
        print(f"❌ Data validation: FAILED - {e}")
        return False


def test_multiple_instruments(api):
    """Test extraction for multiple instruments."""
    print_header("TEST 7: MULTIPLE INSTRUMENTS")

    if api is None:
        print("❌ Skipping - API not available")
        return False

    instruments = ['EUR_USD', 'USD_JPY', 'GBP_USD']
    results = {}

    for instrument in instruments:
        try:
            print(f"\nFetching {instrument}...")
            df = api.get_candles(instrument, granularity='H1', count=5)

            if df is not None and len(df) > 0:
                print(f"✅ {instrument}: {len(df)} rows")
                results[instrument] = True
            else:
                print(f"❌ {instrument}: Failed")
                results[instrument] = False
        except Exception as e:
            print(f"❌ {instrument}: Error - {e}")
            results[instrument] = False

    success_rate = sum(results.values()) / len(results) * 100
    print(f"\n✅ Success rate: {success_rate:.0f}%")

    return all(results.values())


def test_multiple_timeframes(api):
    """Test extraction for multiple timeframes."""
    print_header("TEST 8: MULTIPLE TIMEFRAMES")

    if api is None:
        print("❌ Skipping - API not available")
        return False

    timeframes = ['H1', 'H4', 'D']
    results = {}

    for tf in timeframes:
        try:
            print(f"\nFetching EUR_USD {tf}...")
            df = api.get_candles('EUR_USD', granularity=tf, count=5)

            if df is not None and len(df) > 0:
                print(f"✅ {tf}: {len(df)} rows")
                results[tf] = True
            else:
                print(f"❌ {tf}: Failed")
                results[tf] = False
        except Exception as e:
            print(f"❌ {tf}: Error - {e}")
            results[tf] = False

    success_rate = sum(results.values()) / len(results) * 100
    print(f"\n✅ Success rate: {success_rate:.0f}%")

    return all(results.values())


def main():
    """Run all tests."""
    print("\n" + "🚀" * 35)
    print("  COMPREHENSIVE TEST SUITE - DAYS 1 & 2")
    print("🚀" * 35)

    results = {}

    # Run tests
    results['config'] = test_configuration()
    results['logger'] = test_logger()
    results['env_vars'] = test_environment_variables()

    api_success, api = test_api_connection()
    results['api_connection'] = api_success

    extraction_success, df = test_data_extraction(api)
    results['data_extraction'] = extraction_success

    results['data_validation'] = test_data_validation(df)
    results['multiple_instruments'] = test_multiple_instruments(api)
    results['multiple_timeframes'] = test_multiple_timeframes(api)

    # Summary
    print_header("FINAL SUMMARY")

    total_tests = len(results)
    passed_tests = sum(results.values())
    success_rate = (passed_tests / total_tests) * 100

    print(f"\nTests passed: {passed_tests}/{total_tests}")
    print(f"Success rate: {success_rate:.1f}%\n")

    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status}: {test_name}")

    print("\n" + "=" * 70)

    if success_rate == 100:
        print("🎉 ALL TESTS PASSED! Ready for Day 3!")
    elif success_rate >= 75:
        print("⚠️  MOST TESTS PASSED - Review failures before Day 3")
    else:
        print("❌ MULTIPLE FAILURES - Fix issues before proceeding")

    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
