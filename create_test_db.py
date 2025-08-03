import os
import sqlite3

def create_test_database():
    """Create a fresh test database with sample data."""
    # Remove existing database file if it exists
    db_path = 'test_employee_assignments.db'
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # Create new database and connect
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create LIEU (LOCATION) table
    cursor.execute('''
    CREATE TABLE LIEU (
        idlieu TEXT PRIMARY KEY,
        design TEXT NOT NULL,
        province TEXT NOT NULL
    )
    ''')
    
    # Insert sample locations
    locations = [
        ('L1', 'Antananarivo', 'Antananarivo'),
        ('L2', 'Toamasina', 'Toamasina'),
        ('L3', 'Antsirabe', 'Antananarivo'),
        ('L4', 'Fianarantsoa', 'Fianarantsoa'),
        ('L5', 'Mahajanga', 'Mahajanga'),
        ('L6', 'Toliara', 'Toliara'),
        ('L7', 'Antsiranana', 'Antsiranana'),
        ('L8', 'Moramanga', 'Toamasina'),
        ('L9', 'Ambalavao', 'Fianarantsoa'),
        ('L10', 'Sambava', 'Antsiranana')
    ]
    
    cursor.executemany("INSERT INTO LIEU (idlieu, design, province) VALUES (?, ?, ?)", locations)
    
    # Create other tables (minimal structure for testing)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS EMPLOYE (
        numEmp TEXT PRIMARY KEY,
        civilite TEXT CHECK(civilite IN ('Mr', 'Mme', 'Mlle')) NOT NULL,
        nom TEXT NOT NULL,
        prenom TEXT NOT NULL,
        mail TEXT UNIQUE NOT NULL,
        poste TEXT NOT NULL,
        idlieu TEXT,
        FOREIGN KEY (idlieu) REFERENCES LIEU(idlieu)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS AFFECTER (
        numAffect TEXT PRIMARY KEY,
        numEmp TEXT NOT NULL,
        AncienLieu TEXT NOT NULL,
        NouveauLieu TEXT NOT NULL,
        dateAffect DATE NOT NULL,
        datePriseService DATE NOT NULL,
        FOREIGN KEY (numEmp) REFERENCES EMPLOYE(numEmp),
        FOREIGN KEY (AncienLieu) REFERENCES LIEU(idlieu),
        FOREIGN KEY (NouveauLieu) REFERENCES LIEU(idlieu)
    )
    ''')
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    print(f"Created new test database at: {os.path.abspath(db_path)}")
    print("Sample data has been added to the LIEU table.")

if __name__ == "__main__":
    create_test_database()
