import os
import pandas as pd
import sqlite3
from urllib.parse import urlparse
import psycopg2
from psycopg2 import sql

# Get database URL from environment variable with SQLite as fallback
DATABASE_URL = os.environ.get("https://sqliteonline.com/#sqltext=%23url-sqlite%3Ddb-sqlite%0D%0A%23tab-name%3Dcloud.db%0D%0A")

def get_connection():
    """Create a database connection based on the DATABASE_URL."""
    url = urlparse(DATABASE_URL)
    
    # Use PostgreSQL if DATABASE_URL is a postgres URL
    if url.scheme == "postgres":
        conn = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
        return conn
    
    # Default to SQLite
    sqlite_db_path = DATABASE_URL.replace("sqlite:///", "")
    return sqlite3.connect(sqlite_db_path)

def create_tables():
    """Create necessary tables if they don't exist."""
    conn = get_connection()
    
    try:
        # Check if we're using SQLite or PostgreSQL
        if isinstance(conn, sqlite3.Connection):
            create_tables_sqlite(conn)
        else:
            create_tables_postgres(conn)
    finally:
        conn.close()

def create_tables_sqlite(conn):
    """Create tables for SQLite database."""
    cursor = conn.cursor()
    
    # Create scan_reports table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scan_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            scan_type TEXT,
            scan_summary TEXT,
            scan_date TEXT,
            radiologist_name TEXT,
            file_url TEXT
        )
    ''')
    
    conn.commit()

def create_tables_postgres(conn):
    """Create tables for PostgreSQL database."""
    cursor = conn.cursor()
    
    # Create scan_reports table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scan_reports (
            id SERIAL PRIMARY KEY,
            patient_name TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            scan_type TEXT,
            scan_summary TEXT,
            scan_date TEXT,
            radiologist_name TEXT,
            file_url TEXT
        )
    ''')
    
    conn.commit()

def add_scan_report(patient_name, age, gender, scan_type, scan_summary, scan_date, radiologist_name, file_url):
    """Add a new scan report to the database."""
    conn = get_connection()
    
    try:
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO scan_reports (
                patient_name, age, gender, scan_type, scan_summary, 
                scan_date, radiologist_name, file_url
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (patient_name, age, gender, scan_type, scan_summary, scan_date, radiologist_name, file_url))
        
        conn.commit()
        return True
    except Exception as e:
        print(f"Error adding scan report: {e}")
        return False
    finally:
        conn.close()

def get_all_scan_reports():
    """Get all scan reports from the database."""
    conn = get_connection()
    
    try:
        df = pd.read_sql_query('SELECT * FROM scan_reports ORDER BY scan_date DESC', conn)
        return df
    except Exception as e:
        print(f"Error getting scan reports: {e}")
        return pd.DataFrame()
    finally:
        conn.close()

def search_scan_reports(patient_name):
    """Search for scan reports by patient name."""
    conn = get_connection()
    
    try:
        cursor = conn.cursor()
        
        # Different parameter placeholder syntax for SQLite vs PostgreSQL
        if isinstance(conn, sqlite3.Connection):
            placeholder = "?"
            params = ('%' + patient_name + '%',)
        else:
            placeholder = "%s"
            params = ('%' + patient_name + '%',)
        
        query = f"SELECT * FROM scan_reports WHERE patient_name LIKE {placeholder} ORDER BY scan_date DESC"
        
        df = pd.read_sql_query(query, conn, params=params)
        return df
    except Exception as e:
        print(f"Error searching scan reports: {e}")
        return pd.DataFrame()
    finally:
        conn.close()