import os
import sys
import sqlite3
from pathlib import Path

def test_direct_db():
    """Test direct database access with detailed error reporting."""
    print("Testing direct database access...\n")
    
    # Define database path
    db_name = "test_employee_assignments.db"
    db_path = Path(db_name)
    
    print(f"Current working directory: {Path.cwd()}")
    print(f"Database path: {db_path.absolute()}")
    print(f"Database exists: {db_path.exists()}")
    
    if not db_path.exists():
        print("\nError: Database file does not exist!")
        print("Creating a new database file...")
        try:
            # Create a new database file
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Create LIEU table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS LIEU (
                idlieu TEXT PRIMARY KEY,
                design TEXT NOT NULL,
                province TEXT NOT NULL
            )
            ''')
            
            # Insert test data
            test_data = [
                ('L1', 'Antananarivo', 'Antananarivo'),
                ('L2', 'Toamasina', 'Toamasina'),
                ('L3', 'Antsirabe', 'Antananarivo')
            ]
            
            cursor.executemany("INSERT INTO LIEU (idlieu, design, province) VALUES (?, ?, ?)", test_data)
            conn.commit()
            print("\nCreated new database with test data.")
            
        except Exception as e:
            print(f"\nError creating database: {str(e)}")
            import traceback
            traceback.print_exc()
            return
        finally:
            if 'conn' in locals():
                conn.close()
    
    # Now try to query the database
    try:
        print("\nConnecting to database...")
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
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
            print("\nSample locations:")
            cursor.execute("SELECT * FROM LIEU")
            for row in cursor.fetchall():
                print(f"  {row}")
        
        # Test inserting a new record
        print("\nTesting insert operation...")
        try:
            cursor.execute("INSERT INTO LIEU (idlieu, design, province) VALUES (?, ?, ?)", 
                          ('L999', 'Test Location', 'Test Province'))
            conn.commit()
            print("Successfully inserted test record.")
            
            # Verify the new record
            cursor.execute("SELECT * FROM LIEU WHERE idlieu = ?", ('L999',))
            record = cursor.fetchone()
            print(f"Retrieved test record: {record}")
            
            # Clean up
            cursor.execute("DELETE FROM LIEU WHERE idlieu = ?", ('L999',))
            conn.commit()
            print("Cleaned up test record.")
            
        except Exception as e:
            print(f"Error during insert test: {str(e)}")
            conn.rollback()
        
    except Exception as e:
        print(f"\nError accessing database: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        if 'conn' in locals():
            conn.close()
    
    print("\nTest completed.")
    input("Press Enter to exit...")

if __name__ == "__main__":
    test_direct_db()
