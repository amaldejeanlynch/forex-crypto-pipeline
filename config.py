# config.py

class APIConfig:
    MAX_RETRIES = 3
    TIMEOUT = 30  # seconds


class DataConfig:
    # Default parameters
    DEFAULT_GRANULARITY = 'H1'
    DEFAULT_COUNT = 1000

    # Supported instruments
    SUPPORTED_INSTRUMENTS = [
        'EUR_USD',  # Euro / US Dollar
        'GBP_USD',  # British Pound / US Dollar
        'USD_JPY',  # US Dollar / Japanese Yen
        'USD_CHF',  # US Dollar / Swiss Franc
        'AUD_USD',  # Australian Dollar / US Dollar
        'USD_CAD',  # US Dollar / Canadian Dollar
        'NZD_USD',  # New Zealand Dollar / US Dollar
        'EUR_GBP',  # Euro / British Pound
        'EUR_JPY',  # Euro / Japanese Yen
        'GBP_JPY',  # British Pound / Japanese Yen
    ]

    # Supported timeframes (granularities)
    SUPPORTED_TIMEFRAMES = [
        'M1',   # 1 minute
        'M5',   # 5 minutes
        'M15',  # 15 minutes
        'M30',  # 30 minutes
        'H1',   # 1 hour
        'H4',   # 4 hours
        'D',    # Daily
        'W',    # Weekly
        'M',    # Monthly
    ]

    # Data quality settings
    MAX_NULL_PERCENTAGE = 5.0  # Maximum % of null values allowed
    MAX_DUPLICATE_PERCENTAGE = 1.0  # Maximum % of duplicates allowed


class PathConfig:
    DATA_DIR = 'data/'
    LOG_DIR = 'logs/'

    # Subdirectories
    RAW_DATA_DIR = 'data/raw/'
    PROCESSED_DATA_DIR = 'data/processed/'


class LogConfig:
    LOG_LEVEL = 'INFO'
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

    # Log to both file and console
    LOG_TO_FILE = True
    LOG_TO_CONSOLE = True

    # Log file settings
    LOG_FILE = 'logs/forex_pipeline.log'
    MAX_LOG_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
    BACKUP_COUNT = 5  # Keep 5 backup log files


class DatabaseConfig:
    # Connection pool settings
    POOL_SIZE = 5  # Number of connections to maintain
    MAX_OVERFLOW = 10  # Max connections beyond pool_size
    POOL_TIMEOUT = 30  # Seconds to wait for available connection
    POOL_RECYCLE = 3600  # Recycle connections after 1 hour

    # Query settings
    BATCH_SIZE = 1000  # Number of rows to insert at once
    QUERY_TIMEOUT = 60  # Seconds before query timeout


# Convenience function to validate configuration
def validate_config():

    # Validate API config
    if APIConfig.MAX_RETRIES < 0:
        raise ValueError("MAX_RETRIES must be >= 0")
    if APIConfig.TIMEOUT <= 0:
        raise ValueError("TIMEOUT must be > 0")

    # Validate Data config
    if DataConfig.DEFAULT_GRANULARITY not in DataConfig.SUPPORTED_TIMEFRAMES:
        raise ValueError(
            f"DEFAULT_GRANULARITY must be one of {DataConfig.SUPPORTED_TIMEFRAMES}")
    if DataConfig.DEFAULT_COUNT <= 0:
        raise ValueError("DEFAULT_COUNT must be > 0")

    # Validate Database config
    if DatabaseConfig.POOL_SIZE <= 0:
        raise ValueError("POOL_SIZE must be > 0")

    return True


if __name__ == "__main__":
    # Test configuration validity
    try:
        validate_config()
        print("✅ Configuration validated successfully!")
        print(
            f"\n📊 Supported Instruments ({len(DataConfig.SUPPORTED_INSTRUMENTS)}):")
        for instrument in DataConfig.SUPPORTED_INSTRUMENTS:
            print(f"  - {instrument}")
        print(
            f"\n⏰ Supported Timeframes ({len(DataConfig.SUPPORTED_TIMEFRAMES)}):")
        for tf in DataConfig.SUPPORTED_TIMEFRAMES:
            print(f"  - {tf}")
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
