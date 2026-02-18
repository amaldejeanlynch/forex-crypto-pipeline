-- database/schema.sql
-- Database schema for Forex Data Pipeline
-- This file creates all tables and constraints needed for the project

-- Drop existing tables if they exist (allows clean re-runs)
DROP TABLE IF EXISTS extraction_metadata CASCADE;
DROP TABLE IF EXISTS raw_market_data CASCADE;

-- ============================================================================
-- Table: raw_market_data
-- Purpose: Store historical price data from OANDA API
-- ============================================================================
CREATE TABLE raw_market_data (
    id SERIAL PRIMARY KEY,
    instrument VARCHAR(20) NOT NULL,
    granularity VARCHAR(10) NOT NULL,
    time TIMESTAMP WITH TIME ZONE NOT NULL,
    open DECIMAL(20, 5) NOT NULL,
    high DECIMAL(20, 5) NOT NULL,
    low DECIMAL(20, 5) NOT NULL,
    close DECIMAL(20, 5) NOT NULL,
    volume INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    CONSTRAINT unique_candle UNIQUE (instrument, granularity, time),
    CONSTRAINT valid_prices CHECK (
        open > 0 AND 
        high > 0 AND 
        low > 0 AND 
        close > 0 AND
        high >= low
    )
);

-- Create index for faster queries
CREATE INDEX idx_instrument_time ON raw_market_data(instrument, time);
CREATE INDEX idx_granularity ON raw_market_data(granularity);

-- ============================================================================
-- Table: extraction_metadata
-- Purpose: Track data extraction runs and status
-- ============================================================================
CREATE TABLE extraction_metadata (
    id SERIAL PRIMARY KEY,
    instrument VARCHAR(20) NOT NULL,
    granularity VARCHAR(10) NOT NULL,
    extraction_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    rows_extracted INTEGER NOT NULL DEFAULT 0,
    status VARCHAR(20) NOT NULL,
    error_message TEXT,
    
    -- Constraints
    CONSTRAINT valid_status CHECK (status IN ('SUCCESS', 'FAILED', 'PARTIAL'))
);

-- Create index for tracking
CREATE INDEX idx_extraction_time ON extraction_metadata(extraction_time);
CREATE INDEX idx_status ON extraction_metadata(status);
