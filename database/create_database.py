# database/create_database.py
"""
Script to create database tables from schema.sql file.

This script:
1. Connects to PostgreSQL database
2. Executes schema.sql to create tables
3. Validates that tables were created successfully
"""

import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def create_tables():
    """Create database tables from schema.sql file."""

    print("=" * 60)
    print("DATABASE SETUP - Creating Tables")
    print("=" * 60)

    # Get database URL from environment
    db_url = os.getenv('DATABASE_URL')

    if not db_url:
        print("❌ ERROR: DATABASE_URL not found in .env file")
        print("\nAdd this to your .env file:")
        print("DATABASE_URL=postgresql://username@localhost:5432/forex_data")
        return False

    try:
        # Connect to database
        print(f"\n1. Connecting to database...")
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()
        print("✅ Connected successfully")

        # Read schema.sql file
        print("\n2. Reading schema.sql...")
        schema_path = os.path.join('database', 'schema.sql')

        if not os.path.exists(schema_path):
            print(f"❌ ERROR: {schema_path} not found")
            return False

        with open(schema_path, 'r') as f:
            schema_sql = f.read()

        print("✅ Schema file loaded")

        # Execute schema
        print("\n3. Creating tables...")
        cursor.execute(schema_sql)
        conn.commit()
        print("✅ Tables created successfully")

        # Verify tables exist
        print("\n4. Verifying tables...")
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)

        tables = cursor.fetchall()

        if tables:
            print(f"✅ Found {len(tables)} tables:")
            for table in tables:
                print(f"   - {table[0]}")
        else:
            print("⚠️  No tables found")

        # Close connection
        cursor.close()
        conn.close()

        print("\n" + "=" * 60)
        print("✅ DATABASE SETUP COMPLETE!")
        print("=" * 60)

        return True

    except psycopg2.Error as e:
        print(f"\n❌ Database error: {e}")
        return False

    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False


def test_connection():
    """Test database connection before creating tables."""

    print("\n🔍 Testing database connection...")

    db_url = os.getenv('DATABASE_URL')

    if not db_url:
        print("❌ DATABASE_URL not found in .env")
        return False

    try:
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()

        # Test query
        cursor.execute("SELECT version();")
        version = cursor.fetchone()

        print(f"✅ Connection successful!")
        print(f"   PostgreSQL version: {version[0].split(',')[0]}")

        cursor.close()
        conn.close()

        return True

    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False


if __name__ == "__main__":
    print("\n🚀 FOREX/CRYPTO DATA PIPELINE - DATABASE SETUP\n")

    # Create tables
    create_tables()
