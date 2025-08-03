import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_file='employee_assignments.db'):
        self.conn = sqlite3.connect(db_file)
        self.create_tables()
        self.seed_initial_data()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        
        # Create LIEU (LOCATION) table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS LIEU (
            idlieu TEXT PRIMARY KEY,
            design TEXT NOT NULL,
            province TEXT NOT NULL
        )
        ''')
        
        # Create EMPLOYE (EMPLOYEE) table
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
        
        # Create AFFECTER (ASSIGNMENT) table
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
        
        self.conn.commit()
    
    def seed_initial_data(self):
        cursor = self.conn.cursor()
        
        # Check if LIEU table is empty
        cursor.execute("SELECT COUNT(*) FROM LIEU")
        if cursor.fetchone()[0] == 0:
            # Insert sample locations
            locations = [
                ('L1', 'Siège Social', 'Antananarivo'),
                ('L2', 'Succursale Nord', 'Antsiranana'),
                ('L3', 'Succursale Est', 'Toamasina'),
                ('L4', 'Succursale Sud', 'Fianarantsoa'),
                ('L5', 'Succursale Ouest', 'Mahajanga')
            ]
            cursor.executemany('INSERT INTO LIEU VALUES (?, ?, ?)', locations)
            
            # Insert sample employees
            employees = [
                ('E001', 'Mr', 'Rakoto', 'Jean', 'jean.rakoto@example.com', 'Chef de Service', 'L1'),
                ('E002', 'Mme', 'Rasoa', 'Marie', 'marie.rasoa@example.com', 'Comptable', 'L1'),
                ('E003', 'Mr', 'Rabe', 'Paul', 'paul.rabe@example.com', 'Responsable Ventes', 'L2'),
                ('E004', 'Mlle', 'Rakoto', 'Sofia', 'sofia.rakoto@example.com', 'Assistante', 'L3'),
                ('E005', 'Mr', 'Randria', 'Tahina', 'tahina.randria@example.com', 'Technicien', 'L4')
            ]
            cursor.executemany('''
                INSERT INTO EMPLOYE (numEmp, civilite, nom, prenom, mail, poste, idlieu)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', employees)
            
            # Insert sample assignments
            import datetime
            today = datetime.date.today()
            assignments = [
                ('A001', 'E001', 'L1', 'L2', today - datetime.timedelta(days=30), today - datetime.timedelta(days=25)),
                ('A002', 'E002', 'L1', 'L3', today - datetime.timedelta(days=60), today - datetime.timedelta(days=55)),
                ('A003', 'E003', 'L2', 'L4', today - datetime.timedelta(days=15), today - datetime.timedelta(days=10)),
                ('A004', 'E004', 'L3', 'L2', today - datetime.timedelta(days=10), today - datetime.timedelta(days=5)),
                ('A005', 'E005', 'L4', 'L1', today - datetime.timedelta(days=5), today)
            ]
            cursor.executemany('''
                INSERT INTO AFFECTER (numAffect, numEmp, AncienLieu, NouveauLieu, dateAffect, datePriseService)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', assignments)
            
            self.conn.commit()
    
    def close(self):
        self.conn.close()

if __name__ == "__main__":
    db = Database()
    print("Database initialized successfully!")
    db.close()
