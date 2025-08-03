import sqlite3
import os

def check_database(db_path):
    print(f"Checking database at: {os.path.abspath(db_path)}")
    print(f"File exists: {os.path.exists(db_path)}")
    
    if not os.path.exists(db_path):
        print("Database file does not exist!")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if the LIEU table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='LIEU'")
        table_exists = cursor.fetchone() is not None
        print(f"\nLIEU table exists: {table_exists}")
        
        if table_exists:
            # Get table info
            print("\nTable structure:")
            cursor.execute("PRAGMA table_info(LIEU)")
            columns = cursor.fetchall()
            print("Columns in LIEU table:")
            for col in columns:
                print(f"  {col[1]} ({col[2]}) - PK: {bool(col[5])}")
            
            # Count rows
            cursor.execute("SELECT COUNT(*) FROM LIEU")
            count = cursor.fetchone()[0]
            print(f"\nNumber of locations: {count}")
            
            # Show sample data
            if count > 0:
                print("\nSample locations (first 5):")
                cursor.execute("SELECT * FROM LIEU LIMIT 5")
                for row in cursor.fetchall():
                    print(f"  {row}")
        
        # List all tables
        print("\nAll tables in database:")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        for table in tables:
            print(f"- {table[0]}")
        
        conn.close()
        
    except Exception as e:
        print(f"\nError accessing database: {str(e)}")

if __name__ == "__main__":
    db_path = "employee_assignments.db"
    check_database(db_path)
    
    # Also check in the src directory
    src_db_path = os.path.join("src", "employee_assignments.db")
    if os.path.exists(src_db_path):
        print("\n" + "="*50)
        print("Found another database in src/ directory:")
        check_database(src_db_path)
