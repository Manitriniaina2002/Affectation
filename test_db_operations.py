import os
import sys
import sqlite3
from pathlib import Path

def test_database_operations():
    """Test database operations directly."""
    print("Testing database operations...")
    
    # Define database path
    db_path = Path('test_employee_assignments.db')
    print(f"Database path: {db_path.absolute()}")
    print(f"Database exists: {db_path.exists()}")
    
    if not db_path.exists():
        print("Error: Database file does not exist!")
        return
    
    try:
        # Connect to the database
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        print("\nConnected to database successfully!")
        
        # List all tables
        print("\nListing all tables:")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"Found {len(tables)} tables:")
        for table in tables:
            print(f"- {table[0]}")
        
        # Check LIEU table
        print("\nChecking LIEU table:")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='LIEU'")
        if not cursor.fetchone():
            print("Error: LIEU table does not exist!")
            return
        
        # Get table structure
        print("\nLIEU table structure:")
        cursor.execute("PRAGMA table_info(LIEU)")
        columns = cursor.fetchall()
        print("Columns:")
        for col in columns:
            print(f"  {col[1]} ({col[2]}) - PK: {bool(col[5])}")
        
        # Count locations
        cursor.execute("SELECT COUNT(*) FROM LIEU")
        count = cursor.fetchone()[0]
        print(f"\nNumber of locations: {count}")
        
        # Show sample data
        if count > 0:
            print("\nSample locations (first 5):")
            cursor.execute("SELECT * FROM LIEU LIMIT 5")
            for row in cursor.fetchall():
                print(f"  {row}")
        else:
            print("\nNo locations found in the database.")
        
        conn.close()
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("Starting database test...\n")
    test_database_operations()
    print("\nTest completed.")
    input("Press Enter to exit...")
